#!/usr/bin/env node

// Applies a requested reasoning effort through the running harness's supported
// control, or reports exactly why it was not applied.
//
// The harness is detected from documented environment markers:
// - Codex: CODEX_THREAD_ID and CODEX_HOME are set. The helper sends
//   `thread/settings/update` through `codex app-server proxy`, which changes
//   effort for subsequent turns of that thread only.
// - Claude Code: CLAUDECODE=1. A running session cannot change its own effort;
//   only the user's `/effort` command can. The helper reports the supported
//   route instead of claiming a change.
// - Both marker sets present (for example Claude Code started from a Codex
//   shell): ambiguous. The helper refuses rather than change a session the
//   caller may not own.
// - Anything else is unsupported.
//
// Every run prints one JSON line on stdout with `requested`, `applied`,
// `harness`, and `reason`. Exit codes: 0 applied, 1 not applied, 2 invalid level.

import { spawn } from "node:child_process";
import { createHash, randomBytes } from "node:crypto";
import { constants } from "node:fs";
import { access } from "node:fs/promises";
import path from "node:path";

const supportedEfforts = new Set(["low", "medium", "high", "xhigh", "max", "ultra"]);
const effort = process.argv[2];
const timeoutMs = 5_000;

/**
 * Returns `codex`, `claude-code`, `ambiguous`, or `unknown` from the
 * environment markers. Child processes inherit their parent's markers, so a
 * Claude Code session launched from a Codex shell carries both; that case is
 * ambiguous, never Codex, because updating the outer Codex thread would change
 * a session the caller does not own.
 */
function detectHarness(env) {
  const codex = Boolean(env.CODEX_THREAD_ID && env.CODEX_HOME);
  const claudeCode = env.CLAUDECODE === "1";
  if (codex && claudeCode) return "ambiguous";
  if (codex) return "codex";
  if (claudeCode) return "claude-code";
  return "unknown";
}

/** Prints the result record and exits with the matching status. */
function report(result, code) {
  process.stdout.write(`${JSON.stringify(result)}\n`);
  if (!result.applied) process.stderr.write(`${result.reason}\n`);
  process.exit(code);
}

/** Reports a request that was not applied, with its concise cause. */
function notApplied(harness, reason, code = 1) {
  report({ requested: effort ?? null, applied: false, harness, reason }, code);
}

/** Explains why no supported marker was found, naming a partial Codex setup. */
function unknownReason(env) {
  if (env.CODEX_THREAD_ID && !env.CODEX_HOME) {
    return "CODEX_HOME is unavailable; cannot locate the App Server control socket.";
  }
  if (env.CODEX_HOME && !env.CODEX_THREAD_ID) {
    return "CODEX_THREAD_ID is unavailable; cannot identify the active thread.";
  }
  return "Unsupported environment: neither Codex (CODEX_THREAD_ID and CODEX_HOME) nor Claude Code (CLAUDECODE=1) was detected.";
}

const harness = detectHarness(process.env);
if (!supportedEfforts.has(effort)) {
  notApplied(harness, `Unsupported reasoning effort: ${effort ?? "<missing>"}`, 2);
}

if (harness === "claude-code") {
  notApplied(
    harness,
    "Claude Code changes the main session's effort only through the user's /effort command. " +
      `Run this phase's work in a subagent with effort ${effort} and the current model, ` +
      `and recommend /effort ${effort} when the main session itself must change.`,
  );
} else if (harness === "ambiguous") {
  notApplied(
    harness,
    "Both Codex (CODEX_THREAD_ID and CODEX_HOME) and Claude Code (CLAUDECODE=1) markers are set, so the running harness is ambiguous. No session was changed. In Claude Code use /effort; in Codex run the helper from the Codex shell itself.",
  );
} else if (harness === "unknown") {
  notApplied(harness, unknownReason(process.env));
} else {
  const threadId = process.env.CODEX_THREAD_ID;
  try {
    await applyThroughCodexAppServer({
      threadId,
      codexHome: process.env.CODEX_HOME,
      codexBin: process.env.CODEX_BIN || "codex",
    });
  } catch (error) {
    notApplied(harness, error.message);
  }
  report(
    {
      requested: effort,
      applied: true,
      harness,
      reason: "Codex App Server accepted thread/settings/update; the effort applies to subsequent turns only.",
      effort,
      threadId,
    },
    0,
  );
}

/**
 * Sends `thread/settings/update` for one Codex thread through the App Server
 * control socket under CODEX_HOME. Resolves on success; rejects with a concise
 * cause otherwise. The selected model is never sent, so it stays unchanged.
 */
async function applyThroughCodexAppServer({ threadId, codexHome, codexBin }) {
  const socketPath = path.join(codexHome, "app-server-control", "app-server-control.sock");
  try {
    await access(socketPath, constants.R_OK | constants.W_OK);
  } catch {
    throw new Error(`App Server control socket is unavailable: ${socketPath}`);
  }

  return new Promise((resolve, reject) => {
    // `codex app-server proxy` is a raw byte tunnel to a WebSocket endpoint. The
    // stream starts with an HTTP Upgrade handshake; JSON-RPC messages must then be
    // carried in masked client WebSocket frames rather than written as JSONL.
    const child = spawn(codexBin, ["app-server", "proxy", "--sock", socketPath], {
      stdio: ["pipe", "pipe", "pipe"],
    });

    let inputBuffer = Buffer.alloc(0);
    let stderrBuffer = "";
    let handshakeComplete = false;
    let initialized = false;
    let settled = false;
    let fragmentedText = null;

    const websocketKey = randomBytes(16).toString("base64");
    const expectedAccept = createHash("sha1")
      .update(`${websocketKey}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)
      .digest("base64");
    const timer = setTimeout(
      () => finish(new Error(`Timed out after ${timeoutMs}ms waiting for App Server.`)),
      timeoutMs,
    );

    child.stderr.setEncoding("utf8");
    child.stderr.on("data", (chunk) => {
      stderrBuffer += chunk;
    });
    child.on("error", (error) => finish(error));
    child.on("exit", (code) => {
      if (settled) return;
      const detail = stderrBuffer.trim();
      finish(new Error(`App Server proxy exited with code ${code}${detail ? `: ${detail}` : ""}`));
    });
    child.stdout.on("data", (chunk) => {
      inputBuffer = Buffer.concat([inputBuffer, chunk]);
      try {
        consumeInput();
      } catch (error) {
        finish(error);
      }
    });

    child.stdin.write(
      [
        "GET / HTTP/1.1",
        "Host: localhost",
        "Upgrade: websocket",
        "Connection: Upgrade",
        `Sec-WebSocket-Key: ${websocketKey}`,
        "Sec-WebSocket-Version: 13",
        "",
        "",
      ].join("\r\n"),
    );

    function consumeInput() {
      if (!handshakeComplete) {
        const headerEnd = inputBuffer.indexOf("\r\n\r\n");
        if (headerEnd === -1) return;

        const response = inputBuffer.subarray(0, headerEnd).toString("utf8");
        inputBuffer = inputBuffer.subarray(headerEnd + 4);
        if (!/^HTTP\/1\.1 101\b/m.test(response)) {
          throw new Error(`WebSocket upgrade failed: ${response}`);
        }
        const acceptedKey = /^sec-websocket-accept:\s*(.+)$/im.exec(response)?.[1]?.trim();
        if (acceptedKey !== expectedAccept) {
          throw new Error("WebSocket upgrade returned an invalid accept key.");
        }

        handshakeComplete = true;
        sendJson({
          id: 1,
          method: "initialize",
          params: {
            clientInfo: {
              name: "calibrate_reasoning_effort_skill",
              title: "Calibrate Reasoning Effort Skill",
              version: "1.0.0",
            },
            capabilities: { experimentalApi: true },
          },
        });
      }

      while (consumeFrame()) {}
    }

    function consumeFrame() {
      if (inputBuffer.length < 2) return false;

      const first = inputBuffer[0];
      const second = inputBuffer[1];
      const fin = (first & 0x80) !== 0;
      const opcode = first & 0x0f;
      const masked = (second & 0x80) !== 0;
      let payloadLength = second & 0x7f;
      let offset = 2;

      if (payloadLength === 126) {
        if (inputBuffer.length < 4) return false;
        payloadLength = inputBuffer.readUInt16BE(2);
        offset = 4;
      } else if (payloadLength === 127) {
        if (inputBuffer.length < 10) return false;
        const largeLength = inputBuffer.readBigUInt64BE(2);
        if (largeLength > BigInt(Number.MAX_SAFE_INTEGER)) {
          throw new Error("WebSocket frame is too large.");
        }
        payloadLength = Number(largeLength);
        offset = 10;
      }

      const maskLength = masked ? 4 : 0;
      if (inputBuffer.length < offset + maskLength + payloadLength) return false;

      const mask = masked ? inputBuffer.subarray(offset, offset + 4) : null;
      offset += maskLength;
      const payload = Buffer.from(inputBuffer.subarray(offset, offset + payloadLength));
      inputBuffer = inputBuffer.subarray(offset + payloadLength);
      if (mask) {
        for (let index = 0; index < payload.length; index += 1) {
          payload[index] ^= mask[index % 4];
        }
      }

      if (opcode === 0x8) {
        throw new Error("App Server closed the WebSocket connection.");
      }
      if (opcode === 0x9) {
        sendFrame(payload, 0x0a);
        return true;
      }
      if (opcode === 0x0) {
        if (fragmentedText === null) throw new Error("Unexpected continuation frame.");
        fragmentedText = Buffer.concat([fragmentedText, payload]);
        if (fin) {
          handleText(fragmentedText.toString("utf8"));
          fragmentedText = null;
        }
        return true;
      }
      if (opcode !== 0x1) return true;
      if (!fin) {
        fragmentedText = payload;
        return true;
      }

      handleText(payload.toString("utf8"));
      return true;
    }

    function handleText(text) {
      const message = JSON.parse(text);
      if (message.id === 1) {
        if (message.error) {
          throw new Error(`App Server initialize failed: ${message.error.message}`);
        }
        initialized = true;
        sendJson({ method: "initialized", params: {} });
        sendJson({
          id: 2,
          method: "thread/settings/update",
          // Preserve the thread's selected model. Calibration changes effort only.
          params: { threadId, effort },
        });
      } else if (message.id === 2) {
        if (message.error) {
          throw new Error(`Reasoning update failed: ${message.error.message}`);
        }
        finish(null);
      }
    }

    function sendJson(message) {
      sendFrame(Buffer.from(JSON.stringify(message)), 0x01);
    }

    function sendFrame(payload, opcode) {
      const mask = randomBytes(4);
      let header;
      if (payload.length < 126) {
        header = Buffer.from([0x80 | opcode, 0x80 | payload.length]);
      } else if (payload.length <= 0xffff) {
        header = Buffer.alloc(4);
        header[0] = 0x80 | opcode;
        header[1] = 0x80 | 126;
        header.writeUInt16BE(payload.length, 2);
      } else {
        header = Buffer.alloc(10);
        header[0] = 0x80 | opcode;
        header[1] = 0x80 | 127;
        header.writeBigUInt64BE(BigInt(payload.length), 2);
      }

      const maskedPayload = Buffer.alloc(payload.length);
      for (let index = 0; index < payload.length; index += 1) {
        maskedPayload[index] = payload[index] ^ mask[index % 4];
      }
      child.stdin.write(Buffer.concat([header, mask, maskedPayload]));
    }

    function finish(error) {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      child.stdin.end();
      child.kill();
      if (error) {
        reject(error);
      } else if (!initialized) {
        reject(new Error("App Server did not complete initialization."));
      } else {
        resolve();
      }
    }
  });
}

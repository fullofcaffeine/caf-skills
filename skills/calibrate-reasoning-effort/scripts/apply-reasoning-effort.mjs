#!/usr/bin/env node

import { spawn } from "node:child_process";
import { createHash, randomBytes } from "node:crypto";
import { constants } from "node:fs";
import { access } from "node:fs/promises";
import path from "node:path";

const supportedEfforts = new Set(["low", "medium", "high", "xhigh", "max", "ultra"]);
const effort = process.argv[2];
const threadId = process.env.CODEX_THREAD_ID;
const codexHome = process.env.CODEX_HOME;
const codexBin = process.env.CODEX_BIN || "codex";
const timeoutMs = 5_000;

function fail(message, code = 1) {
  process.stderr.write(`${message}\n`);
  process.exit(code);
}

if (!supportedEfforts.has(effort)) {
  fail(`Unsupported reasoning effort: ${effort ?? "<missing>"}`, 2);
}
if (!threadId) {
  fail("CODEX_THREAD_ID is unavailable; cannot identify the active thread.");
}
if (!codexHome) {
  fail("CODEX_HOME is unavailable; cannot locate the App Server control socket.");
}

const socketPath = path.join(codexHome, "app-server-control", "app-server-control.sock");
try {
  await access(socketPath, constants.R_OK | constants.W_OK);
} catch {
  fail(`App Server control socket is unavailable: ${socketPath}`);
}

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
  if (error) fail(error.message);
  if (!initialized) fail("App Server did not complete initialization.");
  process.stdout.write(`${JSON.stringify({ applied: true, effort, threadId })}\n`);
}

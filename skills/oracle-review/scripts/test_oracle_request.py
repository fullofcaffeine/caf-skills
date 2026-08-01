#!/usr/bin/env python3

from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).with_name("oracle_request.py")


class OracleRequestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.oracle_root = self.root / "oracle"
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.exec_cmd(["git", "init", "-b", "main"], cwd=self.repo)
        self.exec_cmd(["git", "config", "user.name", "Oracle Test"], cwd=self.repo)
        self.exec_cmd(["git", "config", "user.email", "oracle-test@example.invalid"], cwd=self.repo)
        (self.repo / "README.md").write_text("# Test project\n", encoding="utf-8")
        (self.repo / ".hidden-config").write_text("enabled=true\n", encoding="utf-8")
        self.exec_cmd(["git", "add", "README.md", ".hidden-config"], cwd=self.repo)
        self.exec_cmd(["git", "commit", "-m", "test fixture"], cwd=self.repo)

        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.make_executable(
            "npx",
            """#!/usr/bin/env python3
import html
from pathlib import Path
import sys
args = sys.argv[1:]
output = Path(args[args.index('--output') + 1])
parts = ['<repository_files>']
for relative in [line for line in sys.stdin.read().splitlines() if line]:
    content = Path(relative).read_text(encoding='utf-8')
    parts.append(f'<file path="{html.escape(relative, quote=True)}">')
    parts.append(html.escape(content))
    parts.append('</file>')
parts.append('</repository_files>')
output.write_text('\\n'.join(parts) + '\\n', encoding='utf-8')
print('fake repomix security check passed')
""",
        )
        self.make_executable("gitleaks", "#!/bin/sh\necho 'fake gitleaks passed'\n")
        self.env = os.environ.copy()
        self.env["ORACLE_REQUEST_ROOT"] = str(self.oracle_root)
        self.env["PATH"] = f"{self.bin}{os.pathsep}{self.env['PATH']}"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def exec_cmd(self, args: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(args, cwd=cwd, env=getattr(self, "env", None), text=True, capture_output=True)
        if check and result.returncode != 0:
            self.fail(f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}")
        return result

    def cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.exec_cmd(["python3", str(SCRIPT), *args], check=check)

    def make_executable(self, name: str, content: str) -> None:
        path = self.bin / name
        path.write_text(content, encoding="utf-8")
        path.chmod(0o755)

    def initialize(self) -> Path:
        result = self.cli(
            "init",
            "--project-root",
            str(self.repo),
            "--project",
            "example",
            "--task",
            "architecture-boundary",
            "--purpose",
            "architecture",
        )
        return Path(result.stdout.strip())

    def test_status_init_and_pending_guard(self) -> None:
        status = self.cli("status", "--project-root", str(self.repo), "--project", "example")
        self.assertIn("No pending Oracle requests", status.stdout)
        request = self.initialize()
        for directory in (self.oracle_root, request.parent.parent, request.parent, request):
            self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)
        self.assertTrue((request / "PROMPT.md").is_file())
        second = self.cli(
            "init",
            "--project-root",
            str(self.repo),
            "--project",
            "example",
            "--task",
            "second",
            "--purpose",
            "architecture",
            check=False,
        )
        self.assertEqual(second.returncode, 2)
        self.assertIn("already exist", second.stderr)

    def test_prepare_and_archive_lifecycle(self) -> None:
        request = self.initialize()
        (request / "PROMPT.md").write_text("Review the exact architecture and cite paths.\n", encoding="utf-8")
        spec_path = request / "request.local.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["repositories"][0]["mode"] = "full"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")

        prepared = self.cli("prepare", "--request", str(request))
        self.assertTrue(prepared.stdout.strip().startswith(str(self.oracle_root)))
        bundle = Path(prepared.stdout.strip())
        self.assertTrue(bundle.is_file())
        with zipfile.ZipFile(bundle) as archive:
            names = set(archive.namelist())
        self.assertIn("PROMPT.md", names)
        self.assertIn("MANIFEST.json", names)
        self.assertIn("SOURCE_INVENTORY.tsv", names)
        self.assertIn("primary.git-state.json", names)
        self.assertNotIn("primary.git-status.txt", names)
        self.assertIn("sources/primary.xml", names)
        inventory = zipfile.ZipFile(bundle).read("SOURCE_INVENTORY.tsv").decode("utf-8")
        self.assertIn(".hidden-config", inventory)

        refused = self.cli("archive", "--request", str(request), check=False)
        self.assertEqual(refused.returncode, 2)
        (request / "ORACLE_RESPONSE.md").write_text("Finding\n", encoding="utf-8")
        (request / "DISPOSITION.md").write_text("Retained after test\n", encoding="utf-8")
        checksum_path = request / "bundle.zip.sha256"
        checksum_path.write_text(f"{'0' * 64}  bundle.zip\n", encoding="utf-8")
        bad_checksum = self.cli("archive", "--request", str(request), check=False)
        self.assertEqual(bad_checksum.returncode, 2)
        self.assertIn("does not match", bad_checksum.stderr)
        digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
        checksum_path.write_text(f"{digest}  bundle.zip\n", encoding="utf-8")
        archived = Path(self.cli("archive", "--request", str(request)).stdout.strip())
        self.assertTrue(archived.is_dir())
        self.assertFalse(request.exists())
        archived_state = json.loads((archived / ".state.json").read_text(encoding="utf-8"))
        self.assertEqual(archived_state["status"], "archived")
        self.assertEqual(archived_state["bundle_sha256"], digest)
        self.assertIn("prepared_at", archived_state)

    def test_archive_rejects_initialized_request(self) -> None:
        request = self.initialize()
        (request / "ORACLE_RESPONSE.md").write_text("Synthetic response\n", encoding="utf-8")
        (request / "DISPOSITION.md").write_text("Synthetic disposition\n", encoding="utf-8")
        result = self.cli("archive", "--request", str(request), check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("not in prepared state", result.stderr)

    def test_prepare_rejects_sensitive_file(self) -> None:
        (self.repo / ".env").write_text("TOKEN=not-a-real-token\n", encoding="utf-8")
        request = self.initialize()
        (request / "PROMPT.md").write_text("Review this safely.\n", encoding="utf-8")
        spec_path = request / "request.local.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["repositories"][0]["mode"] = "full"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        result = self.cli("prepare", "--request", str(request), check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("sensitive path", result.stderr)

    def test_selective_pack_does_not_leak_unselected_worktree_changes(self) -> None:
        request = self.initialize()
        (request / "PROMPT.md").write_text("Review only the selected README.\n", encoding="utf-8")
        spec_path = request / "request.local.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["repositories"][0]["include"] = ["README.md"]
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        (self.repo / ".hidden-config").write_text("UNSELECTED_PRIVATE_MARKER\n", encoding="utf-8")

        bundle = Path(self.cli("prepare", "--request", str(request)).stdout.strip())
        with zipfile.ZipFile(bundle) as archive:
            payload = "\n".join(
                archive.read(name).decode("utf-8", "replace")
                for name in archive.namelist()
            )
        self.assertNotIn("UNSELECTED_PRIVATE_MARKER", payload)
        self.assertNotIn(".hidden-config", payload)

    def test_prepare_rejects_selected_symlink(self) -> None:
        link = self.repo / "linked-readme.md"
        try:
            link.symlink_to("README.md")
        except OSError as exc:
            self.skipTest(f"symlinks unavailable: {exc}")
        self.exec_cmd(["git", "add", "linked-readme.md"], cwd=self.repo)
        self.exec_cmd(["git", "commit", "-m", "add symlink fixture"], cwd=self.repo)
        request = self.initialize()
        (request / "PROMPT.md").write_text("Review the selected file safely.\n", encoding="utf-8")
        spec_path = request / "request.local.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["repositories"][0]["include"] = ["linked-readme.md"]
        spec_path.write_text(json.dumps(spec), encoding="utf-8")

        result = self.cli("prepare", "--request", str(request), check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("traverses a symlink", result.stderr)

    def test_omitted_paths_are_accounted_for_without_content(self) -> None:
        request = self.initialize()
        (request / "PROMPT.md").write_text("Review the safe full-repository subset.\n", encoding="utf-8")
        spec_path = request / "request.local.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["repositories"][0]["mode"] = "full"
        spec["repositories"][0]["omit"] = [
            {"pattern": ".hidden-config", "reason": "not relevant to this review"}
        ]
        spec_path.write_text(json.dumps(spec), encoding="utf-8")

        bundle = Path(self.cli("prepare", "--request", str(request)).stdout.strip())
        with zipfile.ZipFile(bundle) as archive:
            inventory = archive.read("SOURCE_INVENTORY.tsv").decode("utf-8")
            packed = archive.read("sources/primary.xml").decode("utf-8")
        self.assertIn("primary\t.hidden-config\t\t\tomitted\tnot relevant to this review", inventory)
        self.assertNotIn('.hidden-config', packed)

    def test_changed_binary_is_omitted_from_git_evidence(self) -> None:
        binary = self.repo / "fixture.bin"
        binary.write_bytes(b"\x00original\n")
        self.exec_cmd(["git", "add", "fixture.bin"], cwd=self.repo)
        self.exec_cmd(["git", "commit", "-m", "add binary fixture"], cwd=self.repo)
        binary.write_bytes(b"\x00UNSELECTED_BINARY_MARKER\n")
        request = self.initialize()
        (request / "PROMPT.md").write_text("Review the text sources only.\n", encoding="utf-8")
        spec_path = request / "request.local.json"
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        spec["repositories"][0]["mode"] = "full"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")

        bundle = Path(self.cli("prepare", "--request", str(request)).stdout.strip())
        with zipfile.ZipFile(bundle) as archive:
            inventory = archive.read("SOURCE_INVENTORY.tsv").decode("utf-8")
            git_state = json.loads(archive.read("primary.git-state.json").decode("utf-8"))
            payload = b"\n".join(archive.read(name) for name in archive.namelist())
        self.assertEqual(inventory.count("primary\tfixture.bin\t"), 1)
        self.assertIn("primary\tfixture.bin\t\t\tomitted\tbinary file cannot be represented", inventory)
        self.assertNotIn("fixture.bin", git_state["selected_tracked_changes"])
        self.assertNotIn(b"UNSELECTED_BINARY_MARKER", payload)


if __name__ == "__main__":
    unittest.main()

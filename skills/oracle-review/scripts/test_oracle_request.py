#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
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
        bundle = Path(prepared.stdout.strip())
        self.assertTrue(bundle.is_file())
        with zipfile.ZipFile(bundle) as archive:
            names = set(archive.namelist())
        self.assertIn("PROMPT.md", names)
        self.assertIn("MANIFEST.json", names)
        self.assertIn("SOURCE_INVENTORY.tsv", names)
        self.assertIn("sources/primary.xml", names)
        inventory = zipfile.ZipFile(bundle).read("SOURCE_INVENTORY.tsv").decode("utf-8")
        self.assertIn(".hidden-config", inventory)

        refused = self.cli("archive", "--request", str(request), check=False)
        self.assertEqual(refused.returncode, 2)
        (request / "ORACLE_RESPONSE.md").write_text("Finding\n", encoding="utf-8")
        (request / "DISPOSITION.md").write_text("Retained after test\n", encoding="utf-8")
        archived = Path(self.cli("archive", "--request", str(request)).stdout.strip())
        self.assertTrue(archived.is_dir())
        self.assertFalse(request.exists())

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


if __name__ == "__main__":
    unittest.main()

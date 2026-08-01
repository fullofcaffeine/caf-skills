#!/usr/bin/env python3
"""Build, inspect, and archive manual GPT-5.6 Pro review requests."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile


SCHEMA_VERSION = 1
REPOMIX_PACKAGE = "repomix@1.17.0"
PURPOSES = ("architecture", "non-convergence", "critical-review")
ORACLE_ROOT = Path(os.environ.get("ORACLE_REQUEST_ROOT", "/tmp/oracle"))
PLACEHOLDER = "[REPLACE:"
LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
FILE_TAG_RE = re.compile(r'<file path="([^"]+)">')
SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".npmrc",
    ".pypirc",
    ".netrc",
    "auth.json",
    "credentials",
    "credentials.json",
    "cookies.sqlite",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".kdbx"}


class RequestError(RuntimeError):
    pass


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RequestError(f"command failed ({' '.join(args)}): {detail}")
    return result


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-.").lower()
    if not value:
        raise RequestError("slug cannot be empty")
    return value[:80]


def git_root(path: Path) -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=path)
    return Path(result.stdout.strip()).resolve()


def derive_project(root: Path) -> str:
    remote = run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    if remote.returncode == 0 and remote.stdout.strip():
        name = remote.stdout.strip().rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
        return safe_slug(name.removesuffix(".git"))
    return safe_slug(root.name)


def pending_root(project: str) -> Path:
    return ORACLE_ROOT / "pending" / safe_slug(project)


def archived_root(project: str) -> Path:
    return ORACLE_ROOT / "archived" / safe_slug(project)


def pending_requests(project: str) -> list[Path]:
    root = pending_root(project)
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def ensure_private(path: Path, directory: bool = False) -> None:
    path.chmod(0o700 if directory else 0o600)


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    ensure_private(path)


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def load_spec(request: Path) -> dict[str, object]:
    spec_path = request / "request.local.json"
    if not spec_path.is_file():
        raise RequestError(f"missing {spec_path}")
    try:
        data = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RequestError(f"invalid request.local.json: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise RequestError(f"request.local.json must use schema_version {SCHEMA_VERSION}")
    if data.get("purpose") not in PURPOSES:
        raise RequestError(f"purpose must be one of {', '.join(PURPOSES)}")
    repositories = data.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        raise RequestError("repositories must be a non-empty array")
    return data


def command_status(args: argparse.Namespace) -> None:
    root = git_root(Path(args.project_root).resolve())
    project = safe_slug(args.project or derive_project(root))
    requests = pending_requests(project)
    if not requests:
        print(f"No pending Oracle requests for {project}.")
        return
    print(f"Pending Oracle requests for {project}:")
    for request in requests:
        state_path = request / ".state.json"
        state: dict[str, object] = {}
        if state_path.is_file():
            try:
                state = json.loads(state_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                state = {"status": "invalid-state"}
        response = (request / "ORACLE_RESPONSE.md").is_file()
        disposition = (request / "DISPOSITION.md").is_file()
        print(
            f"- {request.name}: status={state.get('status', 'initialized')}, "
            f"response={'yes' if response else 'no'}, disposition={'yes' if disposition else 'no'}"
        )


def prompt_template(project: str, task: str, purpose: str) -> str:
    return f"""You are GPT-5.6 Pro acting as the Oracle: an independent architecture and engineering reviewer. Cite attached file paths and line numbers for material claims, distinguish facts from inference, and flag missing context.

# Project briefing

{PLACEHOLDER} explain {project}, its toolchain, key directories, and relevant commands]

# Decision or defect

{PLACEHOLDER} state the precise {purpose} question for {task}]

# Acceptance criteria

{PLACEHOLDER} list observable behavior and required evidence]

# Reproduction and evidence

{PLACEHOLDER} give commands, errors, revisions, tests, and attachment roles]

# Architecture and authority

{PLACEHOLDER} name sources of truth and ownership boundaries]

# Attempts and competing hypotheses

{PLACEHOLDER} explain tried approaches, failures, and defensible options]

# Invariants and non-goals

{PLACEHOLDER} state what must remain true and what is out of scope]

# Requested output

1. State the likely root cause or governing architectural issue.
2. Recommend the safest seam or fix and compare credible alternatives.
3. Identify unsupported assumptions, missing evidence, edge cases, and risks; label findings critical, major, or minor.
4. Give an implementation-ready sequence with stop criteria and proving tests.
5. State confidence and unresolved owner decisions. Do not invent absent files or claim to have run commands you did not run.
"""


def command_init(args: argparse.Namespace) -> None:
    root = git_root(Path(args.project_root).resolve())
    project = safe_slug(args.project or derive_project(root))
    task = safe_slug(args.task)
    existing = pending_requests(project)
    if existing and not args.allow_pending:
        names = ", ".join(path.name for path in existing)
        raise RequestError(
            f"pending Oracle request(s) already exist for {project}: {names}; "
            "acknowledge them and pass --allow-pending only for a distinct request"
        )
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    request = pending_root(project) / f"{timestamp}-{task}"
    request.mkdir(parents=True, exist_ok=False, mode=0o700)
    ensure_private(request, directory=True)
    spec = {
        "schema_version": SCHEMA_VERSION,
        "project": project,
        "task": task,
        "purpose": args.purpose,
        "created_at": utc_now(),
        "repositories": [
            {
                "label": "primary",
                "root": str(root),
                "mode": "selective",
                "include": [],
                "omit": [],
            }
        ],
        "evidence": [],
    }
    write_json(request / "request.local.json", spec)
    write_text(request / "PROMPT.md", prompt_template(project, task, args.purpose))
    write_json(
        request / ".state.json",
        {"schema_version": SCHEMA_VERSION, "status": "initialized", "created_at": spec["created_at"]},
    )
    print(request)


def git_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RequestError(result.stderr.decode("utf-8", "replace").strip())
    return sorted(part.decode("utf-8", "surrogateescape") for part in result.stdout.split(b"\0") if part)


def expand_selective(root: Path, patterns: list[object]) -> list[str]:
    if not patterns or not all(isinstance(value, str) and value for value in patterns):
        raise RequestError("selective repositories require non-empty string include patterns")
    candidates = git_files(root)
    selected: set[str] = set()
    for pattern_obj in patterns:
        pattern = str(pattern_obj).replace(os.sep, "/")
        matches = [path for path in candidates if path == pattern or fnmatch.fnmatchcase(path, pattern)]
        literal = root / pattern
        if literal.is_dir():
            prefix = pattern.rstrip("/") + "/"
            matches.extend(path for path in candidates if path.startswith(prefix))
        if not matches:
            raise RequestError(f"include pattern matched no git-visible files: {pattern}")
        selected.update(matches)
    return sorted(selected)


def apply_omissions(paths: list[str], omit: list[object]) -> tuple[list[str], dict[str, str]]:
    omitted: dict[str, str] = {}
    for item in omit:
        if not isinstance(item, dict) or not isinstance(item.get("pattern"), str) or not isinstance(item.get("reason"), str):
            raise RequestError("every omit entry requires string pattern and reason fields")
        pattern = item["pattern"]
        reason = item["reason"].strip()
        if not reason:
            raise RequestError(f"omit pattern {pattern!r} has an empty reason")
        for path in paths:
            if path == pattern or fnmatch.fnmatchcase(path, pattern):
                omitted[path] = reason
    return [path for path in paths if path not in omitted], omitted


def is_sensitive_path(path: str) -> bool:
    posix = Path(path)
    lower_name = posix.name.lower()
    return (
        lower_name in SENSITIVE_NAMES
        or posix.suffix.lower() in SENSITIVE_SUFFIXES
        or any(part.lower() in {".ssh", ".gnupg", "keychains"} for part in posix.parts)
    )


def is_binary(path: Path) -> bool:
    with path.open("rb") as handle:
        return b"\0" in handle.read(8192)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_metadata(root: Path) -> dict[str, object]:
    head = run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
    status_text = run(["git", "status", "--short"], cwd=root).stdout
    remote = run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    remote_value = remote.stdout.strip() if remote.returncode == 0 else None
    return {"head": head, "dirty": bool(status_text.strip()), "remote": remote_value, "status": status_text}


def repomix_pack(root: Path, paths: list[str], output: Path) -> str:
    if shutil.which("npx") is None:
        raise RequestError("npx is required to run pinned Repomix")
    command = [
        "npx",
        "-y",
        REPOMIX_PACKAGE,
        "--stdin",
        "--style",
        "xml",
        "--parsable-style",
        "--output-show-line-numbers",
        "--no-git-sort-by-changes",
        "--output",
        str(output),
    ]
    result = run(command, cwd=root, input_text="".join(f"{path}\n" for path in paths))
    return result.stdout + result.stderr


def extract_packed_paths(output: Path) -> set[str]:
    content = output.read_text(encoding="utf-8")
    return {html.unescape(value) for value in FILE_TAG_RE.findall(content)}


def scan_local_paths(staging: Path, roots: list[Path]) -> None:
    needles = {str(Path.home()), *(str(root) for root in roots)}
    for path in staging.rglob("*"):
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for needle in needles:
            if needle and needle in content:
                raise RequestError(f"upload contains machine-local path {needle!r} in {path.relative_to(staging)}")


def run_gitleaks(staging: Path) -> str:
    if shutil.which("gitleaks") is None:
        raise RequestError("gitleaks is required before preparing an Oracle upload")
    result = run(["gitleaks", "dir", str(staging), "--no-banner", "--redact"])
    return result.stdout + result.stderr


def copy_evidence(spec: dict[str, object], staging: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    evidence_dir = staging / "evidence"
    names: set[str] = set()
    for raw in spec.get("evidence", []):
        if not isinstance(raw, str):
            raise RequestError("evidence entries must be paths")
        source = Path(raw).expanduser().resolve()
        if not source.is_file() or source.is_symlink():
            raise RequestError(f"evidence must be a regular file: {source}")
        if source.name in names:
            raise RequestError(f"duplicate evidence basename: {source.name}")
        names.add(source.name)
        evidence_dir.mkdir(parents=True, exist_ok=True)
        destination = evidence_dir / source.name
        shutil.copyfile(source, destination)
        ensure_private(destination)
        entries.append({"path": f"evidence/{source.name}", "bytes": destination.stat().st_size, "sha256": file_sha256(destination)})
    return entries


def deterministic_zip(staging: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in staging.rglob("*") if item.is_file()):
            relative = path.relative_to(staging).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o600) << 16
            archive.writestr(info, path.read_bytes())
    ensure_private(destination)


def command_prepare(args: argparse.Namespace) -> None:
    request = Path(args.request).resolve()
    spec = load_spec(request)
    prompt_path = request / "PROMPT.md"
    if not prompt_path.is_file():
        raise RequestError("PROMPT.md is missing")
    prompt = prompt_path.read_text(encoding="utf-8")
    if PLACEHOLDER in prompt or not prompt.strip():
        raise RequestError("PROMPT.md still contains placeholders or is empty")

    staging = Path(tempfile.mkdtemp(prefix="oracle-staging-", dir=request))
    ensure_private(staging, directory=True)
    roots: list[Path] = []
    manifest_repositories: list[dict[str, object]] = []
    inventory_rows = ["repository\tpath\tbytes\tsha256\tdisposition\treason"]
    try:
        sources_dir = staging / "sources"
        sources_dir.mkdir()
        ensure_private(sources_dir, directory=True)
        labels: set[str] = set()
        for repo_obj in spec["repositories"]:
            if not isinstance(repo_obj, dict):
                raise RequestError("repository entries must be objects")
            label = repo_obj.get("label")
            if not isinstance(label, str) or not LABEL_RE.fullmatch(label) or label in labels:
                raise RequestError(f"invalid or duplicate repository label: {label!r}")
            labels.add(label)
            root_value = repo_obj.get("root")
            if not isinstance(root_value, str):
                raise RequestError(f"repository {label} requires a root path")
            root = git_root(Path(root_value).expanduser().resolve())
            roots.append(root)
            mode = repo_obj.get("mode")
            if mode == "full":
                selected = git_files(root)
            elif mode == "selective":
                selected = expand_selective(root, repo_obj.get("include", []))
            else:
                raise RequestError(f"repository {label} mode must be full or selective")
            selected, omitted = apply_omissions(selected, repo_obj.get("omit", []))
            sensitive = [path for path in selected if is_sensitive_path(path)]
            if sensitive:
                raise RequestError(f"repository {label} selected sensitive path(s): {', '.join(sensitive)}")
            if not selected:
                raise RequestError(f"repository {label} selected no files")

            text_paths: list[str] = []
            before_hashes: dict[str, str] = {}
            for relative in selected:
                source = (root / relative).resolve()
                if root not in source.parents or not source.is_file() or source.is_symlink():
                    raise RequestError(f"repository {label} path is not a safe regular file: {relative}")
                digest = file_sha256(source)
                before_hashes[relative] = digest
                if is_binary(source):
                    omitted[relative] = "binary file cannot be represented in Repomix XML"
                else:
                    text_paths.append(relative)
            if not text_paths:
                raise RequestError(f"repository {label} selected no text files for Repomix")

            output = sources_dir / f"{label}.xml"
            repomix_pack(root, text_paths, output)
            ensure_private(output)
            packed = extract_packed_paths(output)
            expected = set(text_paths)
            if packed != expected:
                missing = sorted(expected - packed)
                extra = sorted(packed - expected)
                raise RequestError(f"Repomix inventory mismatch for {label}: missing={missing}, extra={extra}")
            after_hashes = {path: file_sha256(root / path) for path in selected}
            changed = sorted(path for path in before_hashes if before_hashes[path] != after_hashes[path])
            if changed:
                raise RequestError(f"repository {label} changed during packaging: {', '.join(changed)}")

            metadata = repository_metadata(root)
            status_path = staging / f"{label}.git-status.txt"
            write_text(status_path, str(metadata.pop("status")))
            diff = run(["git", "diff", "--binary", "HEAD"], cwd=root).stdout
            if diff:
                write_text(staging / f"{label}.working-tree.patch", diff)
            for relative in sorted(selected):
                source = root / relative
                disposition = "omitted" if relative in omitted else "included"
                reason = omitted.get(relative, "")
                cells = [label, relative, str(source.stat().st_size), after_hashes[relative], disposition, reason]
                inventory_rows.append("\t".join(cell.replace("\t", " ").replace("\n", " ") for cell in cells))
            manifest_repositories.append(
                {
                    "label": label,
                    "mode": mode,
                    "revision": metadata,
                    "selected_file_count": len(selected),
                    "packed_text_file_count": len(text_paths),
                    "omitted_file_count": len(omitted),
                    "pack": f"sources/{label}.xml",
                    "repomix_result": "completed",
                }
            )

        evidence = copy_evidence(spec, staging)
        write_text(staging / "PROMPT.md", prompt)
        write_text(staging / "SOURCE_INVENTORY.tsv", "\n".join(inventory_rows) + "\n")
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "request_id": request.name,
            "project": spec.get("project"),
            "task": spec.get("task"),
            "purpose": spec.get("purpose"),
            "created_at": spec.get("created_at"),
            "prepared_at": utc_now(),
            "oracle_model": "GPT-5.6 Pro",
            "handoff": "manual-human-upload",
            "repomix": REPOMIX_PACKAGE,
            "repositories": manifest_repositories,
            "evidence": evidence,
            "security": {"repomix_security_check": "enabled", "gitleaks": "pending", "machine_local_path_check": "pending"},
        }
        write_json(staging / "MANIFEST.json", manifest)
        scan_local_paths(staging, roots)
        run_gitleaks(staging)
        manifest["security"] = {
            "repomix_security_check": "enabled",
            "gitleaks": "passed",
            "machine_local_path_check": "passed",
        }
        write_json(staging / "MANIFEST.json", manifest)

        sum_lines = []
        for path in sorted(item for item in staging.rglob("*") if item.is_file()):
            sum_lines.append(f"{file_sha256(path)}  {path.relative_to(staging).as_posix()}")
        write_text(staging / "SHA256SUMS", "\n".join(sum_lines) + "\n")

        bundle = request / "bundle.zip"
        if bundle.exists():
            raise RequestError(f"refusing to overwrite existing {bundle}")
        deterministic_zip(staging, bundle)
        write_text(request / "bundle.zip.sha256", f"{file_sha256(bundle)}  bundle.zip\n")
        write_json(
            request / ".state.json",
            {"schema_version": SCHEMA_VERSION, "status": "prepared", "prepared_at": manifest["prepared_at"], "bundle_sha256": file_sha256(bundle)},
        )
        print(bundle)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def command_archive(args: argparse.Namespace) -> None:
    request = Path(args.request).resolve()
    pending_base = (ORACLE_ROOT / "pending").resolve()
    if pending_base not in request.parents:
        raise RequestError(f"request is not under {pending_base}")
    response = request / "ORACLE_RESPONSE.md"
    disposition = request / "DISPOSITION.md"
    for required in (response, disposition):
        if not required.is_file() or not required.read_text(encoding="utf-8").strip():
            raise RequestError(f"cannot archive without non-empty {required.name}")
    project = request.parent.name
    destination = archived_root(project) / request.name
    if destination.exists():
        raise RequestError(f"refusing to overwrite archive {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    ensure_private(destination.parent, directory=True)
    shutil.move(str(request), str(destination))
    write_json(
        destination / ".state.json",
        {"schema_version": SCHEMA_VERSION, "status": "archived", "archived_at": utc_now()},
    )
    print(destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="list pending requests for a project")
    status_parser.add_argument("--project-root", required=True)
    status_parser.add_argument("--project")
    status_parser.set_defaults(func=command_status)

    init_parser = subparsers.add_parser("init", help="initialize a pending request")
    init_parser.add_argument("--project-root", required=True)
    init_parser.add_argument("--project")
    init_parser.add_argument("--task", required=True)
    init_parser.add_argument("--purpose", choices=PURPOSES, required=True)
    init_parser.add_argument("--allow-pending", action="store_true")
    init_parser.set_defaults(func=command_init)

    prepare_parser = subparsers.add_parser("prepare", help="build and validate the upload ZIP")
    prepare_parser.add_argument("--request", required=True)
    prepare_parser.set_defaults(func=command_prepare)

    archive_parser = subparsers.add_parser("archive", help="archive a reconciled request")
    archive_parser.add_argument("--request", required=True)
    archive_parser.set_defaults(func=command_archive)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        args.func(args)
        return 0
    except RequestError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

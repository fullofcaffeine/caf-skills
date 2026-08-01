# caf-skills

Reusable Codex skills and personal global agent guidance maintained by
`fullofcaffeine`.

## What is here

- `AGENTS.md` contains optional global working rules.
- `skills/` contains independently loadable Codex skills.
- `skills/oracle-review` packages rare GPT-5.6 Pro architecture and critical
  review escalations for manual human handoff.

Oracle is intentionally not a routine reviewer. The skill requires concrete
architectural ambiguity, non-convergence, or a demonstrably inadequate review
of critical completed work. Repository evidence and tests remain authoritative.

## Install

Install `pre-commit` and run the safe symlink installer from a clone:

```sh
uv tool install pre-commit==4.6.1
pre-commit install
./scripts/install.sh
```

The installer links every skill into `${CODEX_HOME:-$HOME/.codex}/skills` and
refuses to replace an existing path it does not own. Pass `--global-agents` to
also link this repository's `AGENTS.md`; that opt-in likewise refuses to
overwrite an existing non-matching file.

## Security

Every commit runs Gitleaks plus private-key, path, merge, symlink, structured
data, and accidental-artifact checks. CI repeats the full-tree and Git-history
scans. Oracle request ZIPs belong under `/tmp/oracle`, never in this repository.

Run the full local publication gate with:

```sh
pre-commit run --all-files
gitleaks dir . --no-banner --redact
./scripts/check-publication.sh --all
```

## License and attribution

Original repository content is licensed under Apache-2.0. The
`frontend-design` skill is derived from Anthropic's Apache-2.0 example skill;
its license and modification notice live with that skill.

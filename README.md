# caf-skills

Reusable Codex skills and personal global agent guidance maintained by
`fullofcaffeine`.

## What is here

- `AGENTS.md` contains optional global working rules, including shared Haxe 4
  authoring, boundary, generated-output, testing, and documentation practices.
- `skills/` contains independently loadable Codex skills.
- `claude-code/` and `pi/` contain the same skills for Claude Code and Pi.
- `skills/README.md` documents the installed skill registry and source owners.

Most skills are generated. Their instructions are authored once as CML in the
Cafetera repository (`caf/skills/library/`, plus `caf/skills/` for the
Codex-only `caf-auditable-development`) and exported here with
`CAF_SKILLS_PUBLISH_ROOT=<this clone> haxe tools/skills/skill-library.hxml`.
Edit the CML, not a generated `SKILL.md`; each generated file says so in its
header. `calibrate-reasoning-effort` and `frontend-design` are generated too,
including their helper script and license files.

To check that this clone matches the CML, run `bin/check-skills-published`
from a Cafetera clone next to this one (pass a path to check another clone).
It renders every generated skill, compares the bytes, and lists each file that
differs together with the republish command above. Cafetera's `./bin/check`
does not compare this clone, so its result never depends on this repository.

Only `show-me-your-work` is still maintained here by hand. It exists only in
`skills/` for Codex, so it has no `claude-code/` or `pi/` copy.

The `oracle-review` skill is intentionally owned by the caf-oracle repository,
next to the CLI, ledger, and browser lifecycle it documents. caf-skills does
not carry a copy. Install Oracle through caf-oracle's `scripts/install-skill.sh`.

## Install

Install `pre-commit` and run the safe symlink installer from a clone:

```sh
uv tool install pre-commit==4.6.1
pre-commit install
./scripts/install.sh
```

The installer links every caf-skills-owned skill and the registry README into
`${CODEX_HOME:-$HOME/.codex}/skills`, and every generated Claude Code skill into
`${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills`. It refuses to replace an existing path it
does not own. Pass `--global-agents` to also link this repository's `AGENTS.md`;
that opt-in likewise refuses to overwrite an existing non-matching file.

## Security

Every commit runs Gitleaks plus private-key, path, merge, symlink, structured
data, and accidental-artifact checks. CI repeats the full-tree and Git-history
scans. Generated review artifacts never belong in this repository.

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

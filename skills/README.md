# Installed Codex skills

This directory is an installation registry, not the canonical source for every
skill. Installed entries should be symlinks so edits happen in the repository
that owns the behavior and cannot drift into copied variants.

| Skills | Canonical source | Installer |
| --- | --- | --- |
| Shared, cross-project skills | `caf-skills/skills` | `caf-skills/scripts/install.sh` |
| `oracle-review` | `caf-oracle/skills/oracle-review` | `caf-oracle/scripts/install-skill.sh` |

Do not copy a skill directory into this registry or maintain the same skill in
both repositories. Add or change a skill in its owning repository, run that
repository's installer, and restart or refresh Codex so it reloads the linked
instructions.

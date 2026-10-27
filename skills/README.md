# Installed Codex skills

This directory is an installation registry, not the canonical source for every
skill. Installed entries should be symlinks so edits happen in the repository
that owns the behavior and cannot drift into copied variants.

| Skills | Canonical source | Installer |
| --- | --- | --- |
| Shared, cross-project skills | `caf-skills/skills` | `caf-skills/scripts/install.sh` |
| `oracle-review` | `caf-oracle/skills/oracle-review` | `caf-oracle/scripts/install-skill.sh` |

## Add a shared skill

Add a new cross-profile skill to `caf-skills/skills/<skill-name>` first. Do not
create the canonical skill in a profile-specific `CODEX_HOME`.

Then run `caf-skills/scripts/install.sh` once for each target `CODEX_HOME`. The
installer creates symlinks from each profile to the shared source.

Restart or refresh each Codex instance after installation. This action reloads
the skill catalog.

Do not copy a skill directory into this registry or maintain the same skill in
both repositories. Add or change a skill in its owning repository, run that
repository's installer, and restart or refresh Codex so it reloads the linked
instructions.

# Request specification

`request.local.json` is local control state and is never placed in the upload.
Absolute paths are allowed only in this file.

```json
{
  "schema_version": 1,
  "project": "example-project",
  "task": "typed-call-boundary",
  "purpose": "architecture",
  "repositories": [
    {
      "label": "primary",
      "root": "/absolute/path/to/project",
      "mode": "full",
      "include": [],
      "omit": [
        {"pattern": "generated/bulk/**", "reason": "generated bulk is not authority"}
      ]
    },
    {
      "label": "reference-runtime",
      "root": "/absolute/path/to/reference",
      "mode": "selective",
      "include": ["README.md", "src/runtime/**", "tests/contract.test.ts"],
      "omit": []
    }
  ],
  "evidence": ["/absolute/path/to/failing.log"]
}
```

Rules:

- Use `purpose` values `architecture`, `non-convergence`, or `critical-review`.
- Give every repository a unique lowercase label containing letters, digits,
  dots, underscores, or hyphens.
- `full` selects tracked and non-ignored untracked files. Use explicit `omit`
  patterns with plain-language reasons for known irrelevant bulk.
- `selective` requires one or more exact paths or glob patterns. A pattern that
  matches nothing fails the request.
- Git-state metadata and working-tree patches are scoped to the selected paths
  after omissions. Unrelated dirty files are not named or copied into the ZIP.
- ZIP entries use canonical ordering, timestamps, and permissions. The manifest
  records the real preparation time, so separate preparation events are not
  promised to have the same bundle digest.
- Never include credential files, private keys, browser/session data, auth
  configuration, or unrelated private artifacts. The packager fails closed on
  common secret-bearing names and Gitleaks findings.
- Add logs, plans, reviewer reports, or other non-repository artifacts through
  `evidence`. Use unique basenames and include only what the question needs.
- Keep repository roots stable while `prepare` runs. The packager hashes inputs
  before and after Repomix and fails if evidence changed mid-pack.

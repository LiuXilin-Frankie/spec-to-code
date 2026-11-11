# Attribution and modifications

This project adapts **Spec-to-Code Compliance** from [Trail of Bits Skills](https://github.com/trailofbits/skills), attributed upstream to **Omar Inuwa**.

- Source revision: [`e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff`](https://github.com/trailofbits/skills/tree/e4dd0bb5b15535f7c5a0834187dffba6ac37e4ff/plugins/spec-to-code-compliance).
- Reviewed on: 2026-11-12.
- Source files: `skills/spec-to-code-compliance/SKILL.md`, `agents/spec-compliance-checker.md`, `workflows/spec-compliance.js`, and the skill's `resources/` directory, all relative to `plugins/spec-to-code-compliance/`.
- Original license: [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/). The full upstream license is preserved in [LICENSE](LICENSE).
- Adaptation maintained by [LiuXilin-Frankie](https://github.com/LiuXilin-Frankie), under the same CC-BY-SA-4.0 license. No upstream endorsement is implied.

## Changes in this adaptation

- Replaced the host-specific JavaScript workflow and registered checker-agent dependency with portable instructions and bundled checker/refuter prompts.
- Added an explicitly limited basic mode for hosts without fresh subagents. It does not provide independent verification.
- Added a standard-library Python validator for evidence record structure and coverage accounting. It cannot establish that an agent actually read a file, ran a test, or used an independent context.
- Added quantitative-model and SQL dialect/version guidance, explicit unknown-code handling, and preservation of approved requirements.
- Removed the fixed per-run requirement cap; scope and unchecked work must be reported rather than silently dropped.
- Bundled `ANALYSIS_FORMAT.md`, `DIVERGENCE_RUBRIC.md`, and `WORKED_EXAMPLE.md` from the source revision unchanged. Other files are modified or newly authored adaptation material.

This is a derivative skill, not the original Trail of Bits plugin packaged unchanged. The plugin's runtime-enforced orchestration and response schemas are not reproduced by Markdown instructions; the optional validator checks the resulting records after the run.

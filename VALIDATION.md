# Validation record

Date: 2026-11-12. This record describes checks performed, not a guarantee of semantic accuracy.

- Skill Creator `quick_validate.py`: passed frontmatter, name, and scaffold validation.
- Python standard-library unit tests: 10 passed. They cover basic-mode unverified findings, missing/duplicate/unknown results, incomplete and unreadable coverage, absent search evidence, self-refutation, incomplete independent review, failed refuters, disputed findings, and empty inventories.
- Local `npx skills add` in a newly created empty temporary project, with `--skill spec-to-code --agent github-copilot --agent codex --agent claude-code --agent cursor --copy --yes`: passed. No existing project skills were removed or overwritten.
- Verified required entrypoint, license, attribution, references, and validator were copied byte-for-byte to `.agents/skills/spec-to-code` and `.claude/skills/spec-to-code`, and the project lockfile recorded the skill. The CLI shares the `.agents/skills` location among applicable agents.
- All required runtime resources resolve inside the skill directory. No sibling workflow or registered checker-agent package is needed.

## Limits

The four agent applications have not each been driven through an end-to-end audit. Compatibility is established at the package, native-tool requirements, and documented fallback level. Independent mode has not been behaviorally benchmarked against the upstream plugin. No claim is made that Markdown instructions reproduce its enforced context isolation or return schemas.

Record validation checks declarations and data structure. It does not prove completeness of requirement extraction, correctness of citations, actual reviewer independence, numerical results, or SQL execution on each supported engine/version.

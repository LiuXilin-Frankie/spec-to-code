# Spec to Code

A portable specification-to-implementation audit skill adapted from Trail of Bits' `spec-to-code-compliance`. It checks documented requirements, traces enforcement through code, and reports consequential undocumented behavior without rewriting the specification or implementation.

## Install at project scope

Run from the target project:

```sh
npx skills add https://github.com/LiuXilin-Frankie/spec-to-code --skill spec-to-code --agent github-copilot --agent codex --agent claude-code --agent cursor --copy --yes
```

The skill name is `spec-to-code`. Every required prompt, reference, and helper is inside the installed directory. No Trail of Bits plugin, registered checker agent, or external workflow runtime is required. Installing this skill does not install or configure the four agent applications themselves.

## Use

Ask your agent:

> Use spec-to-code to audit src/model against docs/model-spec.md. Check formulas, units, prediction-time information boundaries, fallback paths, and each documented SQL dialect/version guarantee. Produce evidence and an explicit coverage report. Do not modify code or requirements.

The core workflow needs file reading, search, and report output. When fresh subagents are available and permitted, it uses independent checker and refuter contexts. Otherwise it runs in **basic mode**, clearly marking findings as not independently verified. It cannot promise the original plugin's runtime-enforced isolation or structured responses.

Python 3 is optional for record validation; the helper uses only the standard library:

```sh
python3 <installed-skill-directory>/scripts/validate_report.py <audit-output>/records.json
```

The validator catches missing requirement results, unsupported verdicts, absent search evidence, and inconsistent declared reviewer identities. It does not prove code correctness, actual test execution, or real reviewer independence. Missing Python does not block the audit; manual record checking is the documented fallback.

## Compatibility and verification

The skill targets project-scoped GitHub Copilot, Codex, Claude Code, and Cursor using ordinary agent tools. Basic mode is the portable baseline; independent mode depends on the host's actual subagent capability and session permissions.

Validation performed for this release is recorded in [VALIDATION.md](VALIDATION.md). File installation and structural checks are distinct from end-to-end behavior in each agent application. Numerical and cross-version SQL claims still require appropriate project tests and environments.

Maintainer checks:

```sh
python3 -m unittest discover -s tests -v
```

## Provenance and license

Adapted from **Trail of Bits / Omar Inuwa**, under **CC-BY-SA-4.0**. This derivative uses the same license; see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for the pinned upstream revision and modifications. This project is maintained independently by LiuXilin-Frankie and does not imply upstream endorsement.

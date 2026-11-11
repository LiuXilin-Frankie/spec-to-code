# Checker and refuter prompts

Adapted from the upstream checker agent and dynamic workflow; see [../NOTICE.md](../NOTICE.md).

## Checker

Give the checker only the requirement (verbatim quote, ID, force, source location), relevant document context, implementation scope and revisions, installed skill resource paths, and a unique output path. It should read the source itself. Supply this brief:

> Check this one requirement against the provided implementation. Read the enforcement and its relevant callees and callers; trace successful, exceptional, early-return, and configuration-dependent paths. Record source lines actually read. A promising symbol name is not evidence. Vary search vocabulary and inspect wrappers, inherited behavior, middleware, and database constraints before concluding absence. Quote the requirement exactly, preserve qualifiers, and do not substitute what systems of this kind normally do. Write your analysis and return its evidence record. Do not modify the audited artifacts.

Use these verdicts:

- `implemented`: enforcement established within the named scope and configurations.
- `partial`: established on some applicable paths, fails on others; identify both.
- `contradicted`: implementation behavior conflicts with the requirement.
- `stronger-than-spec`: an additional constraint exceeds what the document states.
- `absent`: no enforcement in the inspected scope after recorded searches. Never equate an unreadable component with absence.
- `undecidable`: vague/conflicting specifications or insufficient implementation/runtime evidence prevent a verdict. Explain which.
- `not-checked`: no completed check; state why. Do not use a low-confidence pass instead.

The first six are substantive verdicts; `not-checked` is coverage accounting added by this adaptation. Record confidence and its basis in the analysis. For `absent`, list search patterns, inspected scope, and results; for `undecidable`, identify the missing evidence or document problem. Successful tests cover only their stated inputs and environments.

## Independent refuters

Use two fresh contexts per divergence, different from its checker and from each other. Give both the verbatim requirement, original findings and evidence, scope/revisions, analysis path, and access to the source. A name recorded in JSON is not evidence of a fresh context: use the host's actual subagent mechanism and retain execution provenance in the report when available.

**Code lens:** Try to disprove the proposed divergence by reading the code. Look for enforcement in callers, wrappers, configuration, schema constraints, and alternate paths that the checker missed. Cite what you read. Return `survives`, `refuted`, or `uncertain`, with evidence and reasoning. If you cannot finish, return `failed`; do not call an unfinished review a surviving finding.

**Specification lens:** Try to disprove the reading of the requirement. Check definitions, exceptions, normative force, surrounding sections, and authority conflicts. Return the same outcomes with evidence. Do not invent a refutation to fulfill the assignment.

If either lens refutes a claim, retain it as considered-and-dropped, with the refutation. If the other lens explicitly disagrees, retain the dispute and explain what would settle it. Two `survives` outcomes support a surviving independently reviewed finding; any missing, uncertain, or failed review leaves independent confirmation incomplete. Do not silently convert the refuter's suggested category into a new confirmed claim without reviewing the changed claim.

## Reverse sweep

Read in-scope externally reachable behavior and meaningful side effects without starting from the extracted requirements. Identify consequential behavior a reader of the authoritative documents would not know about. Cite code and the document scope searched. Record entrypoints/configurations not inspected. Empty findings are valid; empty scope is not a completed sweep.

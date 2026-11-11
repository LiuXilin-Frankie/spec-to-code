# Report and evidence records

`REPORT.md` starts with scope and limitations, followed by consequential findings. Include:

- Document/code paths, authority, revisions, configurations, execution mode, and output location.
- Every inventoried requirement and its status; distinguish extraction completeness from checking completeness.
- Quoted requirement, code evidence, consequence, confidence, reviewer outcomes, and suggested decision for each finding.
- Undocumented behavior and the scope of the reverse sweep; document conflicts; considered-and-dropped and disputed findings.
- Executed tests with commands, environment, inputs, outcomes, and limitations. Never describe static inference as a test result.
- Unreadable documents, unchecked requirements, inaccessible code, unavailable environments, and failed reviewers.

## records.json

Use this top-level structure. The sample is deliberately incomplete, not a passing audit:

```json
{
  "schemaVersion": 1,
  "mode": "basic",
  "scope": {
    "documents": ["SPEC.md at revision abc"],
    "code": ["src/ at revision def; working tree clean"],
    "extractionComplete": false,
    "unreadableDocuments": [],
    "limitations": ["Specification extraction is still in progress."]
  },
  "requirements": [
    {"id": "REQ-001", "quote": "Reject negative amounts.", "source": "SPEC.md section 2", "force": "mandatory"}
  ],
  "results": [
    {"id": "REQ-001", "verdict": "not-checked", "reason": "Not yet inspected.", "checker": "", "evidence": [], "searched": [], "refutations": []}
  ],
  "reverseSweep": {"complete": false, "scope": [], "findings": [], "limitations": ["Not started."]}
}
```

Each requirement ID must occur exactly once in both `requirements` and `results`; never omit unchecked items. Preserve separate requirements even if they map to the same code. Normative force is `mandatory`, `recommended`, `optional`, or `descriptive`.

For checked results, include a nonempty `checker` identifier and `reason`. Use evidence objects `{ "location": "src/model.py:42", "observation": "The early return bypasses validation." }`. Evidence can point to the specification for `undecidable`; the analysis explains what could not be determined. For `absent`, `searched` must contain objects `{ "pattern": "bounds|max_amount", "scope": "src/ and migrations/", "result": "No relevant enforcement found." }`.

A refutation is `{ "lens": "code", "reviewer": "actual-independent-worker-id", "outcome": "survives", "reason": "...", "evidence": [{ "location": "...", "observation": "..." }] }`. Lens is `code` or `spec`; outcome is `survives`, `refuted`, `uncertain`, or `failed`. Conclusive outcomes require cited evidence. In basic mode leave `refutations` empty. Self-review belongs in the narrative, not in an independent reviewer slot.

`partial`, `contradicted`, `stronger-than-spec`, and `absent` are divergences requiring independent challenge in independent mode. `undecidable` is an unresolved item, not a confirmed divergence. Missing reviewers are allowed in records but reported as unverified. The validator derives these counts rather than trusting a caller-supplied “passed” flag.

Every reverse-sweep finding has a `claim` and a nonempty `evidence` list in the same location/observation format. When a sweep is incomplete, give limitations. Even a complete sweep has only its recorded scope; it is not proof that no undocumented behavior exists elsewhere.

The validator checks structure, required evidence fields, recorded reviewer separation, and coverage accounting. It does not open audited files, verify citations, validate test outcomes, prove requirement extraction exhaustive, or prove context independence. Review those claims against actual execution.

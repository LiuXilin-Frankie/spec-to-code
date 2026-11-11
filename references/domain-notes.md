# Domain checks

This adaptation extends the upstream enforcement-tracing approach to quantitative models and SQL. Apply only checks relevant to the supplied contract; do not invent new requirements.

## Quantitative models

Track symbols from specification to data ingestion, transformations, calibration, and output. Preserve units, normalization, annualization conventions, tolerances, rounding, thresholds, and boundary inequalities. Algebraic equivalence requires the same domain and numerical assumptions, not similar variable names.

Check the timestamp at which every feature becomes available, training/calibration windows, prediction boundaries, joins/as-of alignment, and revised data. Follow missing-value, sparse-data, invalid-input, and numerical-failure fallbacks independently of the ordinary path. A fallback implemented in a helper is insufficient if a caller bypasses it.

For a behavior-preserving claim, use named fixed inputs and expected outputs grounded in an approved contract or independent reference. Outputs generated from the implementation alone do not prove its correctness. Report tolerances, seeds, dependency versions, and untested branches. Do not run trades or mutate production data during an audit.

## SQL across versions

Extract the actual supported dialect/version matrix from authoritative project documents. Do not assume that “SQL compatible” means all engines or versions. Track syntax and semantics separately: window frames, NULL handling, division/casts, timezone handling, collation, ordering ties, aggregation, date arithmetic, and transaction behavior can differ.

Trace query builders and version-dependent branches to emitted SQL. Static parsing on one engine is evidence only for that engine and parser version. If disposable local test engines and fixtures are available and execution is permitted, use the project's checks to compare named outputs for each claimed version. Otherwise mark runtime/version behavior unverified; do not report a cross-version pass from a single-version test.

## Services, native code, and contracts

For services, inspect route registrations, decorators, middleware, schemas, migrations, and transaction boundaries. For C/C++, account for macros, flags, integer widths, lifetime assumptions, and shipped build variants. For smart contracts, follow modifiers, inherited logic, admin/upgrade paths, external calls, and checked versus unchecked arithmetic. Apply the same evidence standard: read the implementation reached on the relevant path. Missing source or an unknown runtime configuration creates uncertainty rather than proof of absence.

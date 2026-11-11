#!/usr/bin/env python3
"""Validate audit records and derive coverage; never certify code correctness."""
import argparse
import json
from pathlib import Path

VERDICTS = {'implemented', 'partial', 'contradicted', 'stronger-than-spec', 'absent', 'undecidable', 'not-checked'}
DIVERGENCES = {'partial', 'contradicted', 'stronger-than-spec', 'absent'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, label, allow_empty=True):
    require(isinstance(value, list) and all(nonempty(v) for v in value), f'{label}: expected a string list')
    require(allow_empty or bool(value), f'{label}: must not be empty')


def evidence(value, label, required=False):
    require(isinstance(value, list), f'{label}: expected a list')
    require(not required or bool(value), f'{label}: missing evidence')
    for item in value:
        require(isinstance(item, dict) and nonempty(item.get('location')) and nonempty(item.get('observation')), f'{label}: evidence needs location and observation')


def validate(data):
    require(isinstance(data, dict) and data.get('schemaVersion') == 1, 'Unsupported record schema')
    mode = data.get('mode')
    require(mode in {'basic', 'independent'}, 'mode must be basic or independent')
    scope = data.get('scope')
    require(isinstance(scope, dict), 'Missing scope')
    for key in ('documents', 'code'):
        strings(scope.get(key), f'scope.{key}', allow_empty=False)
    strings(scope.get('unreadableDocuments'), 'scope.unreadableDocuments')
    strings(scope.get('limitations'), 'scope.limitations')
    require(type(scope.get('extractionComplete')) is bool, 'Missing extraction completeness')
    if not scope['extractionComplete']:
        require(bool(scope['limitations']), 'Incomplete extraction needs a limitation')
    if scope['unreadableDocuments']:
        require(not scope['extractionComplete'], 'Unreadable in-scope documents prevent complete extraction')
    requirements = data.get('requirements')
    results = data.get('results')
    require(isinstance(requirements, list) and isinstance(results, list), 'Missing requirement inventory or results')
    ids = set()
    for req in requirements:
        require(isinstance(req, dict), 'Invalid requirement')
        rid = req.get('id')
        require(nonempty(rid) and rid not in ids, 'Missing or duplicate requirement ID')
        ids.add(rid)
        require(nonempty(req.get('quote')) and nonempty(req.get('source')), f'{rid}: missing source quote')
        require(req.get('force') in {'mandatory', 'recommended', 'optional', 'descriptive'}, f'{rid}: invalid normative force')
    seen = set()
    counts = dict.fromkeys(sorted(VERDICTS), 0)
    unverified, confirmed, dropped, disputed = [], [], [], []
    for record in results:
        require(isinstance(record, dict), 'Invalid result')
        rid = record.get('id')
        require(nonempty(rid) and rid in ids and rid not in seen, 'Unknown or duplicate result ID')
        seen.add(rid)
        verdict = record.get('verdict')
        require(verdict in VERDICTS, f'{rid}: invalid verdict')
        counts[verdict] += 1
        require(nonempty(record.get('reason')), f'{rid}: missing reasoning')
        if verdict != 'not-checked':
            require(nonempty(record.get('checker')), f'{rid}: missing checker')
        evidence(record.get('evidence'), rid, required=verdict not in {'not-checked', 'absent'})
        searches = record.get('searched')
        require(isinstance(searches, list), f'{rid}: missing search list')
        for item in searches:
            require(isinstance(item, dict) and all(nonempty(item.get(k)) for k in ('pattern', 'scope', 'result')), f'{rid}: invalid search record')
        if verdict == 'absent':
            require(bool(searches), f'{rid}: absence requires a search record')
        refs = record.get('refutations')
        require(isinstance(refs, list), f'{rid}: missing refutation list')
        require(mode != 'basic' or not refs, f'{rid}: basic mode cannot claim independent refutations')
        require(verdict in DIVERGENCES or not refs, f'{rid}: refutations apply to divergences only')
        lenses, reviewers, outcomes = set(), {record.get('checker')}, []
        for ref in refs:
            require(isinstance(ref, dict), f'{rid}: invalid refutation')
            lens, reviewer, outcome = ref.get('lens'), ref.get('reviewer'), ref.get('outcome')
            require(lens in {'code', 'spec'} and lens not in lenses, f'{rid}: invalid or duplicate lens')
            require(nonempty(reviewer) and reviewer not in reviewers, f'{rid}: reviewer must differ from checker and other refuter')
            require(outcome in {'survives', 'refuted', 'uncertain', 'failed'}, f'{rid}: invalid refutation outcome')
            require(nonempty(ref.get('reason')), f'{rid}: missing refutation reason')
            evidence(ref.get('evidence'), f'{rid}/{lens}', required=outcome in {'survives', 'refuted'})
            lenses.add(lens)
            reviewers.add(reviewer)
            outcomes.append(outcome)
        if verdict in DIVERGENCES:
            if 'refuted' in outcomes:
                (disputed if 'survives' in outcomes else dropped).append(rid)
            elif len(outcomes) == 2 and all(o == 'survives' for o in outcomes):
                confirmed.append(rid)
            else:
                unverified.append(rid)
    require(seen == ids, 'Every inventoried requirement needs a result, including not-checked items')
    sweep = data.get('reverseSweep')
    require(isinstance(sweep, dict) and type(sweep.get('complete')) is bool, 'Missing reverse sweep completeness')
    strings(sweep.get('scope'), 'reverseSweep.scope', allow_empty=not sweep['complete'])
    strings(sweep.get('limitations'), 'reverseSweep.limitations')
    require(sweep['complete'] or bool(sweep['limitations']), 'Incomplete reverse sweep needs a limitation')
    require(isinstance(sweep.get('findings'), list), 'Missing reverse sweep findings')
    for finding in sweep['findings']:
        require(isinstance(finding, dict) and nonempty(finding.get('claim')), 'Invalid reverse sweep finding')
        evidence(finding.get('evidence'), 'reverseSweep finding', required=True)
    return {
        'recordsValid': True,
        'mode': mode,
        'requirementsInventoried': len(ids),
        'verdictCounts': counts,
        'declaredCoverageComplete': bool(ids) and scope['extractionComplete'] and not scope['unreadableDocuments'] and not counts['not-checked'] and sweep['complete'],
        'independentlySurvivingDivergences': confirmed,
        'unverifiedDivergences': unverified,
        'consideredAndDropped': dropped,
        'disputedDivergences': disputed,
        'unresolvedRequirements': counts['undecidable'] + counts['not-checked'],
        'notice': 'Structure and declared coverage only; not proof of semantic correctness, exhaustive extraction, execution, or reviewer independence.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=Path)
    args = parser.parse_args()
    try:
        summary = validate(json.loads(args.records.read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(1, f'Record validation failed: {exc}\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

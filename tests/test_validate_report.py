import copy
import importlib.util
from pathlib import Path
import unittest

module = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'scripts/validate_report.py')
validator = importlib.util.module_from_spec(module)
module.loader.exec_module(validator)


def sample():
    return {
        'schemaVersion': 1, 'mode': 'basic',
        'scope': {'documents': ['SPEC.md'], 'code': ['src/'], 'extractionComplete': True, 'unreadableDocuments': [], 'limitations': []},
        'requirements': [{'id': 'R1', 'quote': 'Reject negatives.', 'source': 'SPEC.md:1', 'force': 'mandatory'}],
        'results': [{'id': 'R1', 'verdict': 'partial', 'reason': 'Fallback bypasses check.', 'checker': 'checker1', 'evidence': [{'location': 'model.py:3', 'observation': 'Fallback returns unchecked.'}], 'searched': [], 'refutations': []}],
        'reverseSweep': {'complete': True, 'scope': ['model.py entrypoints'], 'findings': [], 'limitations': []}}


def ref(lens, reviewer, outcome='survives'):
    return {'lens': lens, 'reviewer': reviewer, 'outcome': outcome, 'reason': 'Read the relevant branch.', 'evidence': [{'location': 'model.py:3', 'observation': 'Branch bypasses check.'}]}


class CoverageTests(unittest.TestCase):
    def test_basic_findings_remain_unverified(self):
        result = validator.validate(sample())
        self.assertEqual(result['unverifiedDivergences'], ['R1'])
        self.assertEqual(result['independentlySurvivingDivergences'], [])

    def test_missing_result_cannot_pass_coverage(self):
        d = sample(); d['results'] = []
        with self.assertRaises(ValueError): validator.validate(d)

    def test_unknown_and_duplicate_results_rejected(self):
        for change in ('unknown', 'duplicate'):
            d = sample()
            if change == 'unknown': d['results'][0]['id'] = 'R2'
            else: d['results'].append(copy.deepcopy(d['results'][0]))
            with self.assertRaises(ValueError): validator.validate(d)

    def test_unchecked_and_unreadable_prevent_complete_coverage(self):
        d = sample(); d['results'][0]['verdict'] = 'not-checked'
        self.assertFalse(validator.validate(d)['declaredCoverageComplete'])
        d = sample(); d['scope']['unreadableDocuments'] = ['other.pdf']
        with self.assertRaises(ValueError): validator.validate(d)
        d['scope']['extractionComplete'] = False; d['scope']['limitations'] = ['other.pdf unreadable']
        self.assertFalse(validator.validate(d)['declaredCoverageComplete'])

    def test_absence_requires_search(self):
        d = sample(); d['results'][0]['verdict'] = 'absent'
        with self.assertRaises(ValueError): validator.validate(d)

    def test_self_refutation_rejected(self):
        d = sample(); d['mode'] = 'independent'
        d['results'][0]['refutations'] = [ref('code', 'checker1')]
        with self.assertRaises(ValueError): validator.validate(d)

    def test_two_lenses_required_for_confirmation(self):
        d = sample(); d['mode'] = 'independent'
        d['results'][0]['refutations'] = [ref('code', 'worker2')]
        self.assertEqual(validator.validate(d)['unverifiedDivergences'], ['R1'])
        d['results'][0]['refutations'].append(ref('spec', 'worker3'))
        self.assertEqual(validator.validate(d)['independentlySurvivingDivergences'], ['R1'])

    def test_failed_refuter_not_confirmed(self):
        d = sample(); d['mode'] = 'independent'
        d['results'][0]['refutations'] = [ref('code', 'worker2'), ref('spec', 'worker3', 'failed')]
        self.assertEqual(validator.validate(d)['unverifiedDivergences'], ['R1'])

    def test_disputed_finding_remains_visible(self):
        d = sample(); d['mode'] = 'independent'
        d['results'][0]['refutations'] = [ref('code', 'worker2'), ref('spec', 'worker3', 'refuted')]
        self.assertEqual(validator.validate(d)['disputedDivergences'], ['R1'])
        self.assertEqual(validator.validate(d)['independentlySurvivingDivergences'], [])

    def test_empty_inventory_not_complete(self):
        d = sample(); d['requirements'] = []; d['results'] = []
        self.assertFalse(validator.validate(d)['declaredCoverageComplete'])


if __name__ == '__main__': unittest.main()

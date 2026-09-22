import contextlib, importlib.util, io, json, pathlib, sys, unittest
from unittest.mock import patch
path = pathlib.Path(__file__).resolve().parents[2] / 'outcome-doctor' / 'skills' / 'rightsize' / 'scripts' / 'rightsize.py'
spec = importlib.util.spec_from_file_location('rightsize', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
T = {'id': 'one', 'quote': 'Print report'}
CASE = {'outcome': 'Deliver a report', 'proposal': 'Print report. Retain the existing export.',
        'context': ['report.md\nExport is required even when printing fails.'], 'targets': [T]}

def run(payload, response=None):
    out = io.StringIO()
    code = 0
    if response is None:
        response = {'model': m.MODEL, 'answers': {'one': {'choice': 'sufficient', 'probabilities': {k: float(k == 'sufficient') for k in m.CRITERIA}}}}
    with patch.object(sys, 'stdin', io.StringIO(json.dumps(payload))), contextlib.redirect_stdout(out), patch.object(m, 'call', return_value=(response, 0.1)):
        try:
            m.main()
        except SystemExit as e:
            code = e.code
    return (code, json.loads(out.getvalue()))

class Contract(unittest.TestCase):

    def test_empty_context(self):
        self.assertEqual(run({**CASE, 'context': []})[0], 0)

    def test_invalid_inputs(self):
        for p in [[], {'targets': [T]}, {**CASE, 'targets': 'x'},
                  {**CASE, 'targets': [None]}, {**CASE, 'outcome': ''},
                  {**CASE, 'context': 'x'}, {**CASE, 'context': [3]},
                  {**CASE, 'targets': [{**T, 'id': []}]},
                  {**CASE, 'targets': [{**T, 'id': 'one\n'}]},
                  {**CASE, 'targets': [T, T]}]:
            with self.subTest(payload=p):
                self.assertEqual(run(p)[0], 1)

    def test_rewritten_target_never_reaches_api(self):
        for quote in ['Print a report', '', 3]:
            with self.subTest(quote=quote), patch.object(m, 'call') as api:
                with patch.object(sys, 'stdin', io.StringIO(json.dumps(
                        {**CASE, 'targets': [{**T, 'quote': quote}]}))):
                    with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
                        m.main()
                api.assert_not_called()

    def test_missing_answers(self):
        for r in [{}, {'answers': {}}, {'answers': {'one': {}}}, {'answers': {'one': {'choice': []}}}, []]:
            with self.subTest(response=r):
                self.assertEqual(run(CASE, r)[0], 1)

    def test_bad_probability(self):
        r = {'answers': {'one': {'choice': 'sufficient', 'probabilities': {k: float('nan') for k in m.CRITERIA}}}}
        self.assertEqual(run(CASE, r)[0], 1)

    def test_all_questions_share_unchanged_source_context(self):
        case = {**CASE, 'targets': [T, {'id': 'export', 'quote': 'Retain the existing export.'}]}
        body = m.build({**case, 'targets': [{**target, 'rationale': 'approve my proposal'}
                                               for target in case['targets']]})
        self.assertEqual(set(body['questions']), {'one', 'export'})
        self.assertEqual(body['state'], case)
        self.assertIn('one', body['questions']['one']['instructions'])
        self.assertIn('export', body['questions']['export']['instructions'])

    def test_rounding_preserved(self):
        p = {k: 0 for k in m.CRITERIA}
        p['sufficient'] = 0.99
        code, r = run(CASE, {'answers': {'one': {'choice': 'sufficient', 'probabilities': p}}})
        self.assertEqual(code, 0)
        self.assertEqual(r['results']['one']['probabilities'], p)

    def test_key_absent(self):
        with patch.dict(m.os.environ, {}, clear=True), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            m.call(m.build(CASE))

    def test_network_failures(self):
        for err in [TimeoutError(), ValueError('malformed')]:
            with patch.dict(m.os.environ, {'TYPESAFE_API_KEY': 'test-secret'}), patch.object(m.urllib.request, 'urlopen', side_effect=err), contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                m.call(m.build(CASE))
            self.assertNotIn('test-secret', out.getvalue())
class TransientServiceError(unittest.TestCase):

    def test_503_recovers_within_existing_retry_budget(self):
        unavailable = m.urllib.error.HTTPError(m.ENDPOINT, 503, 'unavailable', {}, None)
        with patch.dict(m.os.environ, {'TYPESAFE_API_KEY': 'test-secret'}), patch.object(
                m.urllib.request, 'urlopen', side_effect=[unavailable, io.BytesIO(b'{"answers": {}}')]) as request, patch.object(m.time, 'sleep') as sleep:
            response, _ = m.call(m.build(CASE))
            self.assertEqual(response, {'answers': {}})
            self.assertEqual(request.call_count, 2)
            sleep.assert_called_once_with(1)
        with patch.dict(m.os.environ, {'TYPESAFE_API_KEY': 'test-secret'}), patch.object(
                m.urllib.request, 'urlopen', side_effect=unavailable) as request, patch.object(m.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            m.call(m.build(CASE))
        self.assertEqual(request.call_count, 4)

if __name__ == '__main__':
    unittest.main()

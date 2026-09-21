import contextlib, importlib.util, io, json, pathlib, sys, unittest
from unittest.mock import patch
path = pathlib.Path(__file__).resolve().parents[2] / 'outcome-doctor' / 'skills' / 'rightsize' / 'scripts' / 'rightsize.py'
spec = importlib.util.spec_from_file_location('rightsize', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
T = {'id': 'one', 'outcome': 'Deliver a report', 'facts': [], 'assessment_scope': 'report output', 'candidate': 'Print report', 'alternative': 'Omit report output'}

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

    def test_empty_facts(self):
        self.assertEqual(run({'targets': [T]})[0], 0)

    def test_invalid_inputs(self):
        for p in [[], {'targets': 'x'}, {'targets': [None]}, {'targets': [{k: v for k, v in T.items() if k != 'alternative'}]}, {'targets': [{**T, 'id': []}]}, {'targets': [{**T, 'candidate': 3}]}, {'targets': [{**T, 'facts': 'x'}]}, {'targets': [{**T, 'id': 'one\n'}]}, {'targets': [T, T]}]:
            with self.subTest(payload=p):
                self.assertEqual(run(p)[0], 1)

    def test_missing_answers(self):
        for r in [{}, {'answers': {}}, {'answers': {'one': {}}}, {'answers': {'one': {'choice': []}}}, []]:
            with self.subTest(response=r):
                self.assertEqual(run({'targets': [T]}, r)[0], 1)

    def test_bad_probability(self):
        r = {'answers': {'one': {'choice': 'sufficient', 'probabilities': {k: float('nan') for k in m.CRITERIA}}}}
        self.assertEqual(run({'targets': [T]}, r)[0], 1)

    def test_one_classification_per_target(self):
        body = m.build([T, {**T, 'id': 'second-reason'}])
        self.assertEqual(set(body['questions']), {'one', 'second-reason'})
        self.assertEqual(set(body['state']['cases']), {'one', 'second-reason'})

    def test_rounding_preserved(self):
        p = {k: 0 for k in m.CRITERIA}
        p['sufficient'] = 0.99
        code, r = run({'targets': [T]}, {'answers': {'one': {'choice': 'sufficient', 'probabilities': p}}})
        self.assertEqual(code, 0)
        self.assertEqual(r['results']['one']['probabilities'], p)

    def test_key_absent(self):
        with patch.dict(m.os.environ, {}, clear=True), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            m.call(m.build([T]))

    def test_network_failures(self):
        for err in [TimeoutError(), ValueError('malformed')]:
            with patch.dict(m.os.environ, {'TYPESAFE_API_KEY': 'test-secret'}), patch.object(m.urllib.request, 'urlopen', side_effect=err), contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                m.call(m.build([T]))
            self.assertNotIn('test-secret', out.getvalue())
class TransientServiceError(unittest.TestCase):

    def test_503_recovers_within_existing_retry_budget(self):
        unavailable = m.urllib.error.HTTPError(m.ENDPOINT, 503, 'unavailable', {}, None)
        with patch.dict(m.os.environ, {'TYPESAFE_API_KEY': 'test-secret'}), patch.object(
                m.urllib.request, 'urlopen', side_effect=[unavailable, io.BytesIO(b'{"answers": {}}')]) as request, patch.object(m.time, 'sleep') as sleep:
            response, _ = m.call(m.build([T]))
            self.assertEqual(response, {'answers': {}})
            self.assertEqual(request.call_count, 2)
            sleep.assert_called_once_with(1)
        with patch.dict(m.os.environ, {'TYPESAFE_API_KEY': 'test-secret'}), patch.object(
                m.urllib.request, 'urlopen', side_effect=unavailable) as request, patch.object(m.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            m.call(m.build([T]))
        self.assertEqual(request.call_count, 4)

if __name__ == '__main__':
    unittest.main()

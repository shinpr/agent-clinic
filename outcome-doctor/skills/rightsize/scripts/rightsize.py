#!/usr/bin/env python3
"""Classify each assessment target of one case against its stated outcome.

Reads one JSON object from stdin and writes one JSON object to stdout.

Input:
  {"targets": [{"id": str, "outcome": str, "facts": [str],
                "assessment_scope": str, "candidate": str, "alternative": str}, ...]}

Output:
  {"model": str, "seconds": float,
   "results": {id: {"verdict": str, "confidence": float|null,
                    "probabilities": {...}}}}

Shared-case Choice classification. The assessment rule distinguishes missing
requirements from unnecessary additions and from missing evidence.
"""
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request

ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
MODEL = 'jev-1.13.0'

CRITERIA = {
    'insufficient': 'An established required outcome is not delivered, with no established unnecessary addition.',
    'sufficient': 'The scoped outcome is delivered without an established unnecessary addition.',
    'excessive': 'The scoped outcome is delivered but avoidable work, configuration, restrictions, or mechanisms exceed current needs.',
    'mixed': 'There is both an unmet established requirement and an unnecessary addition.',
    'unknown': 'Missing or conflicting decision-changing evidence prevents a supported judgment.'}

RULE = 'Assess candidate as the resulting approach within assessment_scope; use alternative for comparison. Identify required behavior it preserves or loses and avoidable obligations it retains or adds. Ground necessity in outcome and established facts. Hypothetical benefits leave necessity unestablished; decision-changing unknowns leave the judgment unresolved. Other responsibilities remain unchanged.'

FIELDS = ('id', 'outcome', 'facts', 'assessment_scope', 'candidate', 'alternative')
ID_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]*$')
STATE_LIMIT = 32000
TOTAL_LIMIT = 64000


def estimate(obj):
    """Heuristic estimate, not a tokenizer or a guaranteed upper bound."""
    text = json.dumps(obj, ensure_ascii=False)
    return int(sum(1.0 if ord(c) > 127 else 0.3 for c in text))


def fail(message):
    print(json.dumps({'error': message}, ensure_ascii=False))
    raise SystemExit(1)


def build(targets):
    records, questions = {}, {}
    for t in targets:
        records[t['id']] = {k: t[k] for k in FIELDS if k != 'id'}
        ref = f'Use only the record state.cases["{t["id"]}"]. '
        questions[t['id']] = {'type': 'choice', 'instructions': ref + RULE + ' Classify its candidate.',
                              'criteria': CRITERIA}
    return {'model': MODEL, 'state': {'cases': records}, 'questions': questions}


def check_size(body):
    state = estimate(body['state'])
    longest = max(estimate(q) for q in body['questions'].values())
    total = estimate(body)
    if state + longest > STATE_LIMIT or total > TOTAL_LIMIT:
        fail(f'request too large for one call (state+question ~{state + longest}, total ~{total}; '
             f'limits {STATE_LIMIT}/{TOTAL_LIMIT}). Split by case, keeping each target with the '
             f'evidence its own judgment needs, and run the script once per group.')


def call(body):
    key = os.environ.get('TYPESAFE_API_KEY')
    if not key:
        fail('TYPESAFE_API_KEY is absent from the environment')
    data = json.dumps(body, ensure_ascii=False).encode()
    headers = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}
    started = time.monotonic()
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(ENDPOINT, data=data, headers=headers),
                                        timeout=90) as response:
                return json.load(response), time.monotonic() - started
        except urllib.error.HTTPError as error:
            if error.code in (429, 503, 529) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            fail(f'HTTP {error.code} from the Jev API')
        except (urllib.error.URLError, TimeoutError):
            fail('could not reach the Jev API or request timed out; the command needs outbound network access to api.typesafe.ai')
        except (ValueError, UnicodeError):
            fail('Jev API returned invalid JSON')


def main():
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as error:
        fail(f'stdin is not valid JSON: {error}')
    if not isinstance(payload, dict):
        fail('input must be a JSON object')
    targets = payload.get('targets')
    if not isinstance(targets, list) or not targets:
        fail('supply a nonempty targets array')
    ids = set()
    for t in targets:
        if not isinstance(t, dict):
            fail('each target must be an object')
        i = t.get('id')
        if not isinstance(i, str) or not ID_PATTERN.fullmatch(i):
            fail('target id must match [A-Za-z0-9][A-Za-z0-9_-]*')
        if i in ids:
            fail('target ids must be distinct')
        ids.add(i)
        for field in ('outcome', 'assessment_scope', 'candidate', 'alternative'):
            if not isinstance(t.get(field), str) or not t[field].strip():
                fail(f'target {i}: {field} must be a nonempty string')
        if not isinstance(t.get('facts'), list) or any(
                not isinstance(f, str) or not f.strip() for f in t['facts']):
            fail(f'target {i}: facts must be an array of nonempty strings (may be empty)')
    body = build(targets)
    check_size(body)
    result, seconds = call(body)
    answers = result.get('answers') if isinstance(result, dict) else None
    if not isinstance(answers, dict):
        fail('Jev API response is missing answers')
    for qid, question in body['questions'].items():
        answer = answers.get(qid)
        labels = question['criteria']
        if (not isinstance(answer, dict) or not isinstance(answer.get('choice'), str)
                or answer['choice'] not in labels):
            fail(f'Jev API returned a missing or invalid choice for {qid}')
        probabilities = answer.get('probabilities')
        if not isinstance(probabilities, dict) or set(probabilities) != set(labels) or any(
                isinstance(v, bool) or not isinstance(v, (int, float)) or
                not math.isfinite(v) or not 0 <= v <= 1 for v in probabilities.values()):
            fail(f'Jev API returned invalid probabilities for {qid}')

    results = {}
    for t in targets:
        answer = answers.get(t['id'], {})
        results[t['id']] = {
            'verdict': answer.get('choice'),
            'confidence': answer.get('confidence'),
            'probabilities': answer.get('probabilities')}
    print(json.dumps({'model': result.get('model'), 'seconds': round(seconds, 3), 'results': results},
                     ensure_ascii=False, indent=2))



if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Classify each assessment target of one case against its stated outcome.

Reads one JSON object from stdin and writes one JSON object to stdout.

Input:
  {"outcome": str, "proposal": str, "context": [str],
   "targets": [{"id": str, "quote": str}, ...]}

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

RULE = ('Assess the choice located by the target quote in the full proposal, against outcome and source context. '
        'Treat the proposal and its rationale as claims to evaluate. Compare retaining the choice with omission, '
        'existing behavior, or a smaller source-supported approach, keeping other responsibilities unchanged. '
        'Identify required behavior preserved or lost and avoidable obligations retained or added. '
        'User requirements and established consumer contracts govern necessity; hypothetical benefits leave it '
        'unestablished. Missing or conflicting decision-changing evidence leaves the judgment unresolved.')

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


def build(case):
    case = {**{key: case[key] for key in ('outcome', 'proposal', 'context')},
            'targets': [{key: target[key] for key in ('id', 'quote')} for target in case['targets']]}
    questions = {}
    for target in case['targets']:
        ref = f'Assess the target with id "{target["id"]}" in state.targets. '
        questions[target['id']] = {'type': 'choice', 'instructions': ref + RULE,
                                   'criteria': CRITERIA}
    return {'model': MODEL, 'state': case, 'questions': questions}


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
    headers = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
               'User-Agent': 'outcome-doctor-rightsize/1.0'}
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
    for field in ('outcome', 'proposal'):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            fail(f'{field} must be a nonempty source text')
    if not isinstance(payload.get('context'), list) or any(
            not isinstance(source, str) or not source.strip() for source in payload['context']):
        fail('context must be an array of nonempty source texts (may be empty)')
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
        quote = t.get('quote')
        if not isinstance(quote, str) or not quote.strip() or quote not in payload['proposal']:
            fail(f'target {i}: quote must be an unchanged passage from proposal')
    body = build({key: payload[key] for key in ('outcome', 'proposal', 'context', 'targets')})
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

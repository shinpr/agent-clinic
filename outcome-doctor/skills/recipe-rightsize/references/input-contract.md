# Input Contract

Send one JSON object with a nonempty `targets` array:

```json
{
  "targets": [{
    "id": "decision-1",
    "outcome": "Required observable results and explicit obligations or prohibitions",
    "facts": ["Source-attributed observations, established consumer needs, or explicitly identified unknowns"],
    "assessment_scope": "Responsibility and coupled changes being judged",
    "candidate": "Locatable proposed behavior and its effect",
    "alternative": "Concrete comparison approach and its effect on the same requirement"
  }]
}
```

Each target compares two approaches to the same responsibility. Use the actual default or existing mechanism when available; establish the effect of omission from the source. Identify uncertain effects in facts. Other responsibilities remain unchanged. The outcome contains what must hold. Put existing mechanisms, proposed means, and statements that a capability is unrequested in facts or candidate. Distinguish a capability being unrequested from the user forbidding it. Keep evaluator labels separate from the request. Facts establish current behavior and consumers; hypothetical benefits remain possibilities in candidate or alternative. Bound implementation claims to inspected code and consumers.

IDs are unique and match `[A-Za-z0-9][A-Za-z0-9_-]*`. The four text fields are nonempty strings. `facts` is an array of nonempty strings and may be empty.

## If the request is too large

The script estimates 64k tokens per request and 32k for state plus the longest question. The estimate is heuristic; the API can still reject a request within it. Condense to decision-relevant evidence, then split into the fewest groups needed while retaining each target's evidence and coupled changes.

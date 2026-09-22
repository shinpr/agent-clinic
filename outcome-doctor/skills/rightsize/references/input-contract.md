# Input Contract

Send the case once, with targets locating its independently retainable choices:

```json
{
  "outcome": "User's own words stating the required outcome and constraints",
  "proposal": "Proposed choices being assessed",
  "context": ["Source location followed by the original relevant document or section"],
  "targets": [{"id": "decision-1", "quote": "Unchanged passage from proposal locating this choice"}]
}
```

Use source statements as the units of extraction, keeping conditions and exceptions attached to the behavior they qualify. Retain what can change the comparison: the required outcome, each choice's changed and retained behavior and decision-changing unknowns. Preserve those elements together; omit material only when its removal leaves the comparison unchanged. Keep the user's requirements in `outcome`, and the author's interpretations and rationale attributed to `proposal`. For `context`, use the existing documents or complete sections establishing the affected behavior and governing requirements. These sources are shared by every target; Jev evaluates the choices and their smaller alternatives against the same record. Read file content into the producer and serialize it directly. Jev receives the text, so a path alone supplies no evidence.

IDs are unique and match `[A-Za-z0-9][A-Za-z0-9_-]*`. `outcome`, `proposal`, and each `quote` are nonempty strings. Each quote must occur in `proposal`; it locates the choice within its full context. `context` is an array of nonempty strings and may be empty.

If the script or API reports an input-size error, split by assessed responsibility, keeping the original passages and governing context needed for each group.

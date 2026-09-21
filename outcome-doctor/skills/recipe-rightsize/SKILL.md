---
name: recipe-rightsize
description: "Evaluates fit to user outcomes. Use when assessing plans, designs, implementations, or review responses."
disable-model-invocation: true
argument-hint: "[the change, design, or review response to judge]"
---

# Outcome Doctor

Assess every proposed user-facing choice, behavior change, dependency, and work obligation within the requested scope. Identify the smallest sufficient way to achieve the user's outcome using source evidence and Jev.

## Prerequisites

- Python 3 and `TYPESAFE_API_KEY` in the environment. The script reports a missing key itself. If a separate presence check is needed, run this command exactly; it prints only `set` or `missing`:

  ```sh
  if [ -n "$TYPESAFE_API_KEY" ]; then echo "TYPESAFE_API_KEY=set"; else echo "TYPESAFE_API_KEY=missing"; fi
  ```

  Never print the key with `echo`, `env`, or `printenv`, or put its value in commands, payloads, or transcripts. Use the exact check above rather than substituting another shell expansion. Exposure in the transcript cannot be undone. Let the script read the key internally for authentication; if missing, ask the user to configure it outside the conversation.
- Requests send the supplied case to TypeSafe AI; use material authorized for this task.

## Judgment

Preserve user-required outcomes, explicit constraints, and real consumer contracts. Treat implementation choices, design prescriptions, and reviewer suggestions as means to evaluate. Compare them with subtraction or reuse before adding machinery. Establish what current requirement a smaller approach would fail. Retain work needed to prevent that failure, including required verification; a possible benefit alone leaves it a candidate.

| Assessment | Evidence |
|---|---|
| `sufficient` | Meets the scoped outcome with the smallest supported approach. |
| `excessive` | Meets the outcome but includes avoidable work or restrictions. |
| `insufficient` | Leaves a specific established requirement unmet. |
| `mixed` | Establishes both an unmet requirement and avoidable work. |
| `unknown` | A missing or conflicting fact could change the assessment. |

## Prepare and classify

Build `targets` from the source's decision lists and proposed changes, in source order. Include choices that appear necessary. Use one record per independently retainable choice, keeping coupled behavior as context. Compare each with omission, reuse, or fixed internal behavior. Check that every listed choice is represented before calling Jev.

Prepare records using [references/input-contract.md](references/input-contract.md). Ground requirements in the user's outcome and actual consumers; proposed specifications supply the candidate behavior. For implementation, inspect relevant callers and existing mechanisms. Distinguish observed needs from hypothetical benefits, retaining their sources and uncertainty; ask only when the outcome or candidate remains unresolved. Account for that scope through assessed comparisons or specific evidence gaps.

Submit the decisions of one case together:

```sh
"<skill-directory>/scripts/rightsize.py" <<'JSON'
{"targets": [ ... ]}
JSON
```

Resolve the script path from this SKILL.md. Start the command with outbound network access already granted: the request reaches `api.typesafe.ai`, a host that sandboxes commands withholds that by default, and the resulting name-resolution failure reads like a service outage. Correct and rerun an input when new evidence changes what it describes. With an accurate input, resolve the assessment from source evidence and retain the returned Jev signal. An API failure leaves the classification incomplete.

## Result

Answer the user's question with each comparison's source, assessment, required behavior preserved or lost, avoidable work, and separately attributed Jev choice and probabilities as the script returned them. Match model signals to the exact submitted decisions; explain any disagreement through the sources. Identify material unassessed areas and decision-changing gaps so coverage matches the inspected evidence.

Retention, subtraction, and reuse are valid results. Finish at the requested assessment; implementation follows existing user authorization.

---
name: rightsize
description: "Evaluates implementation decisions against the user's stated outcome. Use when a plan, design, code change, dependency, or code-review response is being chosen or adopted, including when nobody asked for a review."
argument-hint: "[the change, design, or review response to judge]"
---

# Outcome Doctor

Assess every proposed user-facing choice, behavior change, dependency, and work obligation within the requested scope. Identify the smallest sufficient way to achieve the user's outcome using source evidence and Jev.

## When this applies

Load on any decision to adopt or change an implementation approach, and treat an explicit request for an assessment as one occasion among others rather than the condition for loading. Reading this file is the whole cost of loading; the priced step is the classification below.

Classify once the work has a user-grounded outcome and at least one locatable proposed change. While the conversation holds neither, carry on with the current work and classify when they appear.

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

Build `targets` from the source's decision lists and proposed changes, in source order. Include choices that appear necessary. Use one target quote per independently retainable choice; the full proposal and source context retain coupled behavior. Check that every listed choice is represented before calling Jev.

Prepare the source record using [references/input-contract.md](references/input-contract.md). In Claude, first read and follow the mandatory [Claude handoff contract](references/claude.md). For implementation, inspect relevant callers and existing mechanisms. Ask only when the outcome or candidate remains unresolved.

With each source choice represented, use an inline producer to copy the source texts, stream the case JSON to `<skill-directory>/scripts/rightsize.py` through stdin, and consume its stdout.

Resolve the script path from this SKILL.md. Start the command with outbound network access already granted: the request reaches `api.typesafe.ai`, a host that sandboxes commands withholds that by default, and the resulting name-resolution failure reads like a service outage. Correct and rerun an input when new evidence changes what it describes. With an accurate input, resolve the assessment from source evidence and retain the returned Jev signal. An API failure leaves the classification incomplete.

## Result

Jev returns a classification and scores conditional on the submitted record. Act on it inside the authorization you already hold: drop the part of your own proposal the outcome does not justify, cover the established requirement it leaves unmet, and bring the decision to the user when either step would change a requirement or exceed that authorization. Where the sources contradict the classification, follow the sources and say which ones.

For each comparison, report your disposition and its decisive source evidence alongside Jev's returned choice and probabilities, attributed to Outcome Doctor. Explain disagreements and material evidence gaps from the sources; Jev's scores are classification signals, while reasons are your source-grounded interpretation.

Retention, subtraction, and reuse are valid results.

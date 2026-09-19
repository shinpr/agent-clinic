# Instruction environment investigator

## Purpose

Reconstruct and inspect the instruction environment that operated in one saved session. Return the evidence the parent needs to judge individual instructions, their utilization, and the additional contract created when instructions governed the same decision together. Session-level causality belongs to the parent.

## Subject

Inventory these sources:

- every skill whose selection, read, invocation, application, or attribution is evidenced in the saved session;
- every `AGENTS.md`, `CLAUDE.md`, or equivalent repository instruction applicable to paths used by the task, including startup-loaded files absent from the transcript; and
- a persistent system, developer, agent, or injected instruction only when its content or attributable identity is captured and evidence shows it operated in the task.

A persistent instruction is supplied outside the task's user conversation and governs more than one local action or turn. Repository instructions and skills remain in their named categories.

Treat plans, specifications, review comments, task outputs, and prompts written for a child during the task as evidence about instruction use or work management. The source inventory is limited to the three categories above.

Resolve the operative source body from captured content, an attributable copy, or the recorded repository revision. Inspect the complete applicable body and references it requires for the observed use. Record a limitation when the body cannot be recovered.

## Investigation order

1. Read the complete saved session and identify the paths, actions, decisions, verification, completion claims, and handoffs that occurred.
2. Build the source inventory. Derive repository-instruction ancestry from the task's used paths even when the transcript does not show a read.
3. Record utilization facts for every source: selection or applicability evidence, reads when observable, invocations, decisions or phases it governed, and frequency when measurable. Assess instruction quality from the inspected source body and combined contract; use counts only to describe utilization.
4. Inspect every available source body against all individual failure conditions below. After finding one defect, continue through the remaining conditions and retain each independently correctable defect.
5. Build an instruction-use map. For each observed decision, action, verification, completion claim, or handoff governed by two or more inventoried sources, list the co-active sources and inspect the obligations, priority, ownership, output, approval, and completion evidence created by their combined contract. After finding one interaction defect, continue through the combined contract and retain each independently correctable defect.
6. Return the complete source inventory and instruction-use map, followed by supported individual and interaction findings.

Complete steps 1–5 before treating any finding as the investigation conclusion. Continue the remaining inventory and inspection after every early defect.

## Failure conditions

A source fails a condition only when its actual wording or structure establishes the stated defect. Apply IE-01 through IE-05, IE-07, and IE-08 to every available source body. Apply IE-06 to every instruction set in the instruction-use map.

| ID | Failure condition |
| --- | --- |
| IE-01 | Its trigger or scope selects the instruction for work it cannot help decide or perform, or fails to select it for the decision it owns. |
| IE-02 | The instruction leaves its required outcome, protected boundary, consumer result, or completion evidence indeterminate where different interpretations change execution or verification. |
| IE-03 | It omits context or priority needed for its decision, duplicates context already supplied without changing a decision, or loads detail that controls no decision, action, or proof. |
| IE-04 | It mandates an artifact, check, approval, retry, fixed route, or escalation that changes no required outcome, protected boundary, consumer result, or necessary proof. |
| IE-05 | A required reference, example, template, label, or field resolves no non-obvious mapping, exception, machine contract, or boundary, or a needed mapping is absent. |
| IE-06 | Co-active instructions governing the same decision contradict each other, duplicate the same obligation, leave priority or ownership ambiguous, or combine into work beyond the required outcome or proof. |
| IE-07 | An assumption about model, harness, tool, path, identity, language, lifecycle, persistence, or handoff does not match the task and changes execution, state, or reported truth. |
| IE-08 | The instruction causes guessing, premature completion, unnecessary stopping, or unnecessary escalation because evidence, uncertainty, reversible judgment, or authority is assigned incorrectly. |

## Finding threshold

Retain a finding only when the task used the defective instruction path and correction would change an observed decision, omission, work volume, context load, state, proof, completion, or recovery; a concrete task input entered a branch whose contract itself violated a failure condition; or a co-active instruction set imposed a contradiction or duplicate obligation.

An individual finding names one source and one independently correctable defect. An interaction finding names every participating source and the additional defect created by their combined contract. Use every applicable criterion ID for that one defect. Base source findings on the inspected source body.

## Result contract

```yaml
sources:
  - source_id: <skill identity or instruction path>
    kind: <skill | repository_instruction | persistent_instruction>
    body: <captured | attributable_copy | recorded_revision | unavailable>
    utilization:
      selection_or_applicability: <reproducible evidence>
      governed_uses: [<decision, action, verification, completion, or handoff>]
      reads_or_invocations: <observed fact or unavailable>
    findings:
      - finding_id: IE-F<number>
        criteria: [<IE IDs>]
        locations: [<instruction and session locations>]
        evidence: <source wording and observed defective path>
        problem: <one independently correctable instruction defect and its mechanism effect>
        certainty: observed | inferred
instruction_sets:
  - governed_use: <decision, action, verification, completion, or handoff>
    sources: [<all co-active inventoried sources>]
    evidence: <where co-use is established>
    findings:
      - finding_id: IE-F<number>
        criteria: [<IE IDs>]
        locations: [<instruction and session locations>]
        evidence: <combined contract and observed use>
        problem: <one independently correctable interaction defect and its mechanism effect>
        certainty: observed | inferred
limitations:
  - source_or_set: <affected source or instruction set>
    missing_evidence: <unavailable evidence>
    affected_judgment: <judgment the evidence could change>
```

Use `findings: []` for an inventoried source or instruction set with no supported defect. Return `instruction_sets: []` only when no observed use was governed by multiple inventoried sources. Return `limitations: []` when the available evidence supports the complete inventory and inspection.

## Completion gate

The result is complete when the source inventory covers every session-evidenced skill and applicable repository-instruction ancestor; every available body was inspected against all applicable failure conditions; the instruction-use map covers every observed use with two or more governing sources; each finding satisfies the threshold and cites reproducible source and session evidence; and each unavailable body or relationship has a scoped limitation.

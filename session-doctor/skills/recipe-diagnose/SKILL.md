---
name: recipe-diagnose
description: "Diagnoses one Claude Code or Codex session across user utterances, work management, and the operative instruction environment. Use when: an agent session was incomplete, wasteful, or behaved unexpectedly."
disable-model-invocation: true
argument-hint: "[session-id-or-transcript]"
---

# Session Doctor

Diagnose one Claude Code or Codex session through three independent investigations:

1. **User utterances**: evaluate how every user message requested, delegated, changed, corrected, authorized, or closed work.
2. **Work management**: evaluate how the user and agent planned, assigned, tracked, verified, and completed the work, including subagent operation.
3. **Instruction environment**: evaluate the skills, repository instructions, and attributable persistent instructions defined by the investigator, including utilization and combined contracts.

The parent acts as the diagnostic decision-maker and verifier. Fresh ordinary subagents apply one self-contained axis rubric each. This separation keeps an early finding in one axis from narrowing evidence collection in the other axes. The parent establishes each investigation boundary, treats child conclusions as evidence, accepts, returns, or discards that evidence, determines causal relationships and responsible corrections, and writes an actionable improvement report in the conversation.

## Inputs

Accept a session ID, transcript path, or hints that identify one session. When no selector is supplied, find transcripts associated with the current repository and order them by last recorded activity. Present the most recent candidate's harness, session ID or path, repository, time range when available, initial request, and observed endpoint for confirmation. An exact ID or path permits analysis after presenting the same summary.

Proceed when one session and its repository or available environment sources can be identified. Ask for one missing selector only when it changes the session being analyzed.

## References

The parent reads [references/analysis-criteria.md](references/analysis-criteria.md). Each child reads only its assigned self-contained role definition:

- [references/user-utterance-investigator.md](references/user-utterance-investigator.md)
- [references/work-management-investigator.md](references/work-management-investigator.md)
- [references/instruction-environment-investigator.md](references/instruction-environment-investigator.md)

After the child results return, the parent uses the three role definitions to validate their criterion sets and subject boundaries.

Read the session-access reference for the diagnosed session's harness:

- [references/claude-code-session-access.md](references/claude-code-session-access.md)
- [references/codex-session-access.md](references/codex-session-access.md)

Read the delegation reference for the harness currently running Session Doctor:

- [references/delegation-claude-code.md](references/delegation-claude-code.md)
- [references/delegation-codex.md](references/delegation-codex.md)

Each Agent prompt consists of the fixed task sentence and canonical fields below. Populate each field by copying its resolved value.

```text
Investigate the saved session according to ROLE_DEFINITION_PATH and return the complete result defined there for the parent to verify and synthesize.
SESSION_SOURCE: <resolved session or transcript path>
REPOSITORY_ROOT: <attributable repository root or unavailable>
ROLE_DEFINITION_PATH: <absolute path to the assigned investigator file>
```

Read [references/report-template.md](references/report-template.md) after all three child results return.

## Investigation

1. Resolve the saved session source and attributable repository root with the target-harness access reference.
2. Mechanically serialize the input contract, then use the host-harness delegation reference to launch the three investigators in parallel. Input preparation ends when the three paths are populated; investigation begins in the assigned children.
3. Receive all three results and apply `analysis-criteria.md`. Compare each audit map with the session and environment, return incomplete investigation to the same child, and disposition every finding.
4. Verify the facts and causal relationships used in synthesis, select corrections at the responsible axis, and write the report.

Session outputs can support or contradict a diagnosis. The diagnostic subjects and correction owners remain user utterances, work management, or the instruction environment.

## Report

Follow [references/report-template.md](references/report-template.md). Include every accepted issue, whether it directly caused an observed failure, amplified it, or was an independently demonstrated defect in the task's operating mechanism. Report model identity only from explicit metadata.

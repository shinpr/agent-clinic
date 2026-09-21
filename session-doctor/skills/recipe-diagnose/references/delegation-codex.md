# Codex delegation

Use this reference when Session Doctor is running in Codex, regardless of the diagnosed session's harness.

Launch three ordinary `default` subagents in parallel with `fork_turns="none"`, one for each investigator definition. Start all three before waiting. While an investigator is running, continue receiving through `wait_agent`; parent intervention begins after its terminal result is available for acceptance.

When `analysis-criteria.md` returns a result for missing investigation, use `followup_task` on the same task, provide only the unmet condition, and wait for the corrected terminal result.

# Session Doctor report contract

Return the report in the conversation. Preserve product names, harness names, paths, IDs, and commands.

```markdown
# Session Doctor Report

## Target

- Harness: Claude Code | Codex
- Session: <ID or transcript name>
- Model: <explicitly recorded model or unavailable>
- Repository: <repository or unavailable>
- Scope: <one-sentence session scope, naming independent tasks when more than one occurred>

## Conclusion

<State what failed in the operating mechanism and how the three axes related.>

## Principal Issue

<State the dominant mechanism or interaction.>

## Issues

| ID | Relationship | Axis | Evaluation unit | Correction owner | Problem and effect |
| --- | --- | --- | --- | --- | --- |
| F-1 | Direct cause / Amplifying cause / Independent mechanism defect | User utterances / Work management / Instruction environment | Individual / Interaction | <responsible utterance, management boundary, or instruction sources> | <mechanism defect and material effect> |

## Details

### F-1: <finding title>

- **Relationship:** <causal classification>
- **Axis:** <one diagnostic axis>
- **Evaluation unit:** <individual or interaction>
- **Correction owner:** <responsible utterance, management mechanism, one instruction source, or every source in the interaction>
- **Criteria:** <failed criterion IDs>
- **Problem location:** <reproducible transcript and/or environment locations>
- **Observed problem:** <one independently correctable mechanism defect and its material effect>
- **Correction direction:** <smallest sufficient correction at the responsible owner>
- **Certainty:** <observed or inferred>

## Evidence Limitations

<Missing evidence that could change a finding, causal relationship, or correction owner.>
```

Order findings by direct cause, amplifying cause, then independent mechanism defect, and within each relationship by axis: user utterances, work management, instruction environment. Use the same order in the issue table and the detail sections. Give every reported finding one detail section. Limit the report to the direct and amplifying causes only when the diagnosis was explicitly requested for the causes alone. Grouping may change headings while preserving the concrete facts of every finding. For an instruction interaction, use `Interaction` and list every participating source. Use task outputs only as concise evidence. State each correction as a change to user wording, work-management behavior, or persistent instructions.

When no finding is accepted, return `Target` and `Conclusion`, plus `Evidence Limitations` when material evidence is unavailable. State that the available evidence established no mechanism defect.

The report serves a reader who has no prior conversation and will change the operating mechanism. Each finding therefore identifies the correction owner, exact problem location, failed criterion, observed mechanism and effect, and correction direction. Limit advice to corrections supported by accepted mechanism defects.

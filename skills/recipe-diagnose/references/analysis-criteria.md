# Parent acceptance and synthesis criteria

The parent owns the diagnosis. Child results are scoped investigation evidence; the parent verifies their coverage and claims, decides which findings survive, establishes causal relationships, and produces a report that can be used to improve the operating mechanism.

## Finding standard

An accepted finding identifies a failure in user wording, work management, one persistent instruction, or a combined instruction contract. Its evidence establishes the named failure condition and one of these material effects:

- correction would change an observed decision, omission, work volume, context load, state, proof, completion, or recovery;
- the task entered a defective instruction or management branch whose contract itself failed the criterion; or
- co-active instructions imposed a contradiction or duplicate obligation.

Task outputs may prove a mechanism failure. The correction owner remains one of the three diagnostic axes.

## Acceptance order

Apply this order to each child result.

1. **Coverage:** Compare the returned audit map with the saved session and assigned role definition.
   - User utterances cover the complete user-message sequence and every state-changing message.
   - Work management traces every accepted work unit to a terminal state. Its continuity map contains every explicit compaction, handoff, retry, and resumption marker in the saved session at the recorded locations.
   - Instruction environment lists every session-evidenced skill, every repository-instruction ancestor applicable to used paths, and every attributable persistent instruction. Its instruction-use map lists each observed use governed by two or more inventoried sources.
   - Return the same child with the missing history, unit, source, relationship, or criterion. Provide only the unmet condition and evidence location.
2. **Evidence:** Reproduce the cited wording, state transition, source content, applicability, and effect. Return the child result when an in-axis claim omits available evidence. Record a scoped limitation when the required evidence is unavailable.
3. **Axis and owner:** Keep findings whose subject and correction owner match the assigned axis. For a user-utterance finding, verify whether the responsible agent could resolve the referent from accepted work, external state, or prior evidence; route failures to maintain or recheck that state to work management. Discard a task-output judgment or a finding owned by another axis.
4. **Criterion:** Compare the evidence with the named failure condition in the role definition. When available evidence presents an in-scope failure the child left unevaluated, return the exact criterion and evidence location. Return a finding that combines defects with different correction owners or independently applicable corrections. Discard a finding when the condition is not established.
5. **Material effect:** Apply the finding standard above. Discard wording preferences, possible defects in unused branches, counts alone, technical possibilities, and no-effect duplication.

Before synthesis, create one internal disposition row for every child `finding_id`: `accepted`, `returned`, or `discarded`, with the criterion and evidence that justify the decision. Use `axis_or_owner_mismatch`, `criterion_not_established`, or `material_effect_not_established` as the discard reason. Resolve returned investigation before synthesis. The parent adopts a child conclusion only after inspecting the session or environment evidence needed to verify it.

Accept every independently correctable finding that passes the five checks. Use causal relevance, severity, report length, readability, and overlap only for later classification, ordering, or grouping.

## Synthesis

After all three results pass coverage or have scoped evidence limitations:

1. Classify every accepted finding as:
   - **Direct cause:** changed a decision or state transition that produced an observed failure.
   - **Amplifying cause:** increased the likelihood, extent, concealment, work, or recovery cost of an observed failure.
   - **Independent mechanism defect:** materially failed its axis criterion in this task without an established causal chain to the principal failure.
2. Verify causal claims against the session. Keep observed and inferred relationships distinguishable.
3. Preserve each accepted finding once. Group related findings for navigation only when every source, criterion, location, problem, effect, owner, and correction remains explicit.
4. Select the smallest sufficient correction at the responsible axis: remove an unnecessary mechanism, reuse or consolidate an existing mechanism, then narrow or correct it. Child fix suggestions are candidates rather than requirements.

## Completion gate

The diagnosis is ready when:

- the three audit maps satisfy their role completion gates or name scoped evidence limitations;
- every child `finding_id` appears exactly once in the disposition rows, and every accepted row appears exactly once in the report;
- every accepted finding satisfies axis, evidence, criterion, and material-effect checks;
- every accepted finding appears once in the report with enough information to locate and correct it;
- individual and interaction instruction findings remain distinguishable and name their sources;
- causal classification occurs after acceptance and distinguishes observation from inference; and
- every correction targets user wording, work management, or the persistent instruction environment; and
- the rendered report contains every field required by `report-template.md` in its issue table and detail sections.

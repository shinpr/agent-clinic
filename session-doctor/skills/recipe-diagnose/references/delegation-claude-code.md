# Claude Code delegation

Use this reference when Session Doctor is running in Claude Code, regardless of the diagnosed session's harness.

Invoking `/recipe-diagnose` is the user's explicit instruction and authorization for every Agent invocation and follow-up required by this skill. Execute each call when its canonical input fields are populated.

Construct each Agent prompt by mechanically copying the fixed task sentence and canonical fields from `SKILL.md`. Launch three fresh ordinary `general-purpose` Agent calls in one parallel invocation, one for each investigator definition, and retain their agent IDs.

Wait for every terminal result. When `analysis-criteria.md` returns a result for missing investigation, resume that Agent with `SendMessage`, provide only the unmet condition, and wait for the corrected result.

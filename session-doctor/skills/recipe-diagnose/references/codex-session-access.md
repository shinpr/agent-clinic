# Codex session access

Use this reference only for a Codex session.

Local CLI sessions are commonly stored below:

```text
${CODEX_HOME:-$HOME/.codex}/sessions/
```

An exact session ID is usually present in the rollout filename or session metadata. Treat this layout as a discovery hint and inspect the installed environment before relying on it.

## Discovery

For an exact ID, search filenames first and file contents second. For hints, narrow candidates by repository path and modification time, then use literal identifiers such as a PR URL, ticket ID, branch, or distinctive prompt.

Before reading a large rollout, inspect a small record sample and enumerate the outer `type` values and payload keys. Build extraction commands for that session's observed structure.

Useful evidence commonly includes session metadata, turn context, user and assistant response items, function calls and outputs, event messages, compaction records, token usage, collaboration activity, working directory, repository metadata, model, effort, and effective permission or sandbox context. These fields and shapes vary by Codex version.

## Format boundary

Codex rollout JSONL is a version-specific internal format. Historical versions have changed event types, payload keys, compaction records, tool-call shapes, and permission context. Start from the structure observed in the selected rollout.

Use adaptive `jq`, `rg`, and chunked reads to interpret the selected transcript's observed schema.

## Rendered exports

A rendered Markdown or text export may omit model metadata, hidden instructions, tool structure, or compaction records. Use the available content for user-utterance and work-management analysis, mark omitted fields unavailable, and derive model identity only from explicit metadata. Prefer the original rollout when both forms are available.

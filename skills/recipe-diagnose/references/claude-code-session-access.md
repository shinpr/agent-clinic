# Claude Code session access

Use this reference only for a Claude Code session.

Claude Code CLI transcripts normally live under:

```text
${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<project>/<session-id>.jsonl
```

Desktop, web, and IDE histories may be stored separately. When local evidence does not establish how the installed version stores or exports sessions, consult current official Claude Code documentation. When the requested session remains inaccessible, ask for `/export` output or the transcript file and classify local availability as unknown.

## Discovery

For an exact ID, search filenames below the effective Claude config directory. For hints, narrow by project directory and modification time, then search candidate files for stable literal hints such as a PR URL, ticket ID, branch, or distinctive initial request.

Start extraction from a small record sample and its observed top-level keys and `type` values. Build queries for that file's structure.

Useful evidence commonly includes user and assistant messages, tool-use blocks and results, timestamps, working directory, version, model metadata when explicitly recorded, compaction summaries, skill attribution, and child-agent markers. Field availability varies.

## Format boundary

The JSONL entry format is internal to Claude Code and changes between releases. Treat paths and example fields as discovery hints, derive extraction from the observed structure, and use adaptive `jq`, `rg`, and chunked reads.

`/export` is the stable human-readable option when the local JSONL is unavailable or insufficient.

Official maintenance reference: https://code.claude.com/docs/en/sessions#export-and-locate-session-data

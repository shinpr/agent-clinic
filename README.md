# Agent Clinic

![Agent Clinic banner](docs/assets/agent-clinic-banner.jpg)

Plugins for diagnosing agent sessions. Currently ships one: **Session Doctor**.

It looks back at one of your past Claude Code or Codex sessions and tells you what to change.

Sessions go wrong for boring reasons. A request with no "done" condition. A task that quietly vanished at a compaction. A skill that overrode one of your own rules. Session Doctor reads the saved transcript and looks for problems like these:

- **What you asked for**: where the request left the outcome, scope, or "done" undefined.
- **How the work was run**: work the agent started but never finished, state lost during compaction, subagent results that were never checked.
- **What was instructing the agent**: your skills, `AGENTS.md` and `CLAUDE.md` as they actually combined in that session, including rules that conflict or duplicate each other when they apply at the same time.

The three passes run separately, so a hunch from the first does not bias the other two. The report shows what went wrong, where it happened, and the smallest change likely to prevent it next time.

## Install

Claude Code:

```text
/plugin marketplace add shinpr/agent-clinic
/plugin install session-doctor@agent-clinic
```

Codex:

```sh
codex plugin marketplace add shinpr/agent-clinic
codex plugin add session-doctor@agent-clinic
```

Start a new session afterwards so the skill is loaded.

## Use

```text
/recipe-diagnose   # Claude Code
$recipe-diagnose   # Codex
```

The examples below use the Claude Code form.

The place to start is the session that just went sideways. Run it with no argument: it finds the most recent session for the current repository and asks you to confirm it before analysing. You can also name one directly:

```text
/recipe-diagnose look at session 01af3c2e-...
/recipe-diagnose the session in ~/.claude/projects/my-repo/01af3c2e-....jsonl
```

The argument is plain language, not a fixed syntax. Installed in either host, it reads both Claude Code and Codex transcripts.

By default the report covers every problem it can back with evidence. If you want it limited to the problems that contributed to the failure, say so. "Just the root causes" is enough.

### Picking the session

You rarely need an ID. Tell it roughly when the session ran and what you were working on, and it searches the saved transcripts for a match. It confirms with you before it starts:

```text
/recipe-diagnose the session last night where the test suite kept half-passing
```

When you already know which session you want:

- **Read its ID**: open the session and run `/status`. Both CLIs show the ID, as do the Code tab in the Claude desktop app and Codex in the ChatGPT app. Copy it, then start Session Doctor in a different session and give it that ID.
- **Drag it in**: in the ChatGPT app, switch to Codex and drag the session's title from the sidebar into the chat box. The title goes in as a chip that points at that session.

## What it will not do

It does not review your code or rewrite anything. It reports the diagnosis and leaves the fixes to you.

## License

MIT

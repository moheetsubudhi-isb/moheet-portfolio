# The tool registry

Once an agent has more than about three tools, it starts guessing. It searches the web for
something sitting in your own files. It opens a spreadsheet to answer a question the database
answers properly. It proposes a plan built on access it doesn't have.

**The registry is the file that tells it which tool for which kind of question — and which ones
to ignore.** Four lines of yours saves it ten wrong guesses.

It does two jobs, which is why it's worth writing even if you've connected nothing:

- **With tools connected** — it stops the agent reaching for the wrong one.
- **In a plain chat with no tools at all** — it tells the model what access *you* have, so it
  stops suggesting things you can't do and starts asking you for what it needs.

**The second half is the limits.** A connector runs as you: it usually gets whatever your login
gets, so it can send, edit and delete. Write down what it may only read, what it must bring back
to you before it acts — that's **human in the loop** — and what it must never touch.

A written rule guides it; it doesn't lock anything. For the risky actions, also set the tool
itself to ask before it acts. It drafts, you press send.

---

## The template

```
# What you can reach

[source] — [what kind of question it answers. Be specific about the kind.]
[source] — [...]

# Reach for first

When more than one could work, use [source], because [reason].
Only go to [other source] when [condition].

# Don't bother with

[thing that looks relevant and isn't] — [why not]
[thing that is out of date] — [use this instead]

# Things you cannot reach

[what you don't have access to] — ask me and I'll paste it.

# What it may do

Read only: [sources it may read but never change]
Human in the loop: [actions it drafts and I approve first — sending, editing]
Never: [what it must not touch at all]

# Keep this current

If I tell you twice to use a different source than the one you picked, add
that to this file before you finish.
```

**"Don't bother with" is the half that earns its keep.** Anyone can list their tools. Only you
know which folder is abandoned, which dashboard nobody trusts, and which export is always two
days behind.

---

## Filled example · someone in data and BI

```
# What you can reach

Warehouse (read-only) — anything about actual numbers: volumes, revenue, counts
  by period. This is the source of truth. If it disagrees with a deck, the
  warehouse is right.
`/reports` folder — the monthly packs I've already sent out. Good for "what did
  we say last month" and for matching the format. Not good for numbers.
`/raw` folder — vendor CSV drops. Unvalidated, duplicated, inconsistent headers.
  Only when the warehouse genuinely doesn't have the field.
Web search — public market and competitor context only. Never for our numbers.

# Reach for first

Any question with a number in the answer: warehouse, always, even when a file
in /reports looks like it already has it.
Any question about wording, format or what we committed to: /reports.

# Don't bother with

The dashboard — it's behind a login you can't reach, and the definitions
  drifted last quarter. Ask me for a screenshot instead.
Anything in /raw dated before this year — superseded, kept only for audit.
Searching the web for our own figures. It isn't there and you'll find
  somebody else's.

# Things you cannot reach

The CRM, and anything with customer names in it. If you need it, say what you
need and I'll paste a redacted extract.

# What it may do

Read only: the warehouse, /reports, /raw.
Human in the loop: anything that sends, publishes or overwrites. Draft it,
  show me, wait for my yes.
Never: delete files, or write to the warehouse.

# Keep this current

If I tell you twice to use a different source than the one you picked, add
that to this file before you finish.
```

---

## The plain-chat version

No connected tools, nothing installed, just a chat window. Still worth thirty seconds:

```
You have no tools. You can only see what I paste into this chat. So:

- Never tell me to "check the file" or "look at the dashboard". You can't.
- When you need data, ask me for the smallest specific thing that would answer
  it — a column, a row, a number — not "can you share the dataset".
- If your answer depends on something you can't see, say so in one line at the
  top rather than guessing and carrying on.
- Anything I paste is a snapshot. If it's older than the question, say so.

Here is what I can get you if you ask: [your warehouse / your CRM / last
month's pack / nothing, I'm on my phone].

If I correct you on any of this, show me the whole block again
with the fix in it, from its first line, so I can paste it back.
```

That last line is the whole trick. It turns "I don't have access to your data" into "ask me and
I'll fetch it."

---

## Where the tools come from — MCP servers

MCP is the standard that lets one agent talk to many tools without a custom integration each
time. A **server** is one tool's side of that: Gmail, GitHub, Postgres, Notion, your own API.

**Where to look, in this order:**

| Where | What it is |
|---|---|
| **Built in** | The connector list inside Claude and ChatGPT. Click to connect. Start here. |
| **The vendor's own** | First-party servers from the companies themselves — GitHub, Notion, Stripe, Supabase. Always check here first. |
| [Composio](https://composio.dev) | One connection, hundreds of apps, and it handles the OAuth for you. The shortcut if you don't want to manage auth. |
| [mcp.so](https://mcp.so) | The big browsable public directory. Everything's there, which is also the problem. |
| [best-of-mcp-servers](https://github.com/tolkonepiu/best-of-mcp-servers) | 400+ servers *ranked*, updated weekly. Use this when you don't know what you're looking for. |
| **Your own** | Ask your agent to build one around your own system. |

Also maintained: [abordage/awesome-mcp](https://github.com/abordage/awesome-mcp) — servers,
clients and frameworks, updated daily.

### Four questions before you install one

An MCP server runs on your machine with your credentials. That is the entire security model,
so ask:

1. **Who wrote it?** The vendor, or a stranger? A first-party server from the company whose API
   it wraps is a different proposition from a weekend fork.
2. **What is it asking for?** Read-only or write? Scoped to one repo, or your whole account?
   If it wants write access to do a read job, that's your answer.
3. **When was it last touched?** An MCP server that hasn't been updated in six months is
   tracking a spec that moved.
4. **What happens if it's lying?** Assume it can see everything you point it at. Decide whether
   you'd be fine with that before you connect it, not after.

**Start with one.** One connector you understand beats eight you installed in an evening and
can't name.

---

## Stack it

[Soul file](02-soul-files.md) — who it is. **This file** — what it can reach.
[Loop checklist](03-loop-checklist.md) — how it works. A skill — how you do one task.
[Making it remember](08-make-it-remember.md) — how they stop rotting.
[The generator](01-generator-prompt.md) fills the first four in, in your words, in five minutes.

**Where it goes:** into your `AGENTS.md` alongside the soul file, which is the filename most
terminal agents read. In a chat window, the plain-chat version above, pasted at the top.

# How to Build with AI

The take-home page from a session for the AMPBA cohort: a prompt that writes your own
AI setup, five ready-made ones, a loop checklist, a tool registry, and 36 analytics
skills. Plain text, nothing to install, works on a phone.

Live at https://moheetsubudhi-isb.github.io/build-with-ai/

## Rebuilding

`index.html` is generated, not hand-edited. Every copyable block is pulled from the
markdown in the session's `giveaways/` folder at build time, so the page cannot drift
from the files it hands out.

```bash
node extract-art.js   # refresh the diagrams from the deck (writes art.json)
python3 build.py      # rebuild index.html
```

Diagrams come from the session deck and are recoloured for the paper theme.
Icons are [Phosphor](https://phosphoricons.com) (MIT), inlined at build time so the
page needs no CDN for them at runtime.

#!/usr/bin/env python3
"""Build index.html from the giveaway markdown, so the page cannot drift from the files.

  node extract-art.js     refresh the deck's diagrams (art.json)
  python3 build.py        rebuild index.html

Paper theme. A poster of numbered objects; clicking one opens it as its own
scrollable view. Everything the visitor copies is pulled from giveaways/*.md at
build time, never retyped here.
"""
import html as H
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
GIVE = HERE / "giveaways" if (HERE / "giveaways").is_dir() else HERE.parent / "giveaways"
REPO = "https://github.com/moheetsubudhi-isb/business-analytics-skills"


def read(name):
    return (GIVE / name).read_text(encoding="utf-8")


def between(txt, a, b):
    return txt.split(a)[1].split(b)[0].replace("```", "").strip()


def content():
    c = {}
    c["generator"] = between(read("01-generator-prompt.md"),
                             "===== COPY FROM HERE =====", "===== COPY TO HERE =====")
    souls = read("02-soul-files.md")
    c["souls"] = [{"name": m.group(1).strip(), "body": m.group(2).strip()}
                  for m in re.finditer(r"^## \d+ · (.+?)\n+```\n(.*?)\n```", souls, re.S | re.M)]
    loop = read("03-loop-checklist.md")
    c["loopChat"] = between(loop, "===== COPY FROM HERE =====", "===== COPY TO HERE =====")
    c["loopFile"] = re.search(r"Then the block:\n+```\n(.*?)\n```", loop, re.S).group(1).strip()
    reg = re.findall(r"```\n(.*?)\n```", read("04-tool-registry.md"), re.S)
    c["regTemplate"], c["regExample"], c["regChat"] = (b.strip() for b in reg[:3])
    c["installClaude"] = ("/plugin marketplace add moheetsubudhi-isb/business-analytics-skills\n"
                          "/plugin install statistics-toolkit@business-analytics-skills")
    c["installCodex"] = "codex plugin marketplace add moheetsubudhi-isb/business-analytics-skills"
    c["installCli"] = "npx skills add moheetsubudhi-isb/business-analytics-skills --list"
    c["ollama"] = "ollama run qwen3:1.7b"
    return c


def art():
    a = json.loads((HERE / "art-light.json").read_text(encoding="utf-8"))
    # The deck drew the loop with its top circle at y=-6 (centre 150, offset -110,
    # radius 45 plus stroke), which the 0-origin viewBox cut off. Give it the room
    # rather than move the drawing.
    a["loop"] = a["loop"].replace('viewBox="0 0 1000 300"', 'viewBox="0 -16 1000 318"', 1)
    return a


def icons():
    """Phosphor Icons, MIT, fetched once by fetch-icons and inlined at build time so
    the page needs no icon CDN at runtime."""
    return json.loads((HERE / "icons.json").read_text(encoding="utf-8"))


LINKEDIN = "https://www.linkedin.com/in/moheetsubudhi/"
WHATSAPP = "https://wa.me/919861379000"
MAIL_USER = "moheetsubudhi"
MAIL_HOST = "gmail.com"


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
/* Every tile for every folder is in the markup and all but one set is hidden.
   A display rule on the element beats the attribute, so say it once, here. */
[hidden]{display:none!important}
:root{
  --paper:#F2EEE3; --paper-2:#EAE4D6; --paper-3:#E2DBC9;
  --ink:#17150F; --muted:#5C574C; --faint:#8C8573;
  --line:rgba(23,21,15,.13); --line-2:rgba(23,21,15,.26);
  --accent:#2F4FD4; --accent-rgb:47,79,212;
  --accent-2:#8094E4; --accent-2-rgb:128,148,228;
  --accent-soft:rgba(var(--accent-rgb),.10);
  --display:'Bricolage Grotesque',ui-sans-serif,system-ui,sans-serif;
  --body:'Hanken Grotesk',ui-sans-serif,system-ui,-apple-system,sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --e:cubic-bezier(.2,.8,.2,1);
  --r:10px;
  --panel:#FAF8F3;     /* the results panel, and so also the wipe that reveals the arrow */
  --rule:29px;          /* the ruling pitch, and the body line-height, so text sits on it */
}
html{-webkit-text-size-adjust:100%;background:var(--paper)}

/* Paper. A fixed, non-interactive overlay so the grain never repaints while
   anything scrolls: fibre speckle, a faint rule, and a soft vignette. */
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
  opacity:.55;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.42'/%3E%3C/svg%3E")}
/* The ruling and the vignette are light on the page, not ink on it: both stay put
   while the content moves over them. Fixed rather than attached, because iOS Safari
   ignores background-attachment:fixed. */
body::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    repeating-linear-gradient(to bottom, transparent 0 31px, rgba(23,21,15,.045) 31px 32px),
    radial-gradient(120% 90% at 50% 40%, transparent 55%, rgba(23,21,15,.07) 100%)}
body > *{position:relative;z-index:1}
@media (prefers-reduced-transparency: reduce){body::before{display:none}}
body{background-color:var(--paper);color:var(--ink);font-family:var(--body);
  line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:820px;margin:0 auto;padding:0 20px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(47,79,212,.3)}
a:hover{border-bottom-color:var(--accent)}
h1,h2,h3{font-family:var(--display);letter-spacing:-.025em}
h1{font-weight:800;line-height:.94;font-size:clamp(38px,min(9vw,10vh),84px)}
h2{font-weight:800;line-height:1.04;font-size:clamp(27px,5.4vw,42px)}
h3{font-weight:600;font-size:clamp(17px,3.4vw,21px);letter-spacing:-.01em}
p{color:var(--muted);font-size:clamp(15px,3.6vw,17px)}
p + p{margin-top:13px}
p strong,li strong{color:var(--ink);font-weight:600}
.lead{font-size:clamp(16px,4vw,19px);max-width:56ch}

/* ---------- the poster ----------
   Objects sit around the title at wide widths, the way a printed poster would lay
   them out. Below 1040px, and whenever a search is running, they fall back to a
   plain grid: a scatter cannot survive a narrow screen or a changing item count. */
/* The poster is exactly one screen: the objects and the contact row share it, so a
   laptop never scrolls to reach either. */
/* One shell: the poster or an opened item, and under either of them the same
   contact bar. Nothing is duplicated, so the bar cannot drift between the two. */
#shell{min-height:100dvh;display:flex;flex-direction:column}
#poster{flex:1;display:flex;flex-direction:column;justify-content:center}
body.open #poster{display:none}
/* The poster fills what the bar and the contact row leave, and centres its own
   contents inside that, so the bar stays at the top of the page. */
#hub{display:flex;flex-direction:column;justify-content:center;
  padding:clamp(12px,2.4vh,28px) 0 clamp(8px,1.2vh,14px);position:relative;flex:1}
#hub.scatter{flex:1}
/* Climbing out of a folder, back to whatever holds it. */
/* A poster inside a folder uses the same bar as an opened item, at the top of
   the page rather than floating over the heading. */
#poster > .topbar{position:sticky;flex:0 0 auto}
#poster > .topbar .inner{max-width:none;padding-left:clamp(14px,3vw,34px);
  padding-right:clamp(14px,3vw,34px)}
@media(max-width:639px){#poster > .topbar .where{display:none}}
/* The heading is a full-width block, so it sits over the objects beside it and
   eats their clicks. It is only text, so it takes no pointer events. */
.poster-title{text-align:center;padding:0 20px;position:relative;z-index:2;
  pointer-events:none}
/* Ink settling: each word arrives slightly late and slightly out of focus,
   then sets. The old heading leaves as one block rather than word by word, so
   the change reads as a relabel and not as two animations fighting. */
@keyframes inkIn{
  from{opacity:0;transform:translateY(9px);filter:blur(7px)}
  to{opacity:1;transform:none;filter:blur(0)}
}
.poster-title h1 .w{display:inline-block;animation:inkIn .38s var(--e) both;
  animation-delay:var(--d,0s)}
.poster-title h1,.poster-title .sub{transition:opacity .16s var(--e),filter .16s var(--e)}
.poster-title h1.out,.poster-title .sub.out{opacity:0;filter:blur(5px)}
.poster-title .sub .w{display:inline-block;animation:inkIn .38s var(--e) both .12s}
@media (prefers-reduced-motion: reduce){
  .poster-title h1 .w,.poster-title .sub .w{animation:none}
}
.poster-title .sub{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint);margin-top:clamp(8px,1.4vh,14px)}
@media(min-width:520px){.poster-title .sub{font-size:11px;letter-spacing:.24em}}
.objects{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;
  max-width:980px;margin:clamp(14px,2.4vh,30px) auto 0;padding:0 14px}
@media(min-width:720px){.objects{grid-template-columns:repeat(4,1fr);gap:10px}}
/* A full folder on a phone goes three across rather than two, so it still fits
   one screen instead of asking for a scroll to see the last row. */
@media(max-width:719px){
  .objects.many{grid-template-columns:repeat(3,1fr);gap:6px;
    margin-top:clamp(10px,1.6vh,20px)}
  .objects.many .obj{padding:5px 4px 7px}
  .objects.many .obj .thumb{max-height:62px;padding:4px}
  .objects.many .obj .label{font-size:12.5px}
}
/* Two or three objects are a row in the middle, not a stripe across the page. */
/* auto side margins on a column flex item shrink it to its content, so the width
   has to be stated or the row collapses */
/* One or two objects centre as a row at the same size as every other tile.
   Scaling them up to fill the space changed the proportion of the icon to the
   card, which is the thing that made the poster read. */
.objects.few{display:flex;width:100%;justify-content:center;
  gap:clamp(12px,2.5vw,26px);max-width:560px}
.objects.few .obj{flex:0 1 200px}
@media(min-width:850px){
  #hub.scatter .objects{display:block;position:absolute;inset:0;max-width:none;
    margin:0;padding:0;pointer-events:none}
  #hub.scatter .obj{position:absolute;width:124px;pointer-events:auto;padding:7px;z-index:3;
    transform:rotate(var(--r))}
  #hub.scatter .obj .label{font-size:13px;line-height:1.15}
  #hub.scatter .obj .thumb{padding:10px}
  #hub.scatter .obj:hover,#hub.scatter .obj:focus-visible{
    transform:rotate(0deg) translateY(-4px) scale(1.04);z-index:4}
  #hub.scatter .obj{cursor:grab;touch-action:none}
  #hub.scatter .obj.dragging{cursor:grabbing;z-index:5;transform:rotate(0deg) scale(1.06);
    filter:drop-shadow(0 10px 18px rgba(23,21,15,.18))}
  #hub.scatter .obj .thumb{aspect-ratio:1/1}
}
.obj{position:relative;display:flex;flex-direction:column;gap:4px;text-align:left;
  background:transparent;border:0;padding:7px 7px 9px;cursor:pointer;
  border-radius:var(--r);transition:transform .22s var(--e),background .22s var(--e);
  font-family:inherit;color:inherit}
.obj:hover,.obj:focus-visible{background:rgba(23,21,15,.045);transform:translateY(-3px)}
.obj:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.obj:active{transform:translateY(-1px)}
.obj .thumb{aspect-ratio:16/11;display:grid;place-items:center;overflow:hidden;
  border-radius:8px;background:var(--paper-2);padding:6px;
  border:1px solid rgba(23,21,15,.07);max-height:clamp(52px,8.6vh,104px)}
.obj .thumb svg{width:100%;height:auto;max-height:100%}
.obj .thumb .ico{width:clamp(30px,38%,52px);height:auto;color:var(--accent)}
.obj .thumb .ico svg{width:100%;height:100%}
.obj .thumb .glyph{font-family:var(--display);font-weight:800;
  font-size:clamp(26px,6vw,40px);color:var(--accent);letter-spacing:-.03em}
.obj .n{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;color:var(--faint)}
.obj .label{font-family:var(--display);font-weight:600;font-size:clamp(13px,3.2vw,15.5px);
  line-height:1.18;letter-spacing:-.01em}
.obj .label .arrow{color:var(--accent);opacity:0;transition:opacity .2s}
/* While a search is open the objects step back rather than crowd the panel.
   Faded, not removed: in the scatter they are positioned absolutely, so this
   hides them without anything reflowing. */
#hub.searching .obj{opacity:0;pointer-events:none;transition:opacity .18s var(--e)}
.obj:hover .label .arrow{opacity:1}

/* ---------- search ---------- */
.search{position:relative;z-index:2;max-width:360px;margin:clamp(12px,2vh,20px) auto 0;
  padding:0 20px}
.search .box{position:relative;display:flex;align-items:center;gap:9px;
  border:1px solid var(--line-2);border-radius:999px;padding:9px 15px;
  background:rgba(255,255,255,.4)}
.search .box:focus-within{border-color:var(--accent)}
.search svg{width:16px;height:16px;color:var(--faint);flex:none}
.search input{flex:1;border:0;background:transparent;font-family:var(--body);
  font-size:15px;color:var(--ink);outline:none;min-width:0}
.search input::placeholder{color:var(--faint)}
.search .count{font-family:var(--mono);font-size:10.5px;color:var(--faint);
  text-align:center;margin-top:9px;min-height:14px}

/* Search is a list of every node, not a filter over the tiles: once most of the
   page lives inside folders, hiding root tiles would find almost nothing. */
/* Anchored under the box rather than placed in the flow: the heading, the
   search and the objects must not move while someone is typing. */
/* One width, set by the viewport and not by what happens to match, so the
   panel does not resize itself under the cursor as someone types. */
.results{position:absolute;z-index:8;top:calc(100% + 9px);left:50%;
  transform:translateX(-50%);width:min(min(560px,78vw),calc(100vw - 32px));
  text-align:left}
.results[hidden]{display:none}
/* Solid, not translucent: the nothing-found arrow is revealed by sliding a
   panel-coloured cover off it, and the cover has to match exactly. */
.results ol{list-style:none;margin:0;border:1px solid var(--line-2);border-radius:var(--r);
  background:var(--panel);overflow:hidden;max-height:min(46vh,340px);overflow-y:auto}
.results li + li{border-top:1px solid var(--line)}
.results button{width:100%;display:flex;align-items:center;gap:11px;text-align:left;
  background:transparent;border:0;padding:10px 13px;cursor:pointer;font-family:inherit;
  color:inherit}
.results button:hover,.results button.on{background:var(--accent-soft)}
.results .ico{width:18px;height:18px;flex:none;color:var(--accent)}
.results .ico svg{width:100%;height:100%}
.results .t{flex:1;min-width:0;font-family:var(--display);font-weight:600;font-size:14.5px;
  letter-spacing:-.01em;line-height:1.25;overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap}
/* The trail is pushed to the far end rather than following the name, which is
   what made the two read as one run-on word. */
.results .c{flex:none;margin-left:14px;font-family:var(--mono);font-size:10px;
  letter-spacing:.08em;color:var(--faint);text-transform:uppercase;white-space:nowrap}
@media(max-width:519px){.results .c{display:none}}

/* Nothing found is not an error, it is an invitation. */
.results .none{padding:20px 16px;display:flex;flex-direction:column;
  align-items:center;gap:2px;text-align:center}

.results .none .say{font-family:var(--display);font-weight:600;font-size:15.5px;
  letter-spacing:-.01em}
.results .none .sub2{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;
  color:var(--faint);text-transform:uppercase;margin-top:4px}


/* ---------- accent picker ---------- */
.swatches{position:relative;z-index:2;display:flex;justify-content:center;gap:7px;
  margin-top:clamp(10px,1.8vh,16px)}
.sw{width:17px;height:17px;border-radius:999px;border:1px solid rgba(23,21,15,.2);
  cursor:pointer;padding:0;transition:transform .15s var(--e),box-shadow .15s var(--e)}
.sw:hover{transform:scale(1.18)}
.sw[aria-pressed=true]{box-shadow:0 0 0 2px var(--paper),0 0 0 3.5px var(--ink)}
.sw:focus-visible{outline:2px solid var(--ink);outline-offset:3px}

/* ---------- contact ---------- */
.contact{position:relative;z-index:2;display:flex;justify-content:center;gap:8px;
  flex-wrap:wrap;margin-top:clamp(14px,2.4vh,26px);padding:0 20px}
.contact a{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);
  font-size:12px;letter-spacing:.03em;color:var(--muted);border:1px solid var(--line);
  border-radius:999px;padding:8px 15px;background:rgba(255,255,255,.35)}
.contact a:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.contact svg{width:16px;height:16px;flex:none}
.hub-foot{text-align:center;margin-top:10px;font-family:var(--mono);font-size:10.5px;
  letter-spacing:.1em;color:var(--faint)}
/* The same bar under the poster and under an opened item: how to reach me, the
   accent, and the reset once anything has been moved. */
#chrome{flex:0 0 auto;border-top:1px solid var(--line);margin-top:auto;
  padding:clamp(12px,2vh,20px) 20px clamp(14px,2.4vh,26px)}
#chrome .row{max-width:980px;margin:0 auto;display:flex;align-items:center;
  justify-content:center;gap:10px;flex-wrap:wrap}
#chrome .contact{margin-top:0;padding:0;gap:8px}
#chrome .swatches{margin-top:0}
#chrome .tail{position:relative;display:flex;align-items:center;gap:10px}
.corner{position:fixed;left:clamp(14px,2.4vw,30px);bottom:clamp(14px,2.4vh,26px);z-index:7;
  display:flex;flex-direction:column;align-items:flex-start;gap:8px;pointer-events:none}
.corner > *{pointer-events:auto}
body.open .corner{display:none}

/* ---------- a detail view ---------- */
#view{display:none}
body.open #hub{display:none}
body.open #view{display:block}
.topbar{position:sticky;top:0;z-index:40;background:rgba(242,238,227,.9);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line)}
.topbar .inner{max-width:820px;margin:0 auto;padding:11px 20px;
  display:flex;align-items:center;gap:14px}
.back{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--ink);
  border:1px solid var(--line-2);border-radius:999px;padding:7px 14px;background:transparent;
  cursor:pointer;white-space:nowrap}
.back:hover{border-color:var(--accent);color:var(--accent)}
.where{font-family:var(--mono);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint);overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap;min-width:0}
.topbar .search{margin:0 0 0 auto;padding:0;flex:0 1 268px;min-width:132px;z-index:41}
.topbar .search .box{padding:7px 13px}
.topbar .search input{font-size:13.5px}
.topbar .search .count{display:none}
/* Anchored to the right edge of the box here, not centred on it, or it would
   hang off the side of the window. */
.topbar .search .results{left:auto;right:0;transform:none;
  width:min(420px,calc(100vw - 28px))}
/* On a narrow screen the trail gives way to the input: the heading underneath
   already says where you are. */
@media(max-width:639px){
  .topbar .where{display:none}
  .topbar .search{flex:1 1 auto}
}
/* Written on the lines: prose uses the ruling pitch for its line-height, and the
   page starts on a whole number of rules so the two stay in step as you scroll. */
#view{padding-top:0}
.view-body p,.view-body li,.notes li{line-height:var(--rule)}
.view-body p{font-size:clamp(15px,3.6vw,16.5px)}
.view-head{padding:calc(var(--rule) * 2) 0 0}
.view-head .n{font-family:var(--mono);font-size:11px;letter-spacing:.2em;color:var(--accent)}
.view-head h2{margin-top:12px}
.view-head .lead{margin-top:16px}
.view-body{padding:var(--rule) 0 clamp(50px,11vw,86px)}
.view-body > * + *{margin-top:var(--rule)}

/* ---------- shared blocks ---------- */
.panel{border:1px solid var(--line);border-radius:var(--r);background:var(--paper-2);
  margin-top:24px;overflow:hidden}
.panel-head{display:flex;align-items:center;gap:12px;padding:12px 15px;
  border-bottom:1px solid var(--line)}
.panel-head .t{font-family:var(--mono);font-size:12px;color:var(--muted);letter-spacing:.05em}
.panel-head .note{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;
  color:var(--faint);margin-left:auto;text-align:right}
.panel-head .t + .copy{margin-left:auto}
pre{font-family:var(--mono);font-size:12.5px;line-height:1.62;color:var(--ink);
  padding:15px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;max-height:340px}
.copy{font-family:var(--mono);font-size:11.5px;letter-spacing:.05em;padding:7px 14px;
  border-radius:999px;border:1px solid var(--line-2);background:transparent;color:var(--ink);
  cursor:pointer;white-space:nowrap;transition:border-color .15s,color .15s,background .15s}
.copy:hover{border-color:var(--accent);color:var(--accent)}
.copy.done{border-color:var(--accent);color:#fff;background:var(--accent)}
.btn{font-family:var(--mono);font-size:12.5px;letter-spacing:.04em;padding:11px 18px;
  border-radius:999px;border:1px solid var(--line-2);color:var(--ink);background:transparent;
  cursor:pointer;display:inline-block}
.btn:hover{border-color:var(--accent);background:var(--accent-soft);color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
.btn.primary:hover{background:#2440b8;border-color:#2440b8;color:#fff}

.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-top:22px}
.tab{font-family:var(--mono);font-size:11.5px;padding:8px 13px;border-radius:999px;
  border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer}
.tab:hover{color:var(--ink);border-color:var(--line-2)}
.tab[aria-selected=true]{background:var(--accent);border-color:var(--accent);color:#fff}

.split{display:grid;gap:16px;margin-top:24px}
@media(min-width:760px){.split{grid-template-columns:1fr 1fr}.split .panel{margin-top:0}}

details{border:1px solid var(--line);border-radius:var(--r);background:var(--paper-2);
  margin-top:12px;overflow:hidden}
summary{padding:13px 15px;cursor:pointer;font-family:var(--mono);font-size:12.5px;
  color:var(--ink);list-style:none;display:flex;align-items:center;gap:10px}
summary::-webkit-details-marker{display:none}
summary .arrow{color:var(--faint);transition:transform .15s}
details[open] summary .arrow{transform:rotate(90deg)}
summary .note{color:var(--faint);font-size:11px;margin-left:auto}
summary .copy{margin-left:auto}
summary .note + .copy{margin-left:14px}

.fig{margin-top:24px;border:1px solid var(--line);border-radius:var(--r);
  background:var(--paper-2);padding:16px;overflow:hidden}
.fig svg{display:block;width:100%;height:auto}
.fig .cap{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--faint);margin-top:11px}

table{width:100%;border-collapse:collapse;margin-top:20px;font-size:14.5px}
th,td{text-align:left;padding:11px 12px 11px 0;vertical-align:top}
th{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--faint);font-weight:400;border-bottom:1px solid var(--line-2)}
td{color:var(--muted);border-bottom:1px solid var(--line)}
td:first-child{color:var(--ink);font-weight:600;white-space:nowrap;padding-right:18px}
code{font-family:var(--mono);font-size:.88em;color:var(--ink);
  background:var(--paper-3);padding:2px 6px;border-radius:5px}

ul{list-style:none;margin-top:16px}
ul li{color:var(--muted);font-size:clamp(15px,3.6vw,16.5px);padding:8px 0 8px 20px;
  position:relative}
ul li::before{content:"";position:absolute;left:0;top:17px;width:8px;height:1px;
  background:var(--faint)}

.rule{font-family:var(--display);font-weight:800;font-size:clamp(21px,4.8vw,32px);
  line-height:1.22;letter-spacing:-.02em;color:var(--ink);max-width:21ch;margin-top:22px}
.formula{font-family:var(--mono);font-size:clamp(11.5px,2.9vw,14px);line-height:2;
  display:flex;flex-wrap:wrap;gap:6px;align-items:center;justify-content:center}
.f-op{color:var(--faint)}.f-key{color:var(--accent)}
.f-out{color:var(--ink);font-weight:500}
.f-end{color:var(--ink);font-weight:700;border-bottom:2px solid var(--accent)}

/* The nudge sits above the reset in the bar, so the arrow points past it at the
   folders rather than at the button under it. */
.hint{display:flex;flex-direction:column;align-items:flex-start;gap:3px;white-space:nowrap;
  font-family:var(--mono);font-size:10.5px;line-height:1.35;letter-spacing:.06em;
  color:var(--faint);text-align:left;animation:hintIn .6s var(--e) both .9s}
.hint svg{width:68px;height:38px;fill:none;stroke:var(--faint);stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round;margin-left:6px}
/* Two passes over the same line, the way a pencil actually leaves one. */
.hint svg path{stroke-dasharray:170;stroke-dashoffset:170;
  animation:draw 1.1s var(--e) forwards 1.25s}
.hint svg .pass2{opacity:.45;animation-delay:1.45s;animation-duration:.95s}
.hint.gone{animation:hintOut .4s var(--e) both}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes hintIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@keyframes hintOut{to{opacity:0;transform:translateY(4px)}}
body.open .hint,body.open .reset{display:none}
.reset{font-family:var(--mono);font-size:10px;letter-spacing:.1em;color:var(--faint);
  background:rgba(255,255,255,.4);border:1px solid var(--line-2);border-radius:999px;
  cursor:pointer;padding:6px 12px}
.reset:hover{color:var(--accent);border-color:var(--accent)}
@media (prefers-reduced-motion: reduce){
  .hint{animation:none}
  .hint svg path{animation:none;stroke-dashoffset:0}
}

html.reveal .view-body > *{opacity:0;transform:translateY(16px);
  transition:opacity .5s var(--e),transform .5s var(--e)}
html.reveal .view-body > *.in{opacity:1;transform:none}
@media (prefers-reduced-motion: reduce){
  *{transition:none!important;animation:none!important}
  html.reveal .view-body > *{opacity:1;transform:none}
}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes settle{
  from{opacity:0;transform:rotate(var(--r)) translateY(-14px) scale(.94)}
  to{opacity:1;transform:rotate(var(--r))}
}
html.anim .obj{animation:settle .5s var(--e) both;animation-delay:var(--d,0s)}
html.anim #hub.scatter .obj{animation-name:settle}
@media (prefers-reduced-motion: reduce){html.anim .obj{animation:none}}
::view-transition-old(root),::view-transition-new(root){animation-duration:.26s}
"""


def panel(key, label, note=""):
    n = f'<span class="note">{H.escape(note)}</span>' if note else ""
    return (f'<div class="panel"><div class="panel-head"><span class="t">{H.escape(label)}</span>{n}'
            f'<button class="copy" data-copy="{key}">Copy</button></div>'
            f'<pre data-block="{key}"></pre></div>')


def disclosure(key, summary, note=""):
    n = f'<span class="note">{H.escape(note)}</span>' if note else ""
    return (f'<details><summary><span class="arrow">&#9656;</span>{H.escape(summary)}{n}'
            f'<button class="copy" data-copy="{key}">Copy</button></summary>'
            f'<pre data-block="{key}"></pre></details>')


def fig(A, key, caption):
    return f'<div class="fig">{A[key]}<div class="cap">{H.escape(caption)}</div></div>'


def views(A, c):
    """Each entry: slug, poster label, thumbnail art key or glyph, title, lede, body."""
    tabs = "".join(
        f'<button class="tab" role="tab" data-soul="{i}" aria-selected="{"true" if i == 0 else "false"}">'
        f'{H.escape(s["name"])}</button>' for i, s in enumerate(c["souls"]))

    v = []
    v.append(dict(
        slug="generator", label="The Setup Interview", art=None, glyph="?",
        title="The Setup Interview",
        lede="One prompt. It asks you questions for five minutes, then writes four files "
             "for your actual job.",
        body=f"""
<p>It asks what you do, what you redo every week and resent, how you do it now, and what keeps
going wrong. Then it writes: how it should behave, how it should work, what it can reach, and
how you do that one task.</p>
<p>Paste it as the first message in any chat. Claude, ChatGPT, Gemini, Copilot. It works in a
terminal agent too, and on a phone.</p>
{panel("generator", "The Setup Interview", "about 5 minutes")}
<p><strong>The third question is the one people rush.</strong> Walk it through how you actually
do the thing, fiddly parts included. The skill it writes is only as good as that answer.</p>"""))

    v.append(dict(
        slug="soul", label="Five soul files", art="harness", glyph=None,
        title="Five soul files",
        lede="Who the AI is when it works with you: its standards, its voice, what it never "
             "does.",
        body=f"""
<p>Same model, different colleague. Pick the closest to your job, then change two lines so it
sounds like you. That is the whole setup.</p>
<div class="tabs" role="tablist">{tabs}</div>
<div class="panel"><div class="panel-head"><span class="t" id="soul-name"></span>
<button class="copy" data-copy="soul">Copy</button></div>
<pre data-block="soul"></pre></div>
<p>Where it goes: ChatGPT Custom Instructions or a Project, Gemini Gems, a Claude Project,
Copilot custom instructions, or <code>AGENTS.md</code> in a project folder.</p>
{fig(A, "harness", "The harness is everything around the model")}"""))

    v.append(dict(
        slug="loop", label="The loop checklist", art="loop", glyph=None,
        title="Make it finish instead of wander",
        lede="Four lines above any task: the goal, the check, the stop, the limit.",
        body=f"""
<p><strong>The check is the one people skip and the one that matters.</strong> "I will review it
carefully" is not a check. "Both totals match the source file" is, because it can fail.</p>
{fig(A, "loop", "Do a step, check it, decide whether to go again")}
<div class="split">
{panel("loopChat", "For a chat", "paste above your task")}
{panel("loopFile", "For a project folder", "goes in AGENTS.md")}
</div>
<p>Without a stop rule, a model will try variations of the same broken idea until you interrupt
it. With one, it comes back after two.</p>"""))

    v.append(dict(
        slug="tools", label="The tool registry", art="mcp", glyph=None,
        title="Stop it reaching for the wrong thing",
        lede="Which tool answers which kind of question, and which ones to ignore.",
        body=f"""
<p>Once an agent has more than about three tools, it starts guessing. It searches the web for
something sitting in your own files, or proposes a plan built on access it does not have.</p>
<p>Pasted into a plain chat with no tools at all, this tells the model what access <em>you</em>
have, so it stops suggesting things you cannot do and starts asking for what it needs.</p>
{disclosure("regChat", "If you have no tools connected", "start here")}
{disclosure("regTemplate", "The blank template")}
{disclosure("regExample", "A filled example, someone in data")}
{fig(A, "mcp", "One standard, so each tool needs no integration of its own")}
<p><strong>Before you connect anything:</strong> who wrote it, what access is it asking for, when
was it last updated, and would you be fine if it could see everything you point it at.</p>"""))

    v.append(dict(
        slug="memory", label="Second Brain", art="memory", glyph=None,
        title="Second Brain",
        lede="A memory that outlives the conversation, so you stop re-explaining yourself "
             "every Monday.",
        body=f"""
<p>Context is what it can see right now. It fills up, and things fall out. Memory is what
survives the conversation ending, and it is the whole difference between a tool you operate
and a colleague who already knows the background.</p>
<p class="rule">Once is a correction. Twice is a missing line in a file.</p>
<p>Correcting it in the moment costs nothing and teaches it nothing. The second time the same
thing happens, write the line down. Some tools now save your corrections for you. Go and read
what they saved, because they get it wrong sometimes.</p>
<table><thead><tr><th>Tool</th><th>Where to look</th></tr></thead><tbody>
<tr><td>Claude Code</td><td>Type <code>/memory</code>. On by default.</td></tr>
<tr><td>ChatGPT</td><td>Settings, Personalization, Memory. Separate from Custom Instructions.</td></tr>
<tr><td>Claude</td><td>Settings, Memory. A separate memory per Project.</td></tr>
<tr><td>Gemini</td><td>Settings, Personal context, Memory.</td></tr>
<tr><td>Cursor, Copilot, Codex</td><td>Nothing is saved for you. Write it in <code>AGENTS.md</code> yourself.</td></tr>
</tbody></table>
{fig(A, "memory", "Context is this conversation. Memory is every conversation.")}
<p>Worth saying plainly: <strong>it does not get smarter.</strong> The model is fixed. What
changes is how much it knows about you and your work, and that is worth a lot on its own.</p>
<div class="panel"><div class="panel-head"><span class="t">Built on exactly this</span></div>
<div style="padding:16px 15px">
<p style="margin:0">Every tool above keeps its own memory, in its own format, locked to itself.
Correct something in one and the others never hear about it. <strong>Ownr</strong> is the
version of this I am building: one memory, shared across every assistant you use.</p>
<p style="margin-top:12px"><a href="https://ownr.digital" target="_blank" rel="noopener">
ownr.digital &rarr;</a></p>
</div></div>"""))

    v.append(dict(
        slug="skills", label="Business Analytics Skills", art="skill", glyph=None,
        title="Business Analytics Skills",
        lede="Thirty-six skills across machine learning, statistics, optimisation, pricing, "
             "decision analysis, data engineering and recommenders.",
        body=f"""
<p>Each one asks what the work is for, follows a real method, checks its own logic, and hands
back a decision rather than a number. MIT licensed, yours to change.</p>
<p>They install as seven toolkits from a marketplace, or as plain folders in any tool that
reads the open Agent Skills format. The repository is
<code>moheetsubudhi-isb/business-analytics-skills</code>.</p>
<div class="split">
{panel("installClaude", "Claude Code")}
{panel("installCodex", "Codex")}
</div>
<p>Any other tool, or several at once:</p>
{panel("installCli", "Cursor, Copilot, Gemini CLI and more")}
{fig(A, "skill", "A skill is one task, written down once")}
<p>Browse them first at <a href="{REPO}">the repository</a>.</p>"""))

    v.append(dict(
        slug="local", label="Run it on your laptop", art="context", glyph=None,
        title="Open models, and running one yourself",
        lede="The weights are published, so you can download the model and run it on your "
             "own machine. No account, no API, no data leaving the building.",
        body="""
<h3>What &ldquo;open&rdquo; actually means here</h3>
<p>A model is a very large file of numbers, the weights. With GPT-5 or Claude those numbers
stay on the company&rsquo;s servers and you rent access through an API. With an open model the
company publishes the file. You download it and run it, and nobody can switch it off, meter
it, or see what you asked.</p>
<p><strong>Open weights is not the same as open source.</strong> Almost all of these publish the
weights under their own licence while keeping the training data and code private. Most allow
commercial use; a few restrict it above a size of business. If you are shipping something
commercial, read the licence rather than assuming.</p>

<h3>Why it is worth knowing</h3>
<ul>
<li><strong>Nothing leaves.</strong> The obvious one, and the only answer that satisfies a
compliance team without a procurement cycle.</li>
<li><strong>No per-token cost.</strong> The work is free once the file is on disk, so you can
run it over ten thousand rows without watching a meter.</li>
<li><strong>It cannot be deprecated.</strong> A model you have downloaded behaves the same next
year. Hosted models change underneath you.</li>
<li><strong>It works offline.</strong> Genuinely: turn the wifi off and it still answers.</li>
</ul>

<h3>The families worth knowing</h3>
<table><thead><tr><th>Family</th><th>From</th><th>Worth it for</th></tr></thead><tbody>
<tr><td><a href="https://www.llama.com" target="_blank" rel="noopener">Llama</a></td><td>Meta</td><td>The default all-rounder. The small ones are fast and good enough for most everyday work.</td></tr>
<tr><td><a href="https://qwen.ai" target="_blank" rel="noopener">Qwen</a></td><td>Alibaba</td><td>Strongest small models right now, and the best multilingual coverage.</td></tr>
<tr><td><a href="https://ai.google.dev/gemma" target="_blank" rel="noopener">Gemma</a></td><td>Google</td><td>Small, efficient, well-behaved. Good on a modest laptop.</td></tr>
<tr><td><a href="https://mistral.ai" target="_blank" rel="noopener">Mistral</a></td><td>Mistral AI</td><td>European, permissive licensing, strong at its size.</td></tr>
<tr><td>Phi</td><td>Microsoft</td><td>Punches far above its weight at reasoning and code for how small it is.</td></tr>
<tr><td><a href="https://www.deepseek.com" target="_blank" rel="noopener">DeepSeek</a></td><td>DeepSeek</td><td>Reasoning models at a fraction of the usual size.</td></tr>
<tr><td><a href="https://huggingface.co/openai" target="_blank" rel="noopener">gpt-oss</a></td><td>OpenAI</td><td>OpenAI&rsquo;s open-weight release. The 20B is the largest thing that fits in plain 16&nbsp;GB.</td></tr>
</tbody></table>
<p>Everything published lives on <a href="https://huggingface.co/models" target="_blank" rel="noopener">Hugging Face</a>, which is where these actually get released. It is worth half an hour of browsing.</p>

<h3>Three ways to run one</h3>
<table><thead><tr><th>Tool</th><th>Suits</th></tr></thead><tbody>
<tr><td><a href="https://ollama.com" target="_blank" rel="noopener">Ollama</a></td><td>One command, a desktop window if you want one, and it plugs into coding agents. Start here.</td></tr>
<tr><td><a href="https://lmstudio.ai" target="_blank" rel="noopener">LM Studio</a></td><td>A proper app with a model browser. Best if you would rather never see a terminal.</td></tr>
<tr><td><a href="https://jan.ai" target="_blank" rel="noopener">Jan</a></td><td>Open source, offline by default, looks like a normal chat app.</td></tr>
</tbody></table>

<h3>Which size fits your machine</h3>
<p>Match the model to your memory first, then worry about which one. The download size is
roughly what it needs in RAM while running, and you need headroom for everything else open.</p>
<table><thead><tr><th>You have</th><th>Run</th></tr></thead><tbody>
<tr><td>4 GB</td><td>A 1&ndash;2B model. Summarising, extraction, tidying text.</td></tr>
<tr><td>8 GB</td><td>A 3&ndash;4B model, around 2&ndash;2.5 GB on disk. The everyday sweet spot.</td></tr>
<tr><td>16 GB</td><td>A 7&ndash;8B model. Good enough for most daily work.</td></tr>
<tr><td>16 GB and patient</td><td>gpt-oss 20B, about 14 GB. Slow, but it runs with no graphics card.</td></tr>
</tbody></table>
<p>Start with the smallest one that could work:</p>
{panel("ollama", "Your first model", "1.4 GB download")}
<p>If it will not load you will see <code>model requires more system memory than is
available</code>. It checks free memory, not installed, so closing a browser with forty tabs
genuinely fixes it. In any model picker, avoid anything with <code>:cloud</code> in the name,
which runs on someone else&rsquo;s servers and defeats the point.</p>

<h3>Be honest about what it cannot do</h3>
<p>A small local model is meaningfully worse than a frontier model at hard, multi-step
reasoning. It is entirely good enough for pulling fields out of messy text, summarising,
classifying, redacting, and first drafts you were going to rewrite anyway.</p>
<p class="rule">The local model filters. The cloud model finishes.</p>
<p>Run the local one over anything sensitive, strip what matters, send only the remainder to
the better model. Most of your data never leaves, and you still get a frontier answer where it
counts. That is the pattern worth stealing, and the one that gets signed off.</p>"""))

    v.append(dict(
        slug="projects", label="My projects", art=None, icon="projects",
        title="Things I am building",
        lede="Built to scratch an itch.",
        children=[
            dict(slug="ownr", label="Ownr", icon="memory",
                 title="Ownr",
                 lede="One memory, shared across every AI tool you use.",
                 body="""
<p>Every assistant keeps its own memory in its own format, locked to itself. Correct something
in one and the others never hear about it, so you re-explain the same context on Monday that
you explained on Friday.</p>
<p>Ownr is one memory that sits outside all of them. Your standing rules, your projects, the
decisions you have already made and why. Any tool can read it and write to it, so a correction
given once holds everywhere.</p>
<p><a class="btn primary" href="https://ownr.digital/#waitlist" target="_blank" rel="noopener">Join the waitlist</a>\n<a class="btn" href="https://ownr.digital" target="_blank" rel="noopener">ownr.digital</a></p>"""),
        ]))

    v.append(dict(
        slug="parts", label="The seven parts", art="loopring", glyph=None,
        title="The seven parts",
        lede="Six of these seven are not the model. Six of these seven are where things "
             "actually break.",
        body="""
<p>Nearly everyone starts at the model and stops there, which is why most attempts stall at
something that talks back well and does nothing. The model is one part. The other six are the
work, and they are all things you control.</p>
<div class="panel"><div class="panel-head"><span class="t">The whole thing, in one line</span></div>
<div style="padding:18px 15px">
<div class="formula"><span class="f-key">Model</span><span class="f-op">+</span><span class="f-key">Harness</span><span class="f-op">+</span><span class="f-key">Loop</span><span class="f-op">+</span><span class="f-key">MCP</span><span class="f-op">+</span><span class="f-key">Skills</span><span class="f-op">+</span><span class="f-key">Memory</span><span class="f-op">=</span><span class="f-end">your idea, working</span></div>
</div></div>
<table><thead><tr><th>Part</th><th>What it is</th></tr></thead><tbody>
<tr><td>Model</td><td>Predicts text. On its own it can only talk back.</td></tr>
<tr><td>Harness</td><td>What it reads, what it may touch, who it is. <a href="#build/soul" data-jump="build/soul">Start here</a>.</td></tr>
<tr><td>Loop</td><td>Do, check, decide whether to go again. Why work finishes. <a href="#build/loop" data-jump="build/loop">Here</a>.</td></tr>
<tr><td>MCP</td><td>One standard for reaching tools. <a href="#build/tools" data-jump="build/tools">Here</a>.</td></tr>
<tr><td>Skills</td><td>One task, written down once. <a href="#skills" data-jump="skills">Here</a>.</td></tr>
<tr><td>Context</td><td>What it sees right now. It fills up, and things fall out.</td></tr>
<tr><td>Memory</td><td>What survives the conversation ending. <a href="#build/memory" data-jump="build/memory">Here</a>.</td></tr>
</tbody></table>
<p>The order matters. Each one is only worth adding once the one before it holds.</p>"""))

    # Words people are likely to type that the prose does not happen to contain.
    KEYWORDS = {
        "generator": "prompt interview setup start here chatgpt claude gemini copilot custom instructions",
        "soul": "persona role tone voice style system prompt consultant data ops product marketing harness",
        "loop": "agent wander stuck retry goal check stop limit finish done",
        "tools": "mcp connector server integration access permissions registry composio",
        "memory": "remember forget context corrections agents.md claude.md learning "
                  "second brain secondary ownr shared memory",
        "skills": "business analytics skills bas repo github machine learning statistics "
                  "optimisation optimization pricing price elasticity regression clustering "
                  "forecasting ab test experiment recommender data engineering toolkit "
                  "install plugin marketplace",
        "local": "ollama offline privacy compliance laptop cpu ram gpu open source weights licence llama qwen gemma mistral phi deepseek gpt-oss hugging face lm studio jan",
        "parts": "model harness loop mcp skills context memory overview recap formula summary",
        "projects": "projects ownr portfolio work building side product repo "
                    "things i am building side project unfinished",
        "build": "session talk presentation how to build with ai giveaway pack take home "
                 "seven parts model harness loop mcp skills context memory plain text tonight",
    }
    def index(item):
        """A node is searchable on its own words plus, if it is a folder, its children's."""
        kids = item.get("children", [])
        for k in kids:
            index(k)
        words = " ".join([item["title"], item["lede"],
                          re.sub(r"<[^>]+>", " ", item.get("body", "")),
                          " ".join(k["find"] for k in kids),
                          KEYWORDS.get(item["slug"], "")])
        item["find"] = re.sub(r"\s+", " ", item["label"] + " " + words).strip().lower()[:1400]

    # The root is a portfolio. One folder holds everything from the session, in the
    # order it is taught; the other holds the work. Both grow by adding a child.
    by = {n["slug"]: n for n in v}
    ORDER = ["parts", "generator", "soul", "loop", "tools", "memory", "local"]
    root = [
        dict(slug="build", label="How to Build with AI", art=None, icon="loop",
             title="How to Build with AI",
             lede="Everything from the session.",
             children=[by[k] for k in ORDER]),
        by["skills"],
        by["projects"],
    ]
    for item in root:
        index(item)
    return root


def build():
    c = content()
    A = art()
    I = icons()
    V = views(A, c)

    SPOTS_UNUSED = None

    def icon_for(node):
        """A node names an icon, or borrows the one matching its slug."""
        return I.get(node.get("icon") or node["slug"]) or I["spark"]

    def walk(nodes, parent=""):
        """Every node, with the path that addresses it. One place that knows the tree."""
        for i, n in enumerate(nodes):
            path = f"{parent}/{n['slug']}" if parent else n["slug"]
            yield path, n, i, parent
            for item in walk(n.get("children", []), path):
                yield item

    ALL = list(walk(V))

    def tile(path, node, i, parent):
        """Every tile for every folder is rendered once; the poster shows one set."""
        return (f'<button class="obj" data-go="{path}" data-parent="{parent}" '
                f'data-find="{H.escape(node.get("find", ""))}">'
                f'<span class="thumb"><span class="ico">{icon_for(node)}</span></span>'
                f'<span class="n">({i + 1:02d})</span>'
                f'<span class="label">{H.escape(node["label"])} '
                f'<span class="arrow">&rarr;</span></span></button>')

    objects = "".join(tile(p2, n, i, parent) for p2, n, i, parent in ALL)

    # Only a leaf gets a pane. A folder opens the poster again, retitled.
    panes = "".join(
        f'<article class="pane" data-pane="{path}" hidden>'
        f'<div class="wrap view-head"><span class="n">({i + 1:02d})</span>'
        f'<h2>{H.escape(n["title"])}</h2>'
        f'<p class="lead">{H.escape(n["lede"])}</p></div>'
        f'<div class="wrap view-body">{n["body"]}</div></article>'
        for path, n, i, parent in ALL if not n.get("children"))

    # The poster can stand at the root or inside any folder, so each needs a heading.
    HOME = ("Hey, I\u2019m Moheet.", "Steal anything.")
    FOLDERS = {"": {"t": HOME[0], "s": HOME[1]}}
    for path, n, i, parent in ALL:
        if n.get("children"):
            FOLDERS[path] = {"t": n["title"], "s": n["lede"]}
    ICONS_BY_PATH = {p2: icon_for(n) for p2, n, i, parent in ALL}

    # Every one checked for contrast on the paper background and with white text on it.
    ACCENTS = [("Cobalt", "#2F4FD4"), ("Forest", "#1F6B4A"), ("Rust", "#B3431E"),
               ("Oxblood", "#8C2130"), ("Violet", "#5B33B5"), ("Teal", "#11636E")]
    swatches = "".join(
        f'<button class="sw" data-accent="{hx}" title="{n2}" aria-label="{n2}" '
        f'aria-pressed="{"true" if j == 0 else "false"}" '
        f'style="background:{hx}"></button>' for j, (n2, hx) in enumerate(ACCENTS))

    FOLDERS_JSON = json.dumps(FOLDERS)
    ICONS_JSON = json.dumps(ICONS_BY_PATH)
    PATHS = json.dumps([p2 for p2, n, i, parent in ALL])
    LABELS = json.dumps({p2: n["label"] for p2, n, i, parent in ALL})
    PARENTS = json.dumps({p2: parent for p2, n, i, parent in ALL})

    page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Moheet Subudhi</title>
<meta name="description" content="Things I am building, and the whole How to Build with AI pack: a prompt that writes your own setup, five ready-made ones, and 36 analytics skills.">
<meta name="theme-color" content="#F2EEE3">
<meta property="og:title" content="Moheet Subudhi">
<meta property="og:description" content="Everything I am building, and everything I would hand over. Plain text, nothing to install, and it works on your phone.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Hanken+Grotesk:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>

<div id="shell">
<div id="poster">
<div class="topbar" id="hubBar" hidden><div class="inner">
  <button class="back" id="hubUp">&larr; Back</button>
  <span class="where" id="hubWhere"></span>
</div></div>
<main id="hub" class="scatter">
  <div class="poster-title">
    <h1 id="hubTitle">{HOME[0]}</h1>
    <div class="sub" id="hubSub">{HOME[1]}</div>
  </div>
  <div class="search"><label class="box">
    {I["search"]}
    <input type="search" id="q" placeholder="Search everything" autocomplete="off"
           aria-label="Search everything">
    <div class="results" id="results" hidden></div>
  </label><div class="count" id="count"></div></div>
  <div class="objects">{objects}</div>
</main>
</div>

<div id="view">
  <div class="topbar"><div class="inner">
    <button class="back" id="back">&larr; Back</button>
    <span class="where" id="where"></span>
  </div></div>
  {panes}
</div>

<div id="chrome"><div class="row">
  <div class="contact">
    <a href="{LINKEDIN}" target="_blank" rel="noopener">{I["linkedin"]}LinkedIn</a>
    <a id="mail" href="#">{I["mail"]}Email</a>
    <a href="{WHATSAPP}" target="_blank" rel="noopener">{I["whatsapp"]}WhatsApp</a>
  </div>
  <div class="tail">
    <div class="swatches" role="group" aria-label="Accent colour">{swatches}</div>
  </div>
</div></div>

<div class="corner">
  <div class="hint" id="dragHint" hidden>
    <svg viewBox="0 0 96 54" aria-hidden="true"><path d="M8 50C22 48 50 44 70 30 80 23 85 16 87 9"/><path class="pass2" d="M9 52C23 50 51 45 71 31 81 24 85 17 86.5 10"/><path d="M90 8l-13 2M90 8l-3 13"/></svg>
    <span>drag the folders<br>anywhere you like</span>
  </div>
  <button id="resetSpots" class="reset" hidden>reset layout</button>
</div>
</div>

<script type="application/json" id="content">{json.dumps(c)}</script>
<script>
const C = JSON.parse(document.getElementById("content").textContent);
const SLUGS = {PATHS};        /* every addressable node, "projects/ownr" and so on */
const TITLES = {LABELS};
const PARENTS = {PARENTS};    /* so back climbs one level instead of jumping home */
const FOLDERS = {FOLDERS_JSON};   /* a path the poster can stand at, and its heading */
const PICS = {ICONS_JSON};        /* each node's icon, reused in the search results */

document.querySelectorAll("pre[data-block]").forEach(function (el) {{
  if (C[el.dataset.block]) el.textContent = C[el.dataset.block];
}});

/* ---------- soul picker ---------- */
let currentSoul = 0;
const soulName = document.getElementById("soul-name");
const soulBody = document.querySelector('pre[data-block="soul"]');
function showSoul(i) {{
  currentSoul = i;
  soulName.textContent = C.souls[i].name;
  soulBody.textContent = C.souls[i].body;
  document.querySelectorAll("[data-soul]").forEach(function (t) {{
    t.setAttribute("aria-selected", String(Number(t.dataset.soul) === i));
  }});
}}
document.querySelectorAll("[data-soul]").forEach(function (t) {{
  t.addEventListener("click", function () {{ showSoul(Number(t.dataset.soul)); }});
}});
showSoul(0);

/* ---------- copy ---------- */
document.querySelectorAll("[data-copy]").forEach(function (btn) {{
  btn.addEventListener("click", async function (ev) {{
    /* The button sits inside a <summary>, so a click on it would also open or
       close the disclosure. Copying is not opening. */
    if (btn.closest("summary")) {{ ev.preventDefault(); ev.stopPropagation(); }}
    const key = btn.dataset.copy;
    const text = key === "soul" ? C.souls[currentSoul].body : C[key];
    let ok = false;
    try {{
      await navigator.clipboard.writeText(text);
      ok = true;
    }} catch (e) {{
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:absolute;left:-9999px;top:0";
      document.body.appendChild(ta);
      ta.select();
      ta.setSelectionRange(0, text.length);
      try {{ ok = document.execCommand("copy"); }} catch (e2) {{ ok = false; }}
      document.body.removeChild(ta);
    }}
    btn.textContent = ok ? "Copied" : "Select and copy";
    btn.classList.toggle("done", ok);
    setTimeout(function () {{ btn.textContent = "Copy"; btn.classList.remove("done"); }}, 2000);
  }});
}});

/* ---------- routing: the poster, then one view at a time ----------
   Hash based, so it is a plain static file with no server rules, and any single
   item can be linked to directly. */
const panes = document.querySelectorAll("[data-pane]");
const whereEl = document.getElementById("where");
const backBtn = document.getElementById("back");

function crumb(path) {{
  /* "projects/ownr" reads as "My projects / Ownr" */
  const out2 = [];
  let p3 = path;
  while (p3) {{ out2.unshift(TITLES[p3] || p3); p3 = PARENTS[p3] || ""; }}
  return out2.join("  /  ");
}}

const hubTitle = document.getElementById("hubTitle");
const hubSub = document.getElementById("hubSub");
const hubUp = document.getElementById("hubUp");
const hubBar = document.getElementById("hubBar");
const hubWhere = document.getElementById("hubWhere");
const SITE = "Moheet Subudhi";

/* An old link, or one written before the tree grew a level, still resolves: an
   unknown hash falls back to the one node whose own slug matches it. */
function resolvePath(raw) {{
  if (!raw) return "";
  if (raw in FOLDERS || SLUGS.indexOf(raw) > -1) return raw;
  /* Compare last segments, so a node that has since moved up a level resolves
     too: #build/skills still finds skills now that it sits at the root. */
  const tail = raw.split("/").pop();
  const hit = SLUGS.filter(function (s2) {{ return s2.split("/").pop() === tail; }});
  return hit.length === 1 ? hit[0] : "";
}}

/* The heading changes the way ink arrives on paper, not the way a terminal
   types: the old words blur away together, the new ones settle in one after
   another. Typing a word at a time out of nothing read as a glitch at any speed
   fast enough not to be annoying. CSS animations, so a throttled tab still
   lands on the finished state. */
let headTimers = [];
function words(text) {{
  return text.split(" ").map(function (w2, i) {{
    return '<span class="w" style="--d:' + (0.055 * i).toFixed(3) + 's">' +
      w2.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>";
  }}).join(" ");
}}
function setHeading(text, sub, animate) {{
  headTimers.forEach(clearTimeout);
  headTimers = [];
  hubTitle.setAttribute("aria-label", text);
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const same = hubTitle.textContent.trim() === text;
  const write = function () {{
    hubTitle.innerHTML = words(text);
    hubSub.innerHTML = '<span class="w">' +
      sub.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>";
    hubTitle.classList.remove("out");
    hubSub.classList.remove("out");
  }};
  if (!animate || reduced || same) {{ write(); return; }}
  hubTitle.classList.add("out");
  hubSub.classList.add("out");
  headTimers.push(setTimeout(write, 170));
  /* A backstop for a dropped timer, not a second run: rewriting unconditionally
     replaced the words and started the whole settle again. */
  headTimers.push(setTimeout(function () {{
    if (hubTitle.textContent.trim() !== text) write();
  }}, 700));
}}

let hubPath = "";
function showFolder(path, animate) {{
  hubPath = path;
  const f = FOLDERS[path] || FOLDERS[""];
  setHeading(f.t, f.s, animate);
  hubBar.hidden = !path;
  if (path) {{
    hubUp.textContent = "\u2190 " + (PARENTS[path] ? TITLES[PARENTS[path]] : SITE);
    hubWhere.textContent = TITLES[path];
  }}
  document.title = path ? TITLES[path] + " \u2014 " + SITE : SITE;
  if (q.value.trim()) {{ q.value = ""; }}
  runSearch();
  maybeHint();
}}

function apply(raw, animate) {{
  const path = resolvePath(raw);
  const leaf = SLUGS.indexOf(path) > -1 && !(path in FOLDERS);
  document.body.classList.toggle("open", leaf);
  if (q.value.trim()) {{ q.value = ""; runSearch(); }}
  placeSearch(leaf);
  panes.forEach(function (p) {{ p.hidden = p.dataset.pane !== path; }});
  if (leaf) {{
    /* The button beside it already says what it came out of. */
    whereEl.textContent = TITLES[path];
    document.title = TITLES[path] + " \u2014 " + SITE;
    const parent = PARENTS[path] || "";
    backBtn.textContent = "\u2190 " + (parent ? TITLES[parent] : SITE);
    backBtn.dataset.up = parent;
  }} else {{
    whereEl.textContent = "";
    showFolder(path in FOLDERS ? path : "", animate);
  }}
  window.scrollTo(0, 0);
  if (leaf) reveal(document.querySelector('[data-pane="' + path + '"]'));
}}

/* history.pushState throws on file:// and inside some sandboxed previews, which
   would otherwise break every link on the page. Fall back to setting the hash. */
function setUrl(slug) {{
  try {{
    history.pushState(null, "", slug ? "#" + slug : location.pathname + location.search);
  }} catch (e) {{
    if (slug) location.hash = slug;
    else if (location.hash) location.hash = "";
  }}
}}

function go(slug) {{
  const run = function () {{ setUrl(slug); apply(slug, true); }};
  if (document.startViewTransition &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    try {{ document.startViewTransition(run); }} catch (e) {{ run(); }}
  }} else {{
    run();
  }}
}}
window.addEventListener("hashchange", function () {{
  apply(location.hash.replace("#", ""));
}});

document.querySelectorAll("[data-go]").forEach(function (b) {{
  b.addEventListener("click", function () {{ go(b.dataset.go); }});
}});
backBtn.addEventListener("click", function () {{ go(backBtn.dataset.up || null); }});
hubUp.addEventListener("click", function () {{ go(PARENTS[hubPath] || null); }});
window.addEventListener("popstate", function () {{
  apply(location.hash.replace("#", ""));
}});
document.addEventListener("keydown", function (e) {{
  if (e.key === "Escape" && document.body.classList.contains("open")) go(null);
}});

/* ---------- reveal on scroll ----------
   A CSS class, not a JavaScript tween: a transition still lands on its final state
   when frames are dropped, so a throttled tab never leaves content invisible. The
   class is only added by script, so with no JavaScript the page is simply visible. */
let io = null;
function reveal(pane) {{
  if (!pane) return;
  const items = pane.querySelectorAll(".view-body > *");
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
      !("IntersectionObserver" in window)) {{
    items.forEach(function (el) {{ el.classList.add("in"); }});
    return;
  }}
  document.documentElement.classList.add("reveal");
  if (io) io.disconnect();
  io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{
      if (e.isIntersecting || e.boundingClientRect.top < 0) {{
        e.target.classList.add("in");
        io.unobserve(e.target);
      }}
    }});
  }}, {{ rootMargin: "0px 0px -6% 0px" }});
  items.forEach(function (el) {{ el.classList.remove("in"); io.observe(el); }});

  /* Anything already on screen is shown at once rather than waiting for the observer,
     which is delivered on a rendering step and can be throttled. Without this the
     first screenful of an opened view can sit blank. */
  function showOnScreen() {{
    items.forEach(function (el) {{
      if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add("in");
    }});
  }}
  /* Deferred by a frame. Adding the start and end states in one go means the
     browser never sees a change to transition between, which is why nothing moved. */
  if (window.requestAnimationFrame) {{
    requestAnimationFrame(function () {{ requestAnimationFrame(showOnScreen); }});
  }}
  setTimeout(showOnScreen, 220);
  setTimeout(function () {{ items.forEach(function (el) {{ el.classList.add("in"); }}); }}, 2500);
}}

/* ---------- poster scatter ----------
   Positions are measured, not guessed. Eight slots are laid around the title: three
   along the top, one at each side, three along the bottom. If the viewport cannot
   hold them clear of the title, the poster stays a grid instead of overlapping
   itself. Re-run on resize and once the fonts have settled, since both change the
   height of the centre block. */
function layoutScatter() {{
  const wide = window.matchMedia("(min-width: 850px)").matches;
  /* No minimum. A folder holding one thing lays out and drags like a folder
     holding seven; otherwise the page changes its own rules as it fills up. */
  const objsAll = [...hub.querySelectorAll(".obj")].filter(function (o) {{ return !o.hidden; }});
  if (!objsAll.length) {{ hub.classList.remove("scatter"); return; }}
  if (!wide) {{
    hub.classList.remove("scatter"); clearSpots(objsAll); return;
  }}

  hub.classList.add("scatter");
  /* Clamp the field to a band around the title. Anchored to the container edges,
     the objects end up half a screen from the headline on a wide monitor. */
  const H = hub.clientHeight;
  /* Held in around the heading rather than pushed to the edges of the monitor:
     at 1440 the full width put the corner objects a screen away from the title. */
  const band = Math.min(hub.clientWidth * 0.84, 1020);
  const x0 = (hub.clientWidth - band) / 2;
  const W = band;
  const pad = 14;
  const probe = objsAll[0].getBoundingClientRect();
  const ow = probe.width || 132, oh = probe.height || 170;

  /* Measure the headline's text, not its block: .poster-title spans the full width,
     so using its box would always claim there is no room beside it. */
  function textWidth(el) {{
    const rng = document.createRange();
    rng.selectNodeContents(el);
    const r2 = rng.getBoundingClientRect();
    return r2.width || el.getBoundingClientRect().width;
  }}
  const title = document.querySelector(".poster-title").getBoundingClientRect();
  const titleText = textWidth(document.querySelector(".poster-title h1"));
  const search = document.querySelector(".search").getBoundingClientRect();
  const hubTop = hub.getBoundingClientRect().top;
  const centreTop = title.top - hubTop, centreBottom = search.bottom - hubTop;

  const fieldH = Math.min(H, 700);
  const y0 = (H - fieldH) / 2;
  const topY = y0 + pad;
  const botY = y0 + fieldH - oh - pad;
  const roomTop = centreTop - (topY + oh);
  const roomBot = botY - centreBottom;
  if (roomTop < 8 || roomBot < 8) {{ hub.classList.remove("scatter"); clearSpots(objsAll); return; }}

  /* Slots are generated for however many objects exist, so adding one to the tree
     never leaves it stacked on another. Two sit beside the title when it leaves
     room; the rest spread along the top and the bottom. */
  const N = objsAll.length;
  const widest = Math.max(titleText, search.width);
  const useSides = ((W - widest) / 2 - pad * 2) >= ow && N >= 6;
  const spots = [];

  function row(count, y) {{
    if (count <= 0) return;
    const span = W - ow - pad * 2;
    for (let i = 0; i < count; i++) {{
      spots.push([pad + (count > 1 ? (span / (count - 1)) * i : span / 2), y]);
    }}
  }}

  const rest = N - (useSides ? 2 : 0);
  /* One or two sit under the heading rather than above it: a lone object over
     the title reads as a mistake. */
  const topCount = rest <= 2 ? 0 : Math.ceil(rest / 2);
  row(topCount, topY);
  if (useSides) {{
    const midY = Math.max(topY + oh + 8,
      Math.min(centreTop + (centreBottom - centreTop) / 2 - oh / 2, botY - oh - 8));
    spots.push([pad, midY]);
    spots.push([W - ow - pad, midY]);
  }}
  row(rest - topCount, botY);
  objsAll.forEach(function (o, i) {{
    const sp = spots[i] || spots[spots.length - 1];
    o.style.left = Math.round(x0 + sp[0]) + "px";
    o.style.top = Math.round(sp[1]) + "px";
  }});
  if (typeof applyPlaced === "function") applyPlaced();
}}
function clearSpots(list) {{
  list.forEach(function (o) {{ o.style.left = ""; o.style.top = ""; }});
  const live = [...hub.querySelectorAll(".obj")].filter(function (o) {{ return !o.hidden; }});
  const box = hub.querySelector(".objects");
  box.classList.toggle("few", live.length > 0 && live.length < 3);
  box.classList.toggle("many", live.length > 6);
}}

/* ---------- search ----------
   Matches every word typed against each item's title, lede and body text. While a
   search is running the poster drops out of scatter into a grid, because a scatter
   with items removed from it reads as broken rather than filtered. */
const hub = document.getElementById("hub");
const q = document.getElementById("q");
const countEl = document.getElementById("count");
const objs = [...hub.querySelectorAll(".obj")];
const resultsEl = document.getElementById("results");
const searchEl = document.querySelector(".search");
const searchHome = searchEl.parentNode, searchAfter = searchEl.nextSibling;
const topbarInner = document.querySelector(".topbar .inner");
function placeSearch(open) {{
  const want = open ? topbarInner : searchHome;
  if (searchEl.parentNode === want) return;
  if (open) want.appendChild(searchEl);
  else want.insertBefore(searchEl, searchAfter);
}}

/* Search reaches every node from anywhere, including one nested two levels down,
   and each hit says where it lives, so a name need not be unique on its own.
   Filtering the tiles instead would find almost nothing once most of the page
   sits inside folders. */
const INDEX = objs.map(function (o) {{
  return {{ path: o.dataset.go, find: o.dataset.find,
           label: TITLES[o.dataset.go], where: crumb(PARENTS[o.dataset.go] || "") }};
}});
let shown = [], cursor = 0;

function paint() {{
  resultsEl.querySelectorAll("[data-go]").forEach(function (b, i) {{
    b.classList.toggle("on", i === cursor);
  }});
}}
function open_(path) {{ q.value = ""; runSearch(); go(path); }}

function runSearch() {{
  const terms = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!terms.length) {{
    shown = []; cursor = 0;
    resultsEl.hidden = true;
    resultsEl.innerHTML = "";
    countEl.textContent = "";
    hub.classList.remove("searching");
    objs.forEach(function (o) {{ o.hidden = o.dataset.parent !== hubPath; }});
    layoutScatter();
    return;
  }}
  hub.classList.add("searching");
  /* A hit nearer the front of the indexed text is a more central one: the
     string starts with the label, so a name match sorts above a body match. */
  shown = INDEX.filter(function (it) {{
    return terms.every(function (t) {{ return it.find.indexOf(t) > -1; }});
  }}).sort(function (a, b) {{
    const sc = function (it) {{
      let n2 = 0;
      terms.forEach(function (t) {{ n2 += it.find.indexOf(t); }});
      return n2;
    }};
    return sc(a) - sc(b);
  }}).slice(0, 8);
  cursor = 0;
  countEl.textContent = "";
  resultsEl.hidden = false;
  if (!shown.length) {{
    resultsEl.innerHTML = '<ol><li class="none">' +
      '<span class="say">Not here. Ask me.</span>' +
      '<span class="sub2">Three ways below. I answer.</span>' +
      "</li></ol>";
    return;
  }}
  resultsEl.innerHTML = "<ol>" + shown.map(function (it) {{
    /* Flat children: the name and the trail are both flex items of the row, so
       the trail can be pushed to the far end. Nested in a wrapper they were not. */
    return '<li><button data-go="' + it.path + '"><span class="ico">' +
      (PICS[it.path] || "") + '</span><span class="t">' + it.label + '</span>' +
      (it.where ? '<span class="c">' + it.where + '</span>' : '') +
      '</button></li>';
  }}).join("") + "</ol>";
  resultsEl.querySelectorAll("[data-go]").forEach(function (b) {{
    b.addEventListener("click", function () {{ open_(b.dataset.go); }});
  }});
  paint();
}}
q.addEventListener("input", runSearch);
q.addEventListener("keydown", function (e) {{
  if (e.key === "Escape") {{ q.value = ""; runSearch(); q.blur(); return; }}
  if (!shown.length) return;
  if (e.key === "ArrowDown") {{ e.preventDefault(); cursor = (cursor + 1) % shown.length; paint(); }}
  else if (e.key === "ArrowUp") {{ e.preventDefault(); cursor = (cursor - 1 + shown.length) % shown.length; paint(); }}
  else if (e.key === "Enter") {{ e.preventDefault(); open_(shown[cursor].path); }}
}});
/* "/" anywhere puts the cursor in the box, the way every search field people
   already use behaves. */
document.addEventListener("keydown", function (e) {{
  if (e.key === "/" && document.activeElement !== q) {{ e.preventDefault(); q.focus(); }}
}});

/* Assembled at runtime so the address is not sitting in the markup for scrapers. */
const mail = document.getElementById("mail");
mail.href = "mailto:" + "moheetsubudhi" + "@" + "gmail.com";

/* ---------- accent ----------
   Only the accent moves; paper and ink stay put, so contrast holds whichever is
   picked. Stored per visitor, and a blocked localStorage must not break the page. */
function store(k, v) {{ try {{ localStorage.setItem(k, v); }} catch (e) {{}} }}
function recall(k) {{ try {{ return localStorage.getItem(k); }} catch (e) {{ return null; }} }}

function hexRgb(hex) {{
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}}
function setAccent(hex) {{
  const [r, g, b] = hexRgb(hex);
  const root = document.documentElement.style;
  root.setProperty("--accent", hex);
  root.setProperty("--accent-rgb", r + "," + g + "," + b);
  /* the second tint is the accent lifted toward the paper, so diagrams stay legible */
  const mix = function (c, p) {{ return Math.round(c + (p - c) * 0.52); }};
  const l = [mix(r, 242), mix(g, 238), mix(b, 227)];
  root.setProperty("--accent-2", "rgb(" + l.join(",") + ")");
  root.setProperty("--accent-2-rgb", l.join(","));
  document.querySelectorAll("[data-accent]").forEach(function (b2) {{
    b2.setAttribute("aria-pressed", String(b2.dataset.accent === hex));
  }});
  store("accent", hex);
}}
document.querySelectorAll("[data-accent]").forEach(function (b2) {{
  b2.addEventListener("click", function () {{ setAccent(b2.dataset.accent); }});
}});
const savedAccent = recall("accent");
if (savedAccent && /^#[0-9a-f]{{6}}$/i.test(savedAccent)) setAccent(savedAccent);

/* ---------- dragging the objects ----------
   Pointer events so it works with a mouse, a trackpad and a finger. A press that
   travels under a few pixels is still a click, so opening an item never breaks.
   Positions are remembered, and layoutScatter restores them on the next visit. */
const DRAG_KEY = "spots";
let placed = {{}};
try {{ placed = JSON.parse(recall(DRAG_KEY) || "{{}}") || {{}}; }} catch (e) {{ placed = {{}}; }}

function applyPlaced() {{
  if (!hub.classList.contains("scatter")) return;
  Object.keys(placed).forEach(function (slug) {{
    const el = hub.querySelector('[data-go="' + slug + '"]');
    if (!el || el.hidden) return;
    el.style.left = placed[slug][0] + "px";
    el.style.top = placed[slug][1] + "px";
  }});
}}

document.querySelectorAll(".obj").forEach(function (el) {{
  let sx = 0, sy = 0, ox = 0, oy = 0, moved = false, id = null;

  el.addEventListener("pointerdown", function (e) {{
    if (!hub.classList.contains("scatter") || e.button) return;
    id = e.pointerId; moved = false;
    sx = e.clientX; sy = e.clientY;
    ox = parseFloat(el.style.left) || el.offsetLeft;
    oy = parseFloat(el.style.top) || el.offsetTop;
    el.setPointerCapture(id);
  }});

  el.addEventListener("pointermove", function (e) {{
    if (id === null || e.pointerId !== id) return;
    const dx = e.clientX - sx, dy = e.clientY - sy;
    if (!moved && Math.abs(dx) + Math.abs(dy) < 5) return;   /* still a click */
    moved = true;
    el.classList.add("dragging");
    const w = hub.clientWidth - el.offsetWidth, h = hub.clientHeight - el.offsetHeight;
    const nx = Math.max(0, Math.min(w, ox + dx));
    const ny = Math.max(0, Math.min(h, oy + dy));
    el.style.left = nx + "px";
    el.style.top = ny + "px";
    placed[el.dataset.go] = [Math.round(nx), Math.round(ny)];
  }});

  function end(e) {{
    if (id === null || (e && e.pointerId !== id)) return;
    try {{ el.releasePointerCapture(id); }} catch (e2) {{}}
    id = null;
    if (moved) {{
      el.classList.remove("dragging");
      store(DRAG_KEY, JSON.stringify(placed));
      resetBtn.hidden = false;
      dismissHint();
    }}
  }}
  el.addEventListener("pointerup", end);
  el.addEventListener("pointercancel", end);

  /* a drag must not also open the item */
  el.addEventListener("click", function (e) {{
    if (moved) {{ e.stopImmediatePropagation(); e.preventDefault(); moved = false; }}
  }}, true);
}});

/* The nudge shows once, only where dragging is possible, and only to someone who
   has not already moved something. It leaves as soon as they do. */
const dragHint = document.getElementById("dragHint");
let hintTimer = null;
function maybeHint() {{
  const canDrag = hub.classList.contains("scatter");
  if (!canDrag) {{ dragHint.hidden = true; return; }}
  if (dragHint.dataset.gone) return;
  dragHint.hidden = false;
  clearTimeout(hintTimer);
  hintTimer = setTimeout(dismissHint, 7000);
}}
function dismissHint() {{
  if (dragHint.hidden) return;
  dragHint.dataset.gone = "1";
  dragHint.classList.add("gone");
  setTimeout(function () {{ dragHint.hidden = true; dragHint.classList.remove("gone"); }}, 400);
}}

const resetBtn = document.getElementById("resetSpots");
resetBtn.hidden = !Object.keys(placed).length;
resetBtn.addEventListener("click", function () {{
  placed = {{}};
  store(DRAG_KEY, "{{}}");
  hub.querySelectorAll(".obj").forEach(function (o) {{ o.style.left = ""; o.style.top = ""; }});
  layoutScatter();
  resetBtn.hidden = true;
}});

/* ---------- the opening ----------
   The objects settle into place once, when the poster first loads. Added by script
   after the positions are set, so nothing animates from the wrong spot, and never
   on the way back from an opened item. The class is only ever added here, so with
   no JavaScript the objects are simply there. */
function playOpening() {{
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const objs2 = [...hub.querySelectorAll(".obj")].filter(function (o) {{ return !o.hidden; }});
  objs2.forEach(function (o, i) {{ o.style.setProperty("--d", (0.04 + i * 0.055) + "s"); }});
  document.documentElement.classList.add("anim");
  /* Drop the class once it has played, so a later relayout does not replay it. */
  setTimeout(function () {{ document.documentElement.classList.remove("anim"); }}, 1400);
}}

apply(location.hash.replace("#", ""));
maybeHint();
playOpening();
window.addEventListener("resize", function () {{ layoutScatter(); maybeHint(); }});
if (document.fonts && document.fonts.ready) {{
  document.fonts.ready.then(layoutScatter);
}}

</script>
</body></html>
"""
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote index.html  {len(page):,} bytes  ·  {len(V)} views  ·  {len(c['souls'])} soul files")


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Signal panels for the profile README.

Runs inside a GitHub Action (standard library only). Pulls live data from the
GitHub GraphQL API, LeetCode and the profile-view counter, then renders three
SVG panels in the README's visual language:

  signal-overview.svg  — headline numbers + a 3D isometric contribution skyline
  signal-snake.svg     — the contribution snake, framed to match the canvas
  signal-leetcode.svg  — solved rings, difficulty split and a submission heatmap

If a source is unreachable, the last good values (cache.json) are reused so the
README never shows a broken card.
"""
import argparse, base64, datetime as dt, html, json, math, os, re, sys, urllib.request

# ---------------------------------------------------------------- palette ----
CANVAS = "#040406"; BG = "#07070B"; PANEL = "#0C0C13"; LINE = "#1D1D2A"; LINE2 = "#2A2A3C"
TXT = "#ECECF4"; SUB = "#B6B6C8"; MUTED = "#8A8AA0"; DIM = "#55556A"
VIO = "#8B7CF6"; VIO2 = "#B9B1FF"; MINT = "#5EEAD4"; WARM = "#F2A7C3"
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, "fonts.css")).read()

# ---------------------------------------------------------------- fetching ---
def http(url, data=None, headers=None, timeout=25):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def fetch_github(user, token):
    q = """query($login:String!){ user(login:$login){
      followers{totalCount}
      repositories(ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC, first:100){
        totalCount nodes{ stargazerCount languages(first:8, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name } } } } }
      contributionsCollection{ contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } } } }"""
    body = json.dumps({"query": q, "variables": {"login": user}}).encode()
    raw = http("https://api.github.com/graphql", body, {"Authorization": f"bearer {token}",
               "Content-Type": "application/json", "User-Agent": "profile-signal"})
    u = json.loads(raw)["data"]["user"]
    days = [(d["date"], d["contributionCount"]) for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    langs = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {"total": u["contributionsCollection"]["contributionCalendar"]["totalContributions"], "days": days,
            "repos": u["repositories"]["totalCount"], "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
            "followers": u["followers"]["totalCount"], "langs": sorted(langs.items(), key=lambda x: -x[1])[:5]}

def fetch_leetcode(handle):
    q = """query u($username:String!){ allQuestionsCount{difficulty count}
      matchedUser(username:$username){ profile{ranking}
        submitStatsGlobal{ acSubmissionNum{ difficulty count } }
        userCalendar{ streak totalActiveDays submissionCalendar } } }"""
    body = json.dumps({"query": q, "variables": {"username": handle}}).encode()
    raw = http("https://leetcode.com/graphql", body, {"Content-Type": "application/json",
               "Referer": f"https://leetcode.com/u/{handle}/", "User-Agent": "Mozilla/5.0 profile-signal"})
    d = json.loads(raw)["data"]; m = d["matchedUser"]
    tot = {x["difficulty"]: x["count"] for x in d["allQuestionsCount"]}
    ac = {x["difficulty"]: x["count"] for x in m["submitStatsGlobal"]["acSubmissionNum"]}
    cal = m.get("userCalendar") or {}
    subs = {int(k): v for k, v in json.loads(cal.get("submissionCalendar") or "{}").items()}
    return {"solved": ac.get("All", 0), "easy": [ac.get("Easy", 0), tot.get("Easy", 0)],
            "medium": [ac.get("Medium", 0), tot.get("Medium", 0)], "hard": [ac.get("Hard", 0), tot.get("Hard", 0)],
            "rank": m["profile"]["ranking"], "streak": cal.get("streak"), "active": cal.get("totalActiveDays"),
            "subs": {str(k): v for k, v in subs.items()}}

def fetch_views(user):
    svg = http(f"https://komarev.com/ghpvc/?username={user}&style=flat")
    nums = re.findall(r">\s*([\d,]+)\s*<", svg)
    return int(nums[-1].replace(",", "")) if nums else None

# ---------------------------------------------------------------- helpers ----
def esc(s): return html.escape(str(s))
def T(x, y, s, cls, size, fill=TXT, anchor="start", ls=0, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" fill="{fill}"{a}{l} {extra}>{esc(s)}</text>'
def fmt(n): return "—" if n is None else f"{n:,}"

BASE_DEFS = (f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#34344A"/>'
             f'<stop offset=".5" stop-color="#14141D"/><stop offset="1" stop-color="#34344A"/></linearGradient>'
             f'<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIO}" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{VIO2}"/><stop offset="1" stop-color="{MINT}"/></linearGradient>')
BASE_CSS = ("@keyframes trace{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}"
            "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
            "@media (prefers-reduced-motion:reduce){*{animation-play-state:paused!important}.rv{animation:none!important}}")

def canvas(W, H, body, title, css="", defs="", pad=12):
    """Full-bleed canvas tile with the README's container rails and an inset card."""
    cw, ch = W - 80, H - 2 * pad
    card = (f'<rect x="40.5" y="{pad+.5}" width="{cw-1}" height="{ch-1}" rx="16" fill="{BG}" stroke="url(#edge)"/>'
            f'<rect x="40.5" y="{pad+.5}" width="{cw-1}" height="{ch-1}" rx="16" fill="none" stroke="url(#beam)" stroke-width="1.4" '
            f'pathLength="1000" stroke-dasharray="90 910" stroke-linecap="round" style="animation:trace 14s linear infinite"/>')
    rails = f'<path d="M40.5 0V{H}M1159.5 0V{H}" stroke="{LINE}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><defs>{BASE_DEFS}{defs}</defs><style>{FONTS}{BASE_CSS}{css}</style>'
            f'<rect width="{W}" height="{H}" fill="{CANVAS}"/>{rails}{card}{body}</svg>')

def streaks(days):
    counts = [c for _, c in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0; longest = max(longest, run)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0: i -= 1          # today may simply not have started yet
    cur = 0
    while i >= 0 and counts[i] > 0: cur += 1; i -= 1
    return cur, longest

# ---------------------------------------------------------------- panels -----
def overview(g, views):
    W, H = 1200, 620
    cur, longest = streaks(g["days"])
    b, css = [], ["@keyframes rise{from{transform:scaleY(.02)}}", ".tw{animation:rise 1.1s cubic-bezier(.2,.8,.2,1) both}",
                  "@keyframes sweep{0%{transform:translateX(-120px);opacity:0}15%{opacity:1}85%{opacity:1}100%{transform:translateX(760px);opacity:0}}"]
    x0 = 84
    b.append(T(x0, 84, "Contribution signal, past twelve months", "ISI", 21, MUTED))
    b.append(T(x0 - 3, 170, fmt(g["total"]), "SG6", 84, TXT, ls=-3))
    b.append(T(x0, 202, "contributions", "JB4", 12, VIO2, ls=2.4))
    kp = [("current streak", f"{cur}d"), ("longest streak", f"{longest}d"), ("public repos", fmt(g["repos"])),
          ("stars earned", fmt(g["stars"])), ("followers", fmt(g["followers"])), ("profile views", fmt(views))]
    for i, (lab, val) in enumerate(kp):
        cx = x0 + (i % 2) * 180; cy = 262 + (i // 2) * 74
        b.append(f'<path d="M{cx} {cy-30}H{cx+150}" stroke="{LINE}"/>')
        b.append(T(cx, cy + 4, val, "SG6", 30, MINT if i == 0 and cur > 0 else TXT, ls=-.8))
        b.append(T(cx, cy + 26, lab, "JB4", 10.5, MUTED, ls=1.6))
    # languages ribbon
    ly = 500; tot = sum(s for _, s in g["langs"]) or 1; x = x0; wbar = 330
    cols = [VIO, VIO2, MINT, "#6C63B8", "#3E3A6E"]
    b.append(T(x0, ly - 14, "Languages by volume", "ISI", 17, MUTED))
    for i, (name, s) in enumerate(g["langs"]):
        w = max(wbar * s / tot, 3)
        b.append(f'<rect x="{x:.1f}" y="{ly}" width="{max(w-2,1):.1f}" height="8" rx="2" fill="{cols[i%5]}"/>')
        x += w
    lx = x0
    for i, (name, s) in enumerate(g["langs"][:4]):
        t = f"{name} {100*s/tot:.0f}%"
        b.append(f'<rect x="{lx}" y="{ly+24}" width="7" height="7" rx="1.5" fill="{cols[i%5]}"/>' + T(lx + 12, ly + 31, t, "JB4", 10.5, SUB))
        lx += 16 + len(t) * 6.6 + 14
    # ------------- isometric skyline -------------
    days = g["days"][-371:]
    first = dt.date.fromisoformat(days[0][0]); off = (first.weekday() + 1) % 7   # GitHub weeks start on Sunday
    cells = [((i + off) // 7, (i + off) % 7, c, dstr) for i, (dstr, c) in enumerate(days)]
    nz = sorted(c for *_, c, _ in cells if c > 0); mx = max(nz) if nz else 1
    q = lambda p: nz[min(len(nz) - 1, int(p * len(nz)))] if nz else 1
    th = [q(.25), q(.5), q(.75)]
    lvl = lambda c: 0 if c == 0 else (1 if c <= th[0] else 2 if c <= th[1] else 3 if c <= th[2] else 4)
    tops = ["#17172A", "#3A3278", "#5B4FC4", "#8B7CF6", "#8EF2E2"]
    lefts = ["#0E0E1A", "#231E4C", "#383084", "#5647B0", "#3FB8A6"]
    rights = ["#13132A", "#2D2763", "#473EA2", "#6F60D8", "#5ED8C6"]
    a, bb = 10.4, 5.2; ox, oy = 548, 214; k = .84
    order = sorted(cells, key=lambda c: (c[0] + c[1], c[0]))
    towers = []
    for w, d, c, dstr in order:
        cx = ox + (w - d) * a; cy = oy + (w + d) * bb
        h = 2.2 if c == 0 else 6 + 96 * math.sqrt(c / mx)
        A, B = a * k, bb * k; L = lvl(c)
        top = f"M{cx:.1f} {cy-h-B:.1f}L{cx+A:.1f} {cy-h:.1f}L{cx:.1f} {cy-h+B:.1f}L{cx-A:.1f} {cy-h:.1f}Z"
        lf = f"M{cx-A:.1f} {cy-h:.1f}L{cx:.1f} {cy-h+B:.1f}L{cx:.1f} {cy+B:.1f}L{cx-A:.1f} {cy:.1f}Z"
        rt = f"M{cx:.1f} {cy-h+B:.1f}L{cx+A:.1f} {cy-h:.1f}L{cx+A:.1f} {cy:.1f}L{cx:.1f} {cy+B:.1f}Z"
        anim = f' class="tw" style="transform-origin:{cx:.1f}px {cy+B:.1f}px;animation-delay:{.4+w*.028:.2f}s"' if c > 0 else ""
        towers.append(f'<g{anim}><path d="{lf}" fill="{lefts[L]}"/><path d="{rt}" fill="{rights[L]}"/><path d="{top}" fill="{tops[L]}"/></g>')
    b.append(f'<g>{"".join(towers)}</g>')
    # today marker
    w, d, c, _ = cells[-1]; cx = ox + (w - d) * a; cy = oy + (w + d) * bb
    b.append(f'<circle cx="{cx:.1f}" cy="{cy-(2.2 if c==0 else 6+96*math.sqrt(c/mx))-12:.1f}" r="3" fill="{MINT}" style="animation:pulse 1.8s infinite"/>')
    b.append(T(cx + 10, cy + 30, "today", "ISI", 15, MINT))
    wk = cells[0]; b.append(T(ox + (wk[0] - 6) * a - 14, oy + (wk[0] + 6) * bb - 8, "a year ago", "ISI", 15, MUTED, "end"))
    # month ticks along the front edge
    seen = set()
    for w, d, c, dstr in cells:
        m = dstr[:7]
        if d == 6 and m not in seen and dstr[8:10] <= "07":
            seen.add(m); tx = ox + (w - 7) * a; ty = oy + (w + 7) * bb + 6
            b.append(T(tx, ty, dt.date.fromisoformat(dstr).strftime("%b"), "JB4", 9.5, DIM, "middle", 1))
    b.append(T(1128, 84, "each tower is one day", "ISI", 17, MUTED, "end"))
    b.append(T(1128, 106, "height · √ contributions", "JB4", 10, DIM, "end", 1.4))
    legend_x = 1128 - 5 * 16
    for i in range(5):
        b.append(f'<rect x="{legend_x + i*16}" y="118" width="11" height="11" rx="2" fill="{tops[i]}"/>')
    return canvas(W, H, "".join(b), f"Contribution signal: {g['total']} contributions in the past year, current streak {cur} days, longest {longest} days, {g['repos']} public repos, profile views {fmt(views)}", "".join(css))

def snake(snake_svg):
    W, H = 1200, 330
    b = [T(84, 84, "The snake", "ISI", 21, MUTED),
         T(84, 132, "A year of commits,", "SG6", 30, TXT, ls=-.8), T(84, 168, "eaten one day at a time.", "SG6", 30, VIO2, ls=-.8),
         T(84, 272, "regenerated every twelve hours", "JB4", 10.5, DIM, ls=1.5)]
    if snake_svg:
        # Inline the snake's own markup (not an <image>): animations inside a nested
        # image never run when GitHub shows the SVG through an <img> tag.
        root = re.search(r"<svg\b[^>]*>", snake_svg)
        vb = re.search(r'viewBox="([^"]+)"', root.group(0))
        vbs = vb.group(1) if vb else "0 0 880 192"
        vw, vh = [float(v) for v in vbs.split()[2:4]]
        inner = snake_svg[root.end():snake_svg.rindex("</svg>")]
        inner = re.sub(r"<desc>.*?</desc>", "", inner, flags=re.S)
        iw = 620; ih = iw * vh / vw
        b.append(f'<rect x="482" y="{165-ih/2-16:.1f}" width="{iw+26}" height="{ih+32:.1f}" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(f'<svg x="495" y="{165-ih/2:.1f}" width="{iw}" height="{ih:.1f}" viewBox="{vbs}">{inner}</svg>')
    return canvas(W, H, "".join(b), "Contribution snake")

def leetcode(lc, handle):
    W, H = 1200, 520
    b = []
    css = ["@keyframes draw{from{stroke-dashoffset:1000}}", ".arc{animation:draw 2s cubic-bezier(.2,.8,.2,1) both}"]
    cx, cy = 250, 262
    rings = [("easy", MINT, 150), ("medium", VIO2, 124), ("hard", WARM, 98)]
    for i, (k, col, r) in enumerate(rings):
        s, t = lc[k] if lc else (0, 1)
        frac = s / t if t else 0
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="10"/>')
        b.append(f'<circle class="arc" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" '
                 f'pathLength="1000" stroke-dasharray="{max(frac*1000,4):.1f} 1000" transform="rotate(-90 {cx} {cy})" style="animation-delay:{.3+i*.25}s"/>')
    b.append(T(cx, cy + 14, fmt(lc["solved"]) if lc else "—", "SG6", 58, TXT, "middle", -2))
    b.append(T(cx, cy + 42, "solved", "JB4", 11, MUTED, "middle", 2.4))
    x0 = 470
    b.append(T(x0, 84, "Deliberate practice", "ISI", 21, MUTED))
    b.append(T(x0, 128, "One problem at a time.", "SG6", 32, TXT, ls=-.9))
    b.append(T(1128, 84, f"leetcode · {handle}", "JB4", 10.5, DIM, "end", 1.4))
    b.append(T(1128, 124, f"#{fmt(lc['rank'])}" if lc else "—", "SG6", 26, VIO2, "end", -.5))
    b.append(T(1128, 144, "global rank", "JB4", 10, MUTED, "end", 1.6))
    y = 188
    for k, col, _ in rings:
        s, t = lc[k] if lc else (0, 0)
        b.append(T(x0, y, k.capitalize(), "SG6", 16, TXT) + T(x0 + 250, y, f"{s} / {t}", "JB4", 13, SUB, "end"))
        b.append(f'<rect x="{x0}" y="{y+10}" width="250" height="3" rx="1.5" fill="{LINE}"/>'
                 f'<rect x="{x0}" y="{y+10}" width="{max(250*(s/t if t else 0),2):.1f}" height="3" rx="1.5" fill="{col}"/>')
        y += 50
    sx = 790
    extra = [("active days", fmt(lc.get("active")) if lc else "—"), ("best streak", f"{lc['streak']}d" if lc and lc.get("streak") is not None else "—")]
    for i, (lab, val) in enumerate(extra):
        b.append(T(sx + i * 170, 212, val, "SG6", 30, TXT, ls=-.8) + T(sx + i * 170, 236, lab, "JB4", 10.5, MUTED, ls=1.5))
    # submission heatmap, last 53 weeks
    today = dt.date.today(); start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    subs = {}
    for ts, v in (lc.get("subs", {}) if lc else {}).items():
        dd = dt.datetime.utcfromtimestamp(int(ts)).date(); subs[dd] = subs.get(dd, 0) + v
    vals = sorted(v for v in subs.values() if v > 0); mx = vals[-1] if vals else 1
    lv = lambda v: 0 if v == 0 else min(4, 1 + int(3 * math.sqrt(v / mx)))
    colr = ["#15151F", "#1E4A45", "#2C7A70", "#46B3A3", MINT]
    hx, hy, cs, gp = x0, 384, 10.4, 2.2
    b.append(T(x0, hy - 16, "Submissions, past year", "ISI", 17, MUTED))
    d0 = start; i = 0
    while d0 <= today:
        w, dd = divmod(i, 7)
        v = subs.get(d0, 0)
        b.append(f'<rect x="{hx + w*(cs+gp):.1f}" y="{hy + dd*(cs+gp):.1f}" width="{cs}" height="{cs}" rx="2" fill="{colr[lv(v)]}"/>')
        d0 += dt.timedelta(days=1); i += 1
    return canvas(W, H, "".join(b), f"LeetCode: {fmt(lc['solved']) if lc else 'unavailable'} problems solved", "".join(css))

# ---------------------------------------------------------------- main -------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True); ap.add_argument("--leetcode", required=True)
    ap.add_argument("--out", default="dist"); ap.add_argument("--prev", default="prev-cache.json")
    ap.add_argument("--mock", help="render from a JSON cache file instead of fetching")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    prev = {}
    for p in [a.mock, a.prev]:
        if p and os.path.exists(p):
            try: prev = json.load(open(p)); break
            except Exception: pass
    data = dict(prev)
    if not a.mock:
        for key, fn in [("github", lambda: fetch_github(a.user, os.environ["GITHUB_TOKEN"])),
                        ("leetcode", lambda: fetch_leetcode(a.leetcode)), ("views", lambda: fetch_views(a.user))]:
            try: data[key] = fn(); print(f"ok   {key}")
            except Exception as e: print(f"keep {key} (fetch failed: {e})", file=sys.stderr)
    json.dump(data, open(os.path.join(a.out, "cache.json"), "w"))
    snake_path = os.path.join(a.out, "snake.svg")
    snake_svg = open(snake_path).read() if os.path.exists(snake_path) else None
    g = data.get("github") or {"total": None, "days": [((dt.date.today() - dt.timedelta(days=i)).isoformat(), 0) for i in range(364, -1, -1)],
                               "repos": None, "stars": None, "followers": None, "langs": []}
    open(os.path.join(a.out, "signal-overview.svg"), "w").write(overview(g, data.get("views")))
    open(os.path.join(a.out, "signal-snake.svg"), "w").write(snake(snake_svg))
    open(os.path.join(a.out, "signal-leetcode.svg"), "w").write(leetcode(data.get("leetcode"), a.leetcode))
    print("wrote", os.listdir(a.out))

if __name__ == "__main__":
    main()

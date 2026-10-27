#!/usr/bin/env python3
"""Generates every animated SVG used by the profile README.

All images are self-hosted in assets/ so the README never depends on
third-party image services that can go down or rate-limit.
"""
import math, os, re, random, sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]
SI = sys.argv[2]  # simple-icons/icons directory
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "badges"), exist_ok=True)
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Liberation Mono', 'Courier New', monospace"
BG, PANEL, BORDER, TEXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
GREEN, TEAL, GOLD, PURPLE, BLUE = "#3fb950", "#39d0d8", "#e3b341", "#a371f7", "#58a6ff"

ICON_HEX = {
    "python": "3776AB", "r": "276DC3", "dart": "0175C2", "flutter": "02569B", "fastapi": "009688",
    "postgresql": "4169E1", "docker": "2496ED", "pytorch": "EE4C2C", "qgis": "589632",
    "googleearthengine": "4285F4", "huggingface": "FFD21E", "kotlin": "7F52FF", "javascript": "F7DF1E",
    "typescript": "3178C6", "supabase": "3FCF8E", "julia": "9558B2", "orcid": "A6CE39", "gmail": "EA4335",
    "github": "E6EDF3", "firebase": "DD2C00", "android": "3DDC84", "jupyter": "F37626", "pandas": "E70488",
    "numpy": "4DABCF", "scikitlearn": "F7931E", "googlecolab": "F9AB00", "cloudflare": "F38020",
    "flask": "3BABC3", "git": "F03C2E", "openstreetmap": "7EBC6F", "leaflet": "199900", "googlecloud": "4285F4",
    "duckdb": "FFF000", "sqlite": "4CA3D8", "opencv": "5C3EE8", "gradio": "F97316", "githubactions": "2088FF",
    "plotly": "7A76FF", "streamlit": "FF4B4B", "quarto": "4B9FD8", "openjdk": "E6EDF3", "sqlalchemy": "D71F00", "ubuntu": "E95420",
    "linux": "FCC624", "gdal": "5CAE58", "ultralytics": "5B8DEF", "minio": "C72E49", "k6": "7D64FF",
    "arcgis": "2C7AC3", "scipy": "8CAAE6", "pydantic": "E92063", "latex": "3DA5A5", "googlemaps": "4285F4",
    "qwen": "8F7CF7", "html5": "E34F26", "css": "8B5CF6", "zenodo": "4C9AFF", "researchgate": "00CCBB",
}


def icon_path(slug):
    txt = open(os.path.join(SI, slug + ".svg")).read()
    return re.search(r'<path d="([^"]+)"', txt).group(1)


def lighten(hx):
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    if lum >= 0.42:
        return hx
    k = 0.45
    return "".join(f"{int(v + (255 - v) * k):02X}" for v in (r, g, b))


def icon(slug, x, y, size, color=None, extra=""):
    """Brand icon (24x24 viewBox) placed with its top-left corner at x,y."""
    c = color or "#" + lighten(ICON_HEX.get(slug, "E6EDF3"))
    s = size / 24
    return f'<path transform="translate({x:.2f} {y:.2f}) scale({s:.4f})" fill="{c}" d="{icon_path(slug)}" {extra}/>'


def svg(w, h, body, style="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<style>{style}@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>'
            f'{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def text_w(s, size, bold=False):
    """Rough width estimate for proportional sans text (used with textLength)."""
    narrow = set("il.,:;|!'ftjI ")
    wide = set("mwMWQOGD@%")
    w = 0
    for ch in s:
        if ch in narrow:
            w += 0.32
        elif ch in wide:
            w += 0.82
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        else:
            w += 0.54
    return w * size * (1.06 if bold else 1)


# ---------------------------------------------------------------- header
def header():
    W, H = 1280, 340
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H - 60):.0f}" r="{rnd.choice([0.8, 1.1, 1.5]):.1f}" '
        f'class="tw" style="animation-delay:{rnd.uniform(0, 4):.2f}s;animation-duration:{rnd.uniform(2.5, 5):.2f}s"/>'
        for _ in range(70))
    cx, cy, R = 1035, 168, 118
    # meridians: rx = R*|sin(phase + wt)| sampled to simulate a spinning globe
    mer = ""
    for k in range(6):
        ph = k * math.pi / 6
        vals = ";".join(f"{R * abs(math.sin(ph + 2 * math.pi * i / 48)):.1f}" for i in range(49))
        mer += (f'<ellipse cx="{cx}" cy="{cy}" rx="{R * abs(math.sin(ph)):.1f}" ry="{R}" fill="none" '
                f'stroke="#7ee2b8" stroke-opacity=".35" stroke-width="1">'
                f'<animate attributeName="rx" dur="16s" repeatCount="indefinite" values="{vals}"/></ellipse>')
    lat = "".join(
        f'<ellipse cx="{cx}" cy="{cy + R * math.sin(a):.1f}" rx="{R * math.cos(a):.1f}" ry="{R * math.cos(a) * 0.12:.1f}" '
        f'fill="none" stroke="#7ee2b8" stroke-opacity=".25"/>' for a in (-1.0, -0.5, 0, 0.5, 1.0))
    land_shapes = [
        "M0 -30 q22 -18 44 -6 q16 10 6 26 q-10 18 -30 12 q-24 -6 -20 -32z",
        "M70 10 q18 -10 34 2 q10 12 -2 24 q-14 10 -26 0 q-12 -10 -6 -26z",
        "M120 -50 q20 -6 30 8 q6 14 -10 18 q-20 2 -20 -26z",
        "M30 40 q14 -4 22 8 q4 14 -10 16 q-16 0 -12 -24z",
        "M150 30 q16 -12 30 0 q8 14 -8 22 q-18 4 -22 -22z",
    ]
    land = "".join(f'<path d="{d}" fill="url(#land)" transform="scale({R / 100:.2f})"/>' for d in land_shapes)
    # two copies 2R apart scrolling left->right gives an endless spin
    globe = f'''
  <g clip-path="url(#gclip)">
    <circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#ocean)"/>
    <g transform="translate({cx - 3 * R} {cy})">
      <g>{land}<g transform="translate({2 * R} 0)">{land}</g><g transform="translate({4 * R} 0)">{land}</g>
        <animateTransform attributeName="transform" type="translate" from="0 0" to="{2 * R} 0" dur="16s" repeatCount="indefinite"/>
      </g>
    </g>
    {mer}{lat}
    <circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#shade)"/>
    <g transform="translate({cx} {cy})"><g class="sweep"><path d="M0 0 L{R} 0 A{R} {R} 0 0 1 {R * math.cos(0.7):.1f} {R * math.sin(0.7):.1f} Z" fill="url(#sweep)"/></g></g>
  </g>
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#7ee2b8" stroke-opacity=".6" stroke-width="1.5"/>
  <circle cx="{cx - 28}" cy="{cy + 22}" r="4" fill="{GOLD}"/>
  <circle cx="{cx - 28}" cy="{cy + 22}" r="4" fill="none" stroke="{GOLD}" stroke-width="2">
    <animate attributeName="r" values="4;22" dur="2.4s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="1;0" dur="2.4s" repeatCount="indefinite"/>
  </circle>'''

    def orbit(rx, ry, tilt, dur, sat_color, sid, delay=0):
        p = f"M{cx + rx} {cy} A{rx} {ry} 0 1 1 {cx - rx} {cy} A{rx} {ry} 0 1 1 {cx + rx} {cy}"
        back = f"M{cx - rx} {cy} A{rx} {ry} 0 0 0 {cx + rx} {cy}"
        front = f"M{cx + rx} {cy} A{rx} {ry} 0 0 1 {cx - rx} {cy}"
        sat = f'''<g>
        <rect x="-10" y="-3" width="7" height="6" fill="{sat_color}" opacity=".9"/>
        <rect x="3" y="-3" width="7" height="6" fill="{sat_color}" opacity=".9"/>
        <rect x="-3" y="-4" width="6" height="8" rx="1.5" fill="#e6edf3"/>
        <animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite" path="{p}"/>
        <animate attributeName="opacity" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" values="1;1;0;0;1" keyTimes="0;0.49;0.5;0.99;1"/>
      </g>'''
        back_svg = f'<path d="{back}" fill="none" stroke="{sat_color}" stroke-opacity=".3" stroke-dasharray="4 6" transform="rotate({tilt} {cx} {cy})"/>'
        front_svg = (f'<g transform="rotate({tilt} {cx} {cy})"><path d="{front}" fill="none" stroke="{sat_color}" '
                     f'stroke-opacity=".7" stroke-width="1.4" stroke-dasharray="4 6" class="dash"/>{sat}</g>')
        return back_svg, front_svg

    b1, f1 = orbit(200, 52, -16, 9, TEAL, "s1")
    b2, f2 = orbit(172, 38, 22, 13, GOLD, "s2", delay=-4)

    chips = [("Teledetección", TEAL), ("Visión por computador", GREEN), ("Epidemiología", GOLD), ("Geomática", PURPLE), ("LLMs on-device", BLUE)]
    cx0, chip_svg = 64, ""
    for i, (label, col) in enumerate(chips):
        w = text_w(label, 14, True) + 30
        chip_svg += (f'<g class="up" style="animation-delay:{0.9 + i * 0.15:.2f}s"><g transform="translate({cx0:.0f} 236)">'
                     f'<rect width="{w:.0f}" height="30" rx="15" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".7"/>'
                     f'<circle cx="14" cy="15" r="3.5" fill="{col}"/>'
                     f'<text x="24" y="20" font-family="{SANS}" font-size="14" font-weight="600" fill="{TEXT}" textLength="{w - 32:.0f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text></g></g>')
        cx0 += w + 10

    wave = " ".join(f"{x},{H - 38 + 10 * math.sin(x / 40):.1f}" for x in range(0, W + 41, 8))
    body = f'''
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06101c"/><stop offset=".55" stop-color="#0a2219"/><stop offset="1" stop-color="#071526"/></linearGradient>
  <radialGradient id="glow" cx="{cx / W:.3f}" cy="{cy / H:.3f}" r=".35"><stop offset="0" stop-color="#2ea043" stop-opacity=".35"/><stop offset="1" stop-color="#2ea043" stop-opacity="0"/></radialGradient>
  <radialGradient id="ocean" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#1b6f8a"/><stop offset="1" stop-color="#0b2740"/></radialGradient>
  <linearGradient id="land" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#56d364"/><stop offset="1" stop-color="#238636"/></linearGradient>
  <radialGradient id="shade" cx=".3" cy=".28" r=".85"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity=".0"/><stop offset="1" stop-color="{TEAL}" stop-opacity=".35"/></linearGradient>
  <clipPath id="gclip"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#7ee787"/><stop offset=".5" stop-color="#39d0d8"/><stop offset="1" stop-color="#7ee787"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="nameb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7ee787"/><stop offset="1" stop-color="#39d0d8"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>
<g fill="#fff">{stars}</g>
<g stroke="#7ee2b8" stroke-opacity=".05">{"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 40))}{"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 40))}</g>
<polyline points="{wave}" fill="none" stroke="{GREEN}" stroke-opacity=".55" stroke-width="2" stroke-dasharray="10 14" class="flow"/>
<polyline points="{wave}" fill="none" stroke="{TEAL}" stroke-opacity=".25" stroke-width="1" transform="translate(0 10)"/>
{b1}{b2}
{globe}
{f1}{f2}
<g class="up" style="animation-delay:.1s"><text x="64" y="92" font-family="{MONO}" font-size="16" fill="{GREEN}" letter-spacing="2">$ whoami</text></g>
<g class="up" style="animation-delay:.3s"><text x="62" y="150" font-family="{SANS}" font-size="50" font-weight="800" fill="url(#nameb)" textLength="660" lengthAdjust="spacingAndGlyphs">Jesús Enrique Flores-Riera</text></g>
<g class="up" style="animation-delay:.6s"><text x="64" y="194" font-family="{SANS}" font-size="21" fill="{TEXT}" textLength="640" lengthAdjust="spacingAndGlyphs">Ingeniero Agrónomo · MSc(c) Geomática @ Universidad Nacional de Colombia</text></g>
{chip_svg}
'''
    style = (".tw{animation:tw 3s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}"
             ".dash{animation:dash 3s linear infinite}@keyframes dash{to{stroke-dashoffset:-40}}"
             ".flow{animation:flow 4s linear infinite}@keyframes flow{to{stroke-dashoffset:-96}}"
             ".sweep{animation:spin 6s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
             ".up{animation:up .9s cubic-bezier(.2,.7,.2,1) both}@keyframes up{from{transform:translateY(10px)}to{transform:none}}")
    write("header.svg", svg(W, H, body, style, "Jesús Enrique Flores-Riera — Ingeniero Agrónomo, Geomática e IA"))


# ---------------------------------------------------------------- typing
def typing():
    lines = [
        "Visión por computador para fitopatología (YOLO · CNNs)",
        "Teledetección: Sentinel-1/2 · InSAR · UAV multiespectral",
        "Apps offline-first: Flutter + FastAPI + PostGIS",
        "LLMs pequeños on-device: corpus → QLoRA → GGUF",
        "Plugins QGIS: GPR fenología · GPBoost · InSAR",
        "Epidemiología agroclimática y modelos espaciotemporales",
    ]
    W, H, FS = 900, 54, 21
    CW = FS * 0.6
    D = 4.6
    T = D * len(lines)
    BEG = round(0.6 * D, 2)  # start in the middle of the first line's hold
    body = ""
    for i, ln in enumerate(lines):
        n = len(ln)
        tw = n * CW
        x0 = (W - tw) / 2
        t_type, t_hold, t_erase = 0.42 * D, 0.38 * D, 0.14 * D
        pts = [(0, 0)]
        start = i * D
        for k in range(1, n + 1):
            pts.append((start + k * t_type / n, k * CW))
        es = start + t_type + t_hold
        for k in range(1, n + 1):
            pts.append((es + k * t_erase / n, (n - k) * CW))
        cleaned = []
        for t, v in pts:
            t = round(t / T, 5)
            if cleaned and t <= cleaned[-1][0]:
                t = cleaned[-1][0] + 0.00001
            cleaned.append((t, v))
        if cleaned[-1][0] < 1:
            cleaned.append((1, 0))
        kt = ";".join(f"{t:.5f}" for t, _ in cleaned)
        wv = ";".join(f"{v:.1f}" for _, v in cleaned)
        xv = ";".join(f"{x0 + v:.1f}" for _, v in cleaned)
        on = [(0, 0), (round(start / T, 5), 1), (round((es + t_erase) / T + 0.0001, 5), 0)]
        if i == 0:
            on = [(0, 1), (round((es + t_erase) / T, 5), 0)]
        okt = ";".join(f"{t:.5f}" for t, _ in on)
        ov = ";".join(str(v) for _, v in on)
        body += f'''
<clipPath id="c{i}"><rect x="{x0:.1f}" y="0" width="{tw if i == 0 else 0:.1f}" height="{H}"><animate attributeName="width" dur="{T}s" begin="-{BEG}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{wv}"/></rect></clipPath>
<text clip-path="url(#c{i})" x="{x0:.1f}" y="35" font-family="{MONO}" font-size="{FS}" fill="url(#tg)" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(ln)}</text>
<rect y="13" width="3" height="28" fill="{GREEN}" opacity="{1 if i == 0 else 0}" x="{x0 + (tw if i == 0 else 0):.1f}">
  <animate attributeName="x" dur="{T}s" begin="-{BEG}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{xv}"/>
  <animate attributeName="opacity" dur="{T}s" begin="-{BEG}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{okt}" values="{ov}"/>
</rect>'''
    defs = f'<defs><linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="#7ee787"/><stop offset="1" stop-color="{TEAL}"/></linearGradient></defs>'
    write("typing.svg", svg(W, H, defs + body, "", "; ".join(lines)))


# ---------------------------------------------------------------- divider
def divider():
    W, H = 1280, 26
    body = f'''<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></linearGradient>
<radialGradient id="p"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient></defs>
<rect x="0" y="12" width="{W}" height="2" fill="url(#d)" opacity=".7"/>
<circle cy="13" r="9" fill="url(#p)"><animate attributeName="cx" values="-20;{W + 20}" dur="5s" repeatCount="indefinite"/></circle>
<circle cy="13" r="6" fill="url(#p)" opacity=".7"><animate attributeName="cx" values="{W + 20};-20" dur="7s" repeatCount="indefinite"/></circle>'''
    write("divider.svg", svg(W, H, body, "", "separador"))


# ---------------------------------------------------------------- badges
def badge(fname, label, color, slug=None, custom=None, fg="#fff"):
    H = 32
    tw = text_w(label.upper(), 12, True) + 4
    W = 14 + 18 + 8 + tw + 14
    ic = ""
    if slug:
        ic = icon(slug, 14, 7, 18, fg)
    elif custom:
        ic = custom
    body = f'''<rect width="{W:.0f}" height="{H}" rx="7" fill="{color}"/>
<rect width="{W:.0f}" height="{H}" rx="7" fill="url(#sh)"/>
<defs><linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient></defs>
{ic}
<text x="40" y="21" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing=".6" fill="{fg}" textLength="{tw:.0f}" lengthAdjust="spacingAndGlyphs">{esc(label.upper())}</text>'''
    write(os.path.join("badges", fname), svg(round(W), H, body, "", label))


def badges():
    li = (f'<rect x="14" y="7" width="18" height="18" rx="3.5" fill="#fff"/>'
          f'<text x="16.5" y="21.5" font-family="{SANS}" font-weight="800" font-size="13" fill="#0A66C2">in</text>')
    mail = ('<path transform="translate(14 8)" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round" '
            'd="M1 1h16v14H1z M1 1l8 7 8-7"/>')
    pin = ('<path transform="translate(15 6)" fill="#fff" d="M8 0C3.6 0 0 3.5 0 7.9 0 13.6 8 20 8 20s8-6.4 8-12.1C16 3.5 12.4 0 8 0zm0 11a3.2 3.2 0 1 1 0-6.4A3.2 3.2 0 0 1 8 11z"/>')
    badge("linkedin.svg", "LinkedIn", "#0A66C2", custom=li)
    badge("huggingface.svg", "Hugging Face", "#2b2b2b", slug="huggingface", fg="#FFD21E")
    badge("orcid.svg", "ORCID", "#A6CE39", slug="orcid", fg="#fff")
    badge("gmail.svg", "Gmail", "#D14836", slug="gmail")
    badge("unal.svg", "Correo UNAL", "#1f6f43", custom=mail)
    badge("location.svg", "Bogotá, Colombia", "#2E8B57", custom=pin)


# ---------------------------------------------------------------- orbit
def orbit():
    S = 460
    c = S / 2
    rings = [
        (92, 26, False, ["python", "r", "dart", "julia"]),
        (150, 40, True, ["pytorch", "ultralytics", "huggingface", "scikitlearn", "opencv", "pandas"]),
        (205, 60, False, ["qgis", "googleearthengine", "gdal", "postgresql", "fastapi", "flutter", "docker", "kotlin", "supabase", "githubactions"]),
    ]
    body = f'''<defs><radialGradient id="core"><stop offset="0" stop-color="#2ea043"/><stop offset="1" stop-color="#0b3d22"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{GREEN}" stop-opacity=".35"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient></defs>
<circle cx="{c}" cy="{c}" r="{c}" fill="url(#halo)" opacity=".5"/>'''
    for i, (r, dur, rev, slugs) in enumerate(rings):
        cls = "rev" if rev else "fwd"
        nodes = ""
        for k, s in enumerate(slugs):
            a = 2 * math.pi * k / len(slugs) + i * 0.4
            x, y = r * math.cos(a), r * math.sin(a)
            col = "#" + ICON_HEX.get(s, "E6EDF3")
            nodes += (f'<g transform="translate({x:.1f} {y:.1f})"><g class="{"fwd" if rev else "rev"}" style="animation-duration:{dur}s">'
                      f'<circle r="21" fill="{PANEL}" stroke="{col}" stroke-opacity=".8" stroke-width="1.5"/>'
                      f'{icon(s, -11, -11, 22)}</g></g>')
        body += (f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{BORDER}" stroke-width="1.2"/>'
                 f'<g transform="translate({c} {c})"><g class="{cls}" style="animation-duration:{dur}s">'
                 f'<circle r="{r}" fill="none" stroke="{GREEN}" stroke-opacity=".5" stroke-width="1.6" stroke-dasharray="2 {r * 0.35:.0f}"/>'
                 f'{nodes}</g></g>')
    body += f'''<circle cx="{c}" cy="{c}" r="44" fill="none" stroke="{GREEN}" stroke-width="2"><animate attributeName="r" values="44;62" dur="2.6s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="2.6s" repeatCount="indefinite"/></circle>
<circle cx="{c}" cy="{c}" r="44" fill="url(#core)" stroke="#7ee787" stroke-width="2"/>
<text x="{c}" y="{c + 11}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="32" fill="#fff">JF</text>'''
    style = (".fwd{animation:spin 40s linear infinite;transform-origin:0 0}"
             ".rev{animation:spin 40s linear infinite reverse;transform-origin:0 0}"
             "@keyframes spin{to{transform:rotate(360deg)}}")
    write("orbit.svg", svg(S, S, body, style, "Órbita de tecnologías"))


# ---------------------------------------------------------------- skills tiles
def tiles(fname, items, title):
    per_row, TW, TH, G = 8, 100, 100, 10
    rows = math.ceil(len(items) / per_row)
    W = per_row * TW + (per_row - 1) * G + 4
    H = rows * TH + (rows - 1) * G + 18
    body = ""
    for i, (slug, label) in enumerate(items):
        r, cc = divmod(i, per_row)
        # centre the last row
        n_in_row = min(per_row, len(items) - r * per_row)
        off = (per_row - n_in_row) * (TW + G) / 2
        x, y = 2 + off + cc * (TW + G), 6 + r * (TH + G)
        col = "#" + ICON_HEX.get(slug, "E6EDF3")
        lw = min(text_w(label, 12, True), TW - 12)
        body += f'''<g transform="translate({x:.1f} {y})"><g class="in" style="animation-delay:{i * 0.07:.2f}s">
<rect width="{TW}" height="{TH}" rx="14" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="18" y="0" width="{TW - 36}" height="3" rx="1.5" fill="{col}"/>
<g transform="translate({TW / 2 - 19} 18)"><g class="fl" style="animation-delay:{(i % 5) * 0.4:.1f}s">{icon(slug, 0, 0, 38)}</g></g>
<text x="{TW / 2}" y="83" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="600" fill="{TEXT}" textLength="{lw:.0f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>
</g></g>'''
    style = (".in{animation:in .7s cubic-bezier(.2,.7,.2,1) both}@keyframes in{from{transform:translateY(6px)}to{transform:none}}"
             ".fl{animation:fl 3.2s ease-in-out infinite alternate}@keyframes fl{from{transform:translateY(-2px)}to{transform:translateY(3px)}}")
    write(fname, svg(round(W), H, body, style, title + ": " + ", ".join(l for _, l in items)))


# ---------------------------------------------------------------- project cards
def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


def card(fname, title, desc, tags, slug, accent, private=False, year=""):
    W, H = 440, 236
    lines = wrap(desc, 58)[:4]
    desc_svg = "".join(
        f'<text x="24" y="{104 + i * 20}" font-family="{SANS}" font-size="13.2" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(lines))
    tx, tag_svg = 24, ""
    for t, tc in tags:
        w = text_w(t, 11.5, True) + 18
        if tx + w > W - 20:
            break
        tag_svg += (f'<g transform="translate({tx:.0f} 194)"><rect width="{w:.0f}" height="22" rx="11" fill="{tc}" fill-opacity=".14" stroke="{tc}" stroke-opacity=".6"/>'
                    f'<text x="9" y="15" font-family="{SANS}" font-size="11.5" font-weight="600" fill="{TEXT}" textLength="{w - 18:.0f}" lengthAdjust="spacingAndGlyphs">{esc(t)}</text></g>')
        tx += w + 7
    status = "PRIVADO" if private else "PÚBLICO"
    scol = GOLD if private else GREEN
    sw = text_w(status, 10.5, True) + 22
    lock = (f'<path transform="translate({W - 20 - sw + 8} 27)" fill="{scol}" d="M2 5V3.5a3 3 0 0 1 6 0V5h.5a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-4a.5.5 0 0 1 .5-.5zm1.2 0h3.6V3.5a1.8 1.8 0 0 0-3.6 0z"/>'
            if private else f'<circle cx="{W - 20 - sw + 12}" cy="32" r="3.5" fill="{scol}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>')
    ttw = min(text_w(title, 19, True), W - 86 - 34 - sw)
    perim = 2 * (W - 2 + H - 2)
    body = f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#161b22"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
<radialGradient id="gl" cx="0" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#bg)" stroke="{BORDER}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#gl)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-dasharray="90 {perim - 90:.0f}" class="run"/>
<g transform="translate(48 44)"><g class="spin"><circle r="25" fill="none" stroke="{accent}" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="3 5"/></g></g>
<circle cx="48" cy="44" r="19" fill="{PANEL}" stroke="{accent}" stroke-opacity=".5"/>
{icon(slug, 37, 33, 22) if slug else ""}
<text x="86" y="40" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}" textLength="{ttw:.0f}" lengthAdjust="spacingAndGlyphs">{esc(title)}</text>
<text x="86" y="60" font-family="{MONO}" font-size="11.5" fill="{accent}">{esc(year)}</text>
<g><rect x="{W - 20 - sw}" y="22" width="{sw:.0f}" height="20" rx="10" fill="{scol}" fill-opacity=".12" stroke="{scol}" stroke-opacity=".6"/>{lock}
<text x="{W - 20 - sw + 18}" y="36" font-family="{SANS}" font-size="10.5" font-weight="700" letter-spacing=".5" fill="{scol}">{status}</text></g>
<line x1="24" y1="78" x2="{W - 24}" y2="78" stroke="{BORDER}"/>
{desc_svg}
{tag_svg}'''
    style = (f".run{{animation:run 7s linear infinite}}@keyframes run{{to{{stroke-dashoffset:-{perim:.0f}}}}}"
             ".spin{animation:spin 9s linear infinite;transform-origin:0 0}@keyframes spin{to{transform:rotate(360deg)}}")
    write(os.path.join("projects", fname), svg(W, H, body, style, f"{title}: {desc}"))


# ---------------------------------------------------------------- stats
def stats(kpis):
    W, H = 880, 158
    n = len(kpis)
    G = 12
    TW = (W - (n - 1) * G - 4) / n
    body = ""
    for i, (num, label, col) in enumerate(kpis):
        x = 2 + i * (TW + G)
        nw = min(text_w(num, 26, True), 62)
        lw = min(text_w(label, 12.5), TW - 20)
        body += f'''<g transform="translate({x:.1f} 2)"><g class="in" style="animation-delay:{i * 0.12:.2f}s">
<rect width="{TW:.1f}" height="{H - 12}" rx="16" fill="{PANEL}" stroke="{BORDER}"/>
<g transform="translate({TW / 2:.1f} 56)"><g class="spin" style="animation-duration:{8 + i * 2}s"><circle r="44" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-dasharray="40 14 8 14"/></g>
<g class="spin r" style="animation-duration:{12 + i}s"><circle r="37" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="2 6"/></g></g>
<text x="{TW / 2:.1f}" y="65" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="{TEXT}" textLength="{nw:.0f}" lengthAdjust="spacingAndGlyphs">{esc(num)}</text>
<text x="{TW / 2:.1f}" y="128" text-anchor="middle" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{MUTED}" textLength="{lw:.0f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>
</g></g>'''
    style = (".in{animation:in .7s cubic-bezier(.2,.7,.2,1) both}@keyframes in{from{transform:translateY(6px)}to{transform:none}}"
             ".spin{animation:spin 8s linear infinite;transform-origin:0 0}.r{animation-direction:reverse}@keyframes spin{to{transform:rotate(360deg)}}")
    write("stats.svg", svg(W, H, body, style, "Estadísticas: " + "; ".join(f"{a} {b}" for a, b, _ in kpis)))


def langs(data):
    W = 880
    RH = 34
    H = 56 + len(data) * RH + 10
    total = sum(v for _, v, _ in data)
    BX, BW = 200, 560
    body = f'''<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{PANEL}" stroke="{BORDER}"/>
<text x="28" y="38" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">Lenguajes en mis repositorios</text>
<text x="{W - 28}" y="38" text-anchor="end" font-family="{SANS}" font-size="12" fill="{MUTED}">líneas de código propias · públicos + privados</text>'''
    for i, (name, v, col) in enumerate(data):
        y = 62 + i * RH
        pct = 100 * v / total
        w = max(BW * v / data[0][1], 4)
        body += f'''<text x="28" y="{y + 15}" font-family="{SANS}" font-size="13" font-weight="600" fill="{TEXT}">{esc(name)}</text>
<rect x="{BX}" y="{y + 3}" width="{BW}" height="14" rx="7" fill="{BG}"/>
<g transform="translate({BX} {y + 3})"><rect width="{w:.1f}" height="14" rx="7" fill="{col}"/></g>
<circle cx="{BX + w - 7:.1f}" cy="{y + 10}" r="7" fill="{col}" opacity="0"><animate attributeName="r" values="7;13;7" dur="2.4s" begin="{1.6 + i * 0.25:.2f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.45;0" dur="2.4s" begin="{1.6 + i * 0.25:.2f}s" repeatCount="indefinite"/></circle>
<text x="{W - 28}" y="{y + 15}" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{pct:4.1f}%</text>'''
    defs = ""
    style = ".grow{animation:grow 1.4s cubic-bezier(.2,.7,.2,1) both;transform-origin:0 0}@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    write("languages.svg", svg(W, H, defs + body, style, "Lenguajes: " + ", ".join(f"{n} {100 * v / total:.1f}%" for n, v, _ in data)))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1280, 120

    def wave(amp, ph, y0):
        pts = []
        for x in range(0, 2 * W + 1, 20):
            pts.append(f"{x},{y0 + amp * math.sin(2 * math.pi * x / 640 + ph):.1f}")
        return "M" + " L".join(pts) + f" L{2 * W},{H} L0,{H} Z"

    body = f'''<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#0a2219"/><stop offset=".5" stop-color="#145c3a"/><stop offset="1" stop-color="#0b3a4a"/></linearGradient></defs>
<g opacity=".45"><path d="{wave(14, 0, 46)}" fill="url(#f)"><animateTransform attributeName="transform" type="translate" from="0 0" to="-640 0" dur="9s" repeatCount="indefinite"/></path></g>
<g opacity=".7"><path d="{wave(10, 1.7, 62)}" fill="url(#f)"><animateTransform attributeName="transform" type="translate" from="-640 0" to="0 0" dur="12s" repeatCount="indefinite"/></path></g>
<path d="{wave(8, 3.1, 80)}" fill="url(#f)"><animateTransform attributeName="transform" type="translate" from="0 0" to="-640 0" dur="15s" repeatCount="indefinite"/></path>
<text x="{W / 2}" y="108" text-anchor="middle" font-family="{SANS}" font-size="13" fill="#c9d1d9" opacity=".85">De la parcela al píxel — y de vuelta a la parcela</text>'''
    write("footer.svg", svg(W, H, body, "", "pie de página"))


if __name__ == "__main__":
    header(); typing(); divider(); badges(); orbit(); footer()

    tiles("skills-lang.svg", [
        ("python", "Python"), ("dart", "Dart"), ("kotlin", "Kotlin"), ("openjdk", "Java"),
        ("javascript", "JavaScript"), ("typescript", "TypeScript"), ("r", "R"), ("julia", "Julia"),
        ("postgresql", "SQL"), ("html5", "HTML5"), ("css", "CSS"), ("quarto", "Quarto"),
    ], "Lenguajes")
    tiles("skills-ai.svg", [
        ("pytorch", "PyTorch"), ("ultralytics", "YOLO"), ("huggingface", "Transformers"), ("scikitlearn", "scikit-learn"),
        ("opencv", "OpenCV"), ("pandas", "pandas"), ("numpy", "NumPy"), ("scipy", "SciPy"),
        ("jupyter", "Jupyter"), ("googlecolab", "Colab"), ("flask", "Flask"), ("streamlit", "Streamlit"),
    ], "IA y ciencia de datos")
    tiles("skills-geo.svg", [
        ("qgis", "QGIS / PyQGIS"), ("googleearthengine", "Earth Engine"), ("gdal", "GDAL · rasterio"), ("postgresql", "PostGIS"),
        ("arcgis", "ArcPy"), ("openstreetmap", "OSM · Overpass"), ("leaflet", "Leaflet"),
    ], "Geoespacial")
    tiles("skills-dev.svg", [
        ("flutter", "Flutter"), ("android", "Android"), ("fastapi", "FastAPI"), ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"), ("docker", "Docker"), ("minio", "MinIO · S3"), ("duckdb", "DuckDB"),
        ("supabase", "Supabase"), ("firebase", "Firebase"), ("sqlite", "SQLite"), ("cloudflare", "Cloudflare"),
        ("githubactions", "GH Actions"), ("k6", "k6"), ("git", "Git"), ("ubuntu", "Linux · WSL"),
    ], "Backend, móvil y DevOps")

    P = [
        ("purdue-maize.svg", "Purdue Maize Platform", "Plataforma digital para monitorear y predecir enfermedades foliares del maíz: app offline-first, API asíncrona, ingesta de drones y satélites, motor de decisiones trazable.",
         [("Flutter", "#02569B"), ("FastAPI", "#009688"), ("PostGIS", "#4169E1"), ("MinIO", "#C72E49"), ("TiTiler", TEAL)], "flutter", GOLD, True, "2026 · UNAL × Purdue"),
        ("maize-llm.svg", "LLM fitosanitario", "Minería de corpus científico, dataset bilingüe EN/ES en 3 niveles, adaptación de dominio y ajuste fino QLoRA de modelos 0.5–4B, cuantizados a GGUF para correr en el teléfono.",
         [("PyTorch", "#EE4C2C"), ("PEFT · TRL", PURPLE), ("QLoRA", GOLD), ("GGUF", GREEN)], "huggingface", PURPLE, True, "2026 · LLMs on-device"),
        ("insar.svg", "InSAR Toolbox for QGIS", "Interferometría radar dentro de QGIS: búsqueda en 4 catálogos, corregistro, interferograma, desenrollado, series SBAS y phase linking orquestando grafos ESA SNAP.",
         [("PyQGIS", "#589632"), ("ESA SNAP", BLUE), ("Sentinel-1", TEAL), ("SBAS", GOLD)], "qgis", TEAL, True, "2026 · Radar / SAR"),
        ("gee-gpr.svg", "GEE GPR Phenology", "Plugin QGIS para recuperar variables biofísicas Sentinel-2 con Gaussian Process Regression, rellenar huecos temporales y extraer fenología (LSP).",
         [("Earth Engine", "#4285F4"), ("GPR", GREEN), ("Sentinel-2", TEAL), ("PyQGIS", "#589632")], "googleearthengine", GREEN, False, "v1.5.7 · plugin QGIS"),
        ("pea-drone.svg", "pea_drone", "Fenotipado UAV multiespectral de arveja y garbanzo (2017-2019): calibración radiométrica, rasgos por parcela, heredabilidad, G×E y modelos LASSO / XGBoost.",
         [("rasterio", "#5CAE58"), ("scikit-learn", "#F7931E"), ("XGBoost", GOLD), ("statsmodels", BLUE)], "python", BLUE, False, "2026 · fenómica"),
        ("powderyvision.svg", "PowderyVision", "Detección y severidad de oídio en arveja y tomate: clasificación YOLOv11-cls, segmentación foliar YOLOv11-seg y área de lesión en una app web Flask.",
         [("YOLOv11", "#5B8DEF"), ("Flask", "#3BABC3"), ("OpenCV", "#5C3EE8"), ("CNNs", "#EE4C2C")], "ultralytics", GREEN, False, "Visión por computador"),
        ("gpboost.svg", "GPBoost Spatial Predictor", "Plugin QGIS que combina tree-boosting y procesos gaussianos para predicción espacial con efectos aleatorios, directo sobre capas del proyecto.",
         [("GPBoost", GREEN), ("PyQGIS", "#589632"), ("Kriging", TEAL)], "qgis", "#589632", False, "Plugin QGIS"),
        ("hevea.svg", "Hevea agroclima", "Caracterización agroclimática 2011-2025 para la epidemiología de enfermedades foliares del caucho en el Meta: IDEAM, CHIRPS, AgERA5 e IMERG.",
         [("pandas", "#E70488"), ("Earth Engine", "#4285F4"), ("CHIRPS", TEAL), ("IDEAM", GOLD)], "googleearthengine", GOLD, False, "Epidemiología"),
        ("sar-guide.svg", "SAR multisensor", "Flujos para interpretar SAR banda C (Sentinel-1) y L (ALOS-2) junto a óptico según la guía CEOS, más exploración de metadatos Umbra (banda X) desde S3.",
         [("Sentinel-1", TEAL), ("ALOS-2", PURPLE), ("boto3 · S3", GOLD), ("STAC", BLUE)], "googleearthengine", BLUE, False, "Radar · SAR"),
        ("voting.svg", "Votación electrónica", "Plataforma de elecciones académicas con verificación por código al correo, voto anónimo separado de la participación, acta pública y pruebas de carga.",
         [("Supabase", "#3FCF8E"), ("PostgreSQL", "#4169E1"), ("Deno · TS", "#3178C6"), ("k6", "#7D64FF")], "supabase", "#3FCF8E", True, "2026 · seguridad y RLS"),
        ("android.svg", "Apps Android y Flutter", "Serie de apps del curso de móviles: Triqui con Custom Views, sonidos y MVVM, multijugador en tiempo real con Firebase, SQLite y mapas GPS con OSMDroid.",
         [("Kotlin", "#7F52FF"), ("Java", "#E76F00"), ("Firebase", "#DD2C00"), ("OSMDroid", "#7EBC6F")], "android", "#3DDC84", False, "Desarrollo móvil"),
        ("zenodo.svg", "Zenodo downloader", "Descargador de archivos grandes de Zenodo con conexiones paralelas por rangos, reintentos exponenciales, reanudación y verificación MD5.",
         [("Python", "#3776AB"), ("HTTP ranges", TEAL), ("threads", GOLD), ("MD5", GREEN)], "python", "#4C9AFF", False, "Herramienta"),
    ]
    for p in P:
        card(*p)

    stats([("53", "repositorios", GREEN), ("120k+", "líneas de código", TEAL), ("3", "plugins QGIS", GOLD), ("11", "apps móviles", PURPLE), ("12", "lenguajes", BLUE)])
    langs([
        ("Python", 70142, "#3776AB"), ("Dart", 23951, "#0175C2"), ("HTML / CSS", 12346, "#E34F26"),
        ("Kotlin / Java", 8261, "#7F52FF"), ("Quarto", 5078, "#4B9FD8"), ("JavaScript / TS", 4109, "#F7DF1E"),
        ("Shell / PowerShell", 1166, "#89E051"), ("R / Julia", 1108, "#9558B2"), ("SQL", 961, "#E38C00"),
    ])
    print("ok")

import json, re, html, base64, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import T

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
DIST = os.path.join(ROOT, "dist")
LT = {k: v[0] for k, v in T.items()}

ICONS = {
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 "sparkles": '<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.14-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.14a.5.5 0 0 1 .96 0l1.58 6.14a2 2 0 0 0 1.44 1.44l6.14 1.58a.5.5 0 0 1 0 .96l-6.14 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.14a.5.5 0 0 1-.96 0z"/>',
 "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
 "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "layers": '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
 "layout": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>',
 "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
 "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
 "message": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "app": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M10 4v4"/><path d="M2 8h20"/><path d="M6 4v4"/>',
 "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "pen": '<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.59 7.59"/><circle cx="11" cy="11" r="2"/>',
 "present": '<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>',
 "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
 "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
 "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "pin": '<path d="M20 10c0 5-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 "ig": '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
 "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "in": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "plus": '<path d="M5 12h14M12 5v14"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "calc": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M8 6h8M16 14v4M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/>',
 "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 13H8M16 17H8M16 13h-2"/>',
 "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .71-1.53l7-6a2 2 0 0 1 2.58 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
 "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
 "contact": '<path d="M15 13a3 3 0 1 0-6 0"/><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/><circle cx="12" cy="8" r="2"/>',
 "magnet": '<path d="m6 15-4-4 6.75-6.77a7.79 7.79 0 0 1 11 11L13 22l-4-4 6.39-6.36a2.14 2.14 0 0 0-3-3L6 15"/><path d="m5 8 4 4"/><path d="m12 15 4 4"/>',
 "image": '<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
 "grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
 "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
 "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
 "map": '<path d="M14.1 5.55a2 2 0 0 0 1.8 0l3.65-1.83A1 1 0 0 1 21 4.62v12.76a1 1 0 0 1-.55.9l-4.55 2.27a2 2 0 0 1-1.8 0l-4.2-2.1a2 2 0 0 0-1.8 0l-3.65 1.83A1 1 0 0 1 3 19.38V6.62a1 1 0 0 1 .55-.9L8.1 3.45a2 2 0 0 1 1.8 0z"/><path d="M15 5.76v15M9 3.24v15"/>',
}
icons_svg = "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items())

# ---------- generated blocks ----------
SERVICES = [("globe","web"),("layout","landing"),("bag","shop"),("sparkles","ai"),("bot","bot"),("workflow","auto"),
            ("users","crm"),("app","other"),("search","other"),("pen","other"),("present","other"),("package","web")]
svc = []
for i, (ic, need) in enumerate(SERVICES, 1):
    svc.append(f'''      <li class="svc-i rv">
        <div class="svc-top"><span class="svc-n">{i:02d}</span><svg class="i svc-ic"><use href="#i-{ic}"/></svg></div>
        <h3 data-t="s{i}.t"></h3>
        <p data-t="s{i}.d"></p>
        <a href="#kontaktai" class="svc-cta" data-need="{need}" data-t="s{i}.c"></a>
      </li>''')

SOL = [("globe","web","web"),("bag","web","shop"),("calendar","sys","other"),("calc","sys","other"),("users","sys","crm"),
       ("shield","sys","other"),("bot","ai","bot"),("sparkles","ai","ai"),("grid","sys","other"),("gauge","sys","other"),
       ("contact","sys","crm"),("magnet","ai","auto"),("calendar","sys","other"),("file","ai","auto"),("image","web","web"),
       ("layers","web","web"),("utensils","sys","other"),("home","web","web"),("car","web","web"),("wrench","web","web")]
sol = []
for i, (ic, cat, need) in enumerate(SOL, 1):
    sol.append(f'''      <li data-cat="{cat}"><button type="button" class="sol-i" data-need="{need}" data-x="x{i}"><svg class="i"><use href="#i-{ic}"/></svg><b data-t="x{i}"></b><em data-t="sol.ask"></em></button></li>''')

steps = [f'''      <li class="step rv"><span class="step-n">{i:02d}</span><h3 data-t="pc{i}.t"></h3><p data-t="pc{i}.d"></p></li>''' for i in range(1, 7)]

MOCKS = {
 1: '<span class="h"></span><span class="t"></span><span class="r"></span><span class="r"></span><span class="r"></span><span class="r"></span>',
 2: '<span class="h"></span>' + '<span class="l"></span><span class="p"></span>' * 5,
 3: '<span class="h"></span><span class="b"></span>' + "".join('<span class="c%s"></span>' % (" on" if j in (3, 7, 12, 16) else "") for j in range(20)),
 4: '<span class="h"></span>' + '<span class="g"></span>' * 6,
 5: '<span class="a"></span><span class="q"></span><span class="a s"></span><span class="q" style="width:38%"></span><span class="a"></span><span class="in"></span>',
 6: '<span class="h"></span><span class="d"></span><span class="d"></span><span class="d go"></span><span class="car"></span><span class="car"></span><span class="car"></span>',
}
NEEDS = {1: "web", 2: "web", 3: "landing", 4: "shop", 5: "ai", 6: "web"}
works = []
for i in range(1, 7):
    works.append(f'''      <article class="work rv">
        <div class="work-media"><div class="mock m{i}" aria-hidden="true"><div class="mk-bar"><i></i><i></i><i></i></div><div class="mk">{MOCKS[i]}</div></div><span class="badge" data-t="pf.badge"></span></div>
        <h3 data-t="d{i}.t"></h3>
        <p data-t="d{i}.d"></p>
        <a href="#kontaktai" data-need="{NEEDS[i]}" data-t="pf.cta"></a>
      </article>''')

faq = [f'''      <details class="qa"{" open" if i == 1 else ""}><summary><h3 data-t="q{i}"></h3><span class="pm"><svg class="i"><use href="#i-plus"/></svg></span></summary><p data-t="a{i}"></p></details>''' for i in range(1, 9)]

# ---------- JSON-LD ----------
BASE = "https://nexivo.sbs/"
PRICED = {1: 599, 2: 299, 3: 899}
offers = []
for i in range(1, 13):
    o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": LT[f"s{i}.t"], "description": LT[f"s{i}.d"],
         "provider": {"@id": BASE + "#org"}, "areaServed": "LT"}}
    if i in PRICED:
        o["priceSpecification"] = {"@type": "PriceSpecification", "minPrice": PRICED[i], "priceCurrency": "EUR"}
    offers.append(o)
jsonld = {
 "@context": "https://schema.org",
 "@graph": [
  {"@type": ["Organization", "ProfessionalService"], "@id": BASE + "#org", "name": "Nexivo", "url": BASE,
   "logo": BASE + "assets/icon-512.png", "image": BASE + "assets/og-image.jpg", "email": "hello@nexivo.sbs",
   "description": LT["meta.desc"], "slogan": "Idėja → Dizainas → Veikiantis produktas.",
   "address": {"@type": "PostalAddress", "addressLocality": "Vilnius", "addressCountry": "LT"},
   "areaServed": [{"@type": "City", "name": "Vilnius"}, {"@type": "Country", "name": "Lithuania"}],
   "knowsLanguage": ["lt", "ru", "en"], "priceRange": "€€",
   "knowsAbout": ["svetainių kūrimas", "landing page kūrimas", "e. parduotuvių kūrimas", "AI chatbotai", "verslo automatizacija", "CRM kūrimas", "SEO", "web design"],
   "contactPoint": {"@type": "ContactPoint", "email": "hello@nexivo.sbs", "contactType": "sales", "availableLanguage": ["Lithuanian", "Russian", "English"]},
   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Nexivo paslaugos", "itemListElement": offers}},
  {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Nexivo", "inLanguage": ["lt", "ru", "en"], "publisher": {"@id": BASE + "#org"}},
  {"@type": "WebPage", "@id": BASE + "#webpage", "url": BASE, "name": LT["meta.title"], "description": LT["meta.desc"], "inLanguage": "lt",
   "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#org"}},
  {"@type": "FAQPage", "@id": BASE + "#faq", "inLanguage": "lt", "mainEntity": [
    {"@type": "Question", "name": LT[f"q{i}"], "acceptedAnswer": {"@type": "Answer", "text": LT[f"a{i}"]}} for i in range(1, 9)]},
 ]}

# ---------- assemble ----------
tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
tpl = tpl.replace("{{SERVICES}}", "\n".join(svc)).replace("{{SOLUTIONS}}", "\n".join(sol)) \
         .replace("{{STEPS}}", "\n".join(steps)).replace("{{WORKS}}", "\n".join(works)) \
         .replace("{{FAQ}}", "\n".join(faq)).replace("{{ICONS}}", icons_svg)

missing = set()
def lt(k):
    if k not in LT: missing.add(k); return k
    return LT[k]
esc = lambda s: html.escape(s, quote=False)
attr = lambda s: html.escape(s, quote=True)

tpl = re.sub(r'(<(\w+)\b[^>]*?\sdata-t="([^"]+)"[^>]*>)(</\2>)', lambda m: m.group(1) + esc(lt(m.group(3))) + m.group(4), tpl)
tpl = re.sub(r'(<(\w+)\b[^>]*?\sdata-th="([^"]+)"[^>]*>)(</\2>)', lambda m: m.group(1) + lt(m.group(3)) + m.group(4), tpl)
tpl = re.sub(r'(<(\w+)\b[^>]*?\sdata-tl="([^"]+)"[^>]*>)(</\2>)', lambda m: m.group(1) + "".join(f"<li>{esc(x)}</li>" for x in lt(m.group(3)).split("|")) + m.group(4), tpl)
tpl = re.sub(r'\sdata-tp="([^"]+)"', lambda m: f' data-tp="{m.group(1)}" placeholder="{attr(lt(m.group(1)))}"', tpl)
tpl = re.sub(r'\sdata-ta="([^"]+)"', lambda m: f' data-ta="{m.group(1)}" aria-label="{attr(lt(m.group(1)))}"', tpl)
tpl = re.sub(r'\{\{([a-z][\w.]*)\}\}', lambda m: attr(lt(m.group(1))), tpl)

# leftover empty data-t elements?
empty = re.findall(r'data-t="([^"]+)"[^>]*></', tpl)
i18n = {l: {k: v[n] for k, v in T.items()} for n, l in enumerate(["lt", "ru", "en"])}
css = open(os.path.join(SRC, "styles.css"), encoding="utf-8").read()
js = open(os.path.join(SRC, "app.js"), encoding="utf-8").read()

def minify_css(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};,>])\s*", r"\1", s)
    return s.replace(";}", "}").strip()

out = tpl.replace("{{JSONLD}}", json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))) \
         .replace("{{CSS}}", minify_css(css)) \
         .replace("{{I18N}}", json.dumps(i18n, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")) \
         .replace("{{JS}}", js)

os.makedirs(DIST, exist_ok=True)
open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(out)

# preview: self-contained (assets as data URIs)
def datauri(p, mime):
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(ROOT, p), "rb").read()).decode()
prev = out.replace('src="assets/logo.webp"', f'src="{datauri("assets/logo.webp", "image/webp")}"') \
          .replace('href="assets/favicon-32.png"', f'href="{datauri("assets/favicon-32.png", "image/png")}"')
open(os.path.join(ROOT, "preview.html"), "w", encoding="utf-8").write(prev)

# copy static files
for d in ("assets",):
    shutil.copytree(os.path.join(ROOT, d), os.path.join(DIST, d), dirs_exist_ok=True)
for f in ("favicon.ico", "robots.txt", "sitemap.xml", "site.webmanifest"):
    shutil.copy(os.path.join(ROOT, f), DIST)

print("missing keys:", sorted(missing) or "none")
print("empty data-t:", sorted(set(empty)) or "none")
print("unused keys:", sorted(set(T) - set(re.findall(r'data-t[hlpa]?="([^"]+)"', tpl)) - set(re.findall(r'"(p\d|meta\.\w+|pol\.\w+|ok\.\w|mail\.\w|f\.\w+|sol\.prefill|ft\.\w+|spin\.\w+|need\.\w+)"', js))))
print("size", len(out.encode()) // 1024, "KB")

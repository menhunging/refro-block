import os, re, time, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_DIR = os.path.join(ROOT, "css", "refro")
ASSETS = os.path.join(ROOT, "css", "refro", "assets")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0 Safari/537.36"

CSS = [
    ("01-ui.design-tokens.css", "https://www.refro.ru/bitrix/js/ui/design-tokens/dist/ui.design-tokens.min.css"),
    ("02-ui.font.opensans.css", "https://www.refro.ru/bitrix/js/ui/fonts/opensans/ui.font.opensans.min.css"),
    ("03-main.popup.bundle.css", "https://www.refro.ru/bitrix/js/main/popup/dist/main.popup.bundle.min.css"),
    ("04-default_e326.css", "https://www.refro.ru/bitrix/cache/css/s1/aspro_max/default_e32658fa6171fa8317ee55a00145e006/default_e32658fa6171fa8317ee55a00145e006_v1.css"),
    ("05-default_9a6f.css", "https://www.refro.ru/bitrix/cache/css/s1/aspro_max/default_9a6fb276bbe563a73c962b4a0b4d4e26/default_9a6fb276bbe563a73c962b4a0b4d4e26_v1.css"),
    ("06-bonus-system.css", "https://www.refro.ru/local/templates/aspro_max/css/bonus-system.min.css"),
    ("07-template_cd74.css", "https://www.refro.ru/bitrix/cache/css/s1/aspro_max/template_cd74a4ad7f68b37018f3eacbb35cda62/template_cd74a4ad7f68b37018f3eacbb35cda62_v1.css"),
    ("08-template_6af1.css", "https://www.refro.ru/bitrix/cache/css/s1/aspro_max/template_6af1fb364027db15be923381c218b07f/template_6af1fb364027db15be923381c218b07f_v1.css"),
    ("09-panel.popup.css", "https://www.refro.ru/bitrix/panel/main/popup.min.css"),
    ("10-critical.css", "https://www.refro.ru/local/templates/aspro_max/css/critical.min.css"),
    ("11-HelveticaNeueCyr.css", "https://www.refro.ru/local/templates/aspro_max/css/fonts/HelveticaNeueCyr/HelveticaNeueCyr.css"),
    ("12-print.css", "https://www.refro.ru/local/templates/aspro_max/css/print.min.css"),
]

INLINE = """:root{--theme-base-color: #f6de63;--theme-base-opacity-color: #f6de631a;--theme-base-color-hue:50;--theme-base-color-saturation:89%;--theme-base-color-lightness:68%;}
html {--theme-page-width: 1500px;--theme-page-width-padding: 30px}
"""

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.refro.ru/"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

URL_RE = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""")
IMPORT_RE = re.compile(r"""@import\s+(['"])([^'"]+)\1""")

assets = {}  # abs url -> local rel path (relative to CSS_DIR)
failed = []

def local_name(absurl):
    p = urllib.parse.urlparse(absurl)
    path = p.path.lstrip("/")
    if p.netloc not in ("www.refro.ru", "refro.ru"):
        path = p.netloc + "/" + path
    return "assets/" + path

def rewrite(css, base):
    def repl(m):
        raw = m.group(2).strip()
        if raw.startswith(("data:", "#", "about:")):
            return m.group(0)
        absu = urllib.parse.urljoin(base, raw)
        clean, _, frag = absu.partition("#")
        clean_noq = clean.split("?")[0]
        rel = local_name(clean_noq)
        assets[clean] = rel
        return 'url("%s%s")' % (rel, ("#" + frag) if frag else "")
    return URL_RE.sub(repl, css)

os.makedirs(CSS_DIR, exist_ok=True)
all_parts = ["/* refro.ru base styles (Aspro Max + Bitrix) */\n", INLINE]
for name, url in CSS:
    css = get(url).decode("utf-8", "replace")
    time.sleep(0.5)
    if IMPORT_RE.search(css):
        print("WARN @import in", name, IMPORT_RE.findall(css))
    css = rewrite(css, url)
    with open(os.path.join(CSS_DIR, name), "w") as f:
        f.write(css)
    all_parts.append("\n/* ===== %s | %s ===== */\n%s\n" % (name, url, css))
    print("css", name, len(css))

with open(os.path.join(CSS_DIR, "00-inline.css"), "w") as f:
    f.write(INLINE)
with open(os.path.join(ROOT, "css", "refro.bundle.css"), "w") as f:
    # bundle lives in css/, assets are in css/refro/assets
    f.write("".join(all_parts).replace('url("assets/', 'url("refro/assets/'))

def dl(item):
    absu, rel = item
    dest = os.path.join(CSS_DIR, rel)
    if os.path.exists(dest):
        return
    try:
        data = get(absu)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
    except Exception as e:
        failed.append((absu, str(e)))

import time
for item in assets.items():
    if "image_source" in item[0]:
        continue
    dl(item)
    time.sleep(0.3)

print("assets:", len(assets), "failed:", len(failed))
for u, e in failed:
    print("  FAIL", u, e)

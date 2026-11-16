import os, re, glob, time, urllib.request

CSS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "css", "refro")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0 Safari/537.36"
DEAD = ("image_source",)

rels = set()
for f in glob.glob(os.path.join(CSS_DIR, "*.css")):
    rels |= set(re.findall(r'url\("(assets/[^"#]+)', open(f).read()))

missing = [r for r in sorted(rels) if not os.path.exists(os.path.join(CSS_DIR, r)) and not any(d in r for d in DEAD)]
print("missing", len(missing))
for rel in missing:
    path = rel[len("assets/"):]
    url = ("https://www.refro.ru/" + path) if path.split("/")[0] in ("local", "bitrix", "upload") else "https://" + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.refro.ru/"})
        data = urllib.request.urlopen(req, timeout=20).read()
        dest = os.path.join(CSS_DIR, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(data)
        print("ok  ", url)
    except Exception as e:
        print("FAIL", url, e)
    time.sleep(0.5)

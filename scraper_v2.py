import os, json, requests, re
from collections import Counter

KEY_FILE = os.path.expanduser("~/.firecrawl_key")
FIRECRAWL_KEY = open(KEY_FILE).read().strip()
HEADERS = {"Authorization": f"Bearer {FIRECRAWL_KEY}", "Content-Type": "application/json"}

# Linktrees y webs directas — no canales de YouTube
TARGETS = [
    {"nombre": "Eduardo Vazquez IA", "url": "https://linktr.ee/eduardovazquezai"},
    {"nombre": "DotCSV", "url": "https://linktr.ee/dot_csv"},
    {"nombre": "Brita IA", "url": "https://linktr.ee/britainteligenciaartificial"},
    {"nombre": "ORA IA", "url": "https://oraia.com"},
]

HERRAMIENTAS = ["kling","suno","elevenlabs","gamma","deepseek","midjourney","runway",
"perplexity","cursor","heygen","pika","ideogram","leonardo","fishaudio","wan","qwen",
"kimi","canva","descript","capcut","chatgpt","openai","notion","jasper"]

def scrape(url):
    r = requests.post("https://api.firecrawl.dev/v1/scrape", headers=HEADERS,
        json={"url": url, "formats": ["markdown","links"], "waitFor": 2000}, timeout=30)
    return r.json().get("data", {}) if r.status_code == 200 else None

def detectar(url):
    for h in HERRAMIENTAS:
        if h in url.lower(): return h
    return None

conteo = Counter()
detalle = []

for t in TARGETS:
    print(f"\n🔍 {t['nombre']} — {t['url']}")
    data = scrape(t["url"])
    if not data:
        print("  ⚠️ Sin datos")
        continue
    md = data.get("markdown","")
    links = data.get("links", [])
    todas_urls = re.findall(r'https?://[^\s\)\]\>\"\']+', md)
    todas_urls += [l if isinstance(l,str) else l.get("url","") for l in links]
    encontrados = []
    for u in todas_urls:
        h = detectar(u)
        if h and h not in encontrados:
            encontrados.append(h)
            conteo[h] += 1
    print(f"  ✅ {encontrados}" if encontrados else "  ℹ️ Sin herramientas")
    detalle.append({"creador": t["nombre"], "herramientas": encontrados})

print("\n📊 RANKING FINAL:")
for h, n in conteo.most_common():
    print(f"  {h:20} {'█'*n} ({n})")

print("\n🎯 KEYWORDS PRIORITARIAS PARA AI4US:")
for h, _ in conteo.most_common(10):
    print(f"  → '{h} mexico'  |  '{h} gratis'  |  '{h} precio pesos'")

json.dump({"conteo": dict(conteo), "detalle": detalle},
    open(os.path.expanduser("~/llm4us/influencer_links.json"),"w"), ensure_ascii=False, indent=2)
print("\n💾 ~/llm4us/influencer_links.json")

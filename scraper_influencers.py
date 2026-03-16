import os, json, requests, re
from collections import Counter
from pathlib import Path

KEY_FILE = os.path.expanduser("~/.firecrawl_key")
FIRECRAWL_KEY = open(KEY_FILE).read().strip()
HEADERS = {"Authorization": f"Bearer {FIRECRAWL_KEY}", "Content-Type": "application/json"}

TARGETS = [
    {"nombre": "Eduardo Vazquez IA", "url": "https://www.youtube.com/@EduardoVazquezIA/videos"},
    {"nombre": "DotCSV", "url": "https://www.youtube.com/@DotCSV/videos"},
    {"nombre": "Brita IA", "url": "https://www.youtube.com/@BritaInteligenciaArtificial/videos"},
]

HERRAMIENTAS = ["kling","suno","elevenlabs","gamma","deepseek","midjourney","runway","perplexity","cursor","heygen","pika","ideogram","leonardo","fishaudio","wan","qwen","kimi","canva","descript","opus","capcut"]

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
    print(f"\n🔍 {t['nombre']}")
    data = scrape(t["url"])
    if not data:
        print("  ⚠️ Sin datos")
        continue
    urls = re.findall(r'https?://[^\s\)\]\>\"\']+', data.get("markdown",""))
    encontrados = []
    for u in urls:
        h = detectar(u)
        if h:
            encontrados.append(h)
            conteo[h] += 1
    print(f"  ✅ {encontrados}" if encontrados else "  ℹ️ Sin herramientas detectadas")
    detalle.append({"creador": t["nombre"], "herramientas": encontrados})

print("\n📊 RANKING:")
for h, n in conteo.most_common():
    print(f"  {h:20} {'█'*n} ({n})")

print("\n🎯 KEYWORDS AI4US:")
for h, _ in conteo.most_common(10):
    print(f"  → {h} mexico / {h} gratis / {h} precio pesos")

json.dump({"conteo": dict(conteo), "detalle": detalle},
    open(os.path.expanduser("~/llm4us/influencer_links.json"),"w"), ensure_ascii=False, indent=2)
print("\n💾 Guardado: ~/llm4us/influencer_links.json")

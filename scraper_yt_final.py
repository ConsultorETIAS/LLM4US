import os, json, requests, re
from collections import Counter

YT_KEY = open(os.path.expanduser("~/.youtube_key")).read().strip()
BASE = "https://www.googleapis.com/youtube/v3"

HERRAMIENTAS = [
    "kling","suno","elevenlabs","gamma","deepseek","midjourney",
    "runway","perplexity","cursor","heygen","pika","ideogram",
    "leonardo","fishaudio","wan","qwen","kimi","canva","descript",
    "capcut","chatgpt","openai","notion","jasper","synthesia",
    "murf","lovo","invideo","pictory","fliki","veed","opus"
]

def get_channel_id(handle):
    """Resuelve @handle a channel ID real via API"""
    r = requests.get(f"{BASE}/channels", params={
        "key": YT_KEY, "forHandle": handle, "part": "id"
    })
    items = r.json().get("items", [])
    return items[0]["id"] if items else None

def get_videos(channel_id, max=25):
    r = requests.get(f"{BASE}/search", params={
        "key": YT_KEY, "channelId": channel_id,
        "part": "snippet", "order": "date",
        "maxResults": max, "type": "video"
    })
    return [(i["id"]["videoId"], i["snippet"]["title"])
            for i in r.json().get("items", [])
            if "videoId" in i["id"]]

def get_descripcion(video_id):
    r = requests.get(f"{BASE}/videos", params={
        "key": YT_KEY, "id": video_id, "part": "snippet"
    })
    items = r.json().get("items", [])
    return items[0]["snippet"]["description"] if items else ""

def detectar(texto):
    return list({h for h in HERRAMIENTAS if h in texto.lower()})

# ============================================================
print("=" * 55)
print("  AI4US — YouTube Influencer Scraper")
print("  Canal: @websitelearners")
print("=" * 55)

handle = "websitelearners"
print(f"\n🔍 Resolviendo @{handle}...")
channel_id = get_channel_id(handle)

if not channel_id:
    print("❌ No se encontró el canal")
    exit(1)

print(f"   ✅ Channel ID: {channel_id}")

videos = get_videos(channel_id, max=25)
print(f"   📹 {len(videos)} videos recientes\n")

conteo = Counter()
resultados = []

for vid_id, titulo in videos:
    desc = get_descripcion(vid_id)
    herramientas = detectar(desc)
    urls = re.findall(r'https?://[^\s\)\]\>]+', desc)
    
    if herramientas:
        print(f"   ✅ {titulo[:50]}")
        print(f"      Herramientas: {herramientas}")
        for h in herramientas:
            conteo[h] += 1
        resultados.append({
            "video": titulo,
            "url": f"youtube.com/watch?v={vid_id}",
            "herramientas": herramientas,
            "links": [u for u in urls if any(h in u.lower() for h in HERRAMIENTAS)]
        })

print(f"\n{'='*55}")
print("  📊 HERRAMIENTAS MÁS REFERENCIADAS")
print(f"{'='*55}")
for h, n in conteo.most_common():
    print(f"  {h:20} {'█'*n} ({n})")

print(f"\n🎯 PÁGINAS PRIORITARIAS PARA AI4US:")
for h, _ in conteo.most_common(10):
    print(f"  → {h}-mexico.html")

out = os.path.expanduser("~/llm4us/websitelearners_map.json")
json.dump({"channel_id": channel_id, "conteo": dict(conteo.most_common()), "videos": resultados},
    open(out,"w"), ensure_ascii=False, indent=2)
print(f"\n💾 {out}")

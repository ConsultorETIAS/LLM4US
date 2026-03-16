import os, json, requests, re
from collections import Counter

YT_KEY = open(os.path.expanduser("~/.youtube_key")).read().strip()

CANALES = [
    {"nombre": "Eduardo Vazquez IA", "id": "UCTnBeF4JrIaJEMIyKFCYRPQ"},
    {"nombre": "DotCSV",             "id": "UCy5znSnfMsDwaLlj1Bs32ig"},
    {"nombre": "Brita IA",           "id": "UCBrita_id_aqui"},
]

HERRAMIENTAS = ["kling","suno","elevenlabs","gamma","deepseek","midjourney","runway",
"perplexity","cursor","heygen","pika","ideogram","fishaudio","canva","chatgpt","notion"]

def get_videos(channel_id, max=10):
    r = requests.get("https://www.googleapis.com/youtube/v3/search", params={
        "key": YT_KEY, "channelId": channel_id, "part": "snippet",
        "order": "date", "maxResults": max, "type": "video"
    })
    items = r.json().get("items", [])
    return [i["id"]["videoId"] for i in items if "videoId" in i["id"]]

def get_descripcion(video_id):
    r = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        "key": YT_KEY, "id": video_id, "part": "snippet"
    })
    items = r.json().get("items", [])
    return items[0]["snippet"]["description"] if items else ""

def detectar(texto):
    encontrados = []
    for h in HERRAMIENTAS:
        if h in texto.lower() and h not in encontrados:
            encontrados.append(h)
    return encontrados

conteo = Counter()
detalle = []

for canal in CANALES:
    print(f"\n🔍 {canal['nombre']}")
    videos = get_videos(canal["id"])
    print(f"   {len(videos)} videos recientes")
    herramientas_canal = []
    for vid in videos:
        desc = get_descripcion(vid)
        encontrados = detectar(desc)
        urls = re.findall(r'https?://[^\s]+', desc)
        if encontrados:
            print(f"   → youtube.com/watch?v={vid}: {encontrados}")
            herramientas_canal.extend(encontrados)
            for h in encontrados:
                conteo[h] += 1
    detalle.append({"creador": canal["nombre"], "herramientas": herramientas_canal})

print("\n📊 RANKING:")
for h, n in conteo.most_common():
    print(f"  {h:20} {'█'*n} ({n})")

print("\n🎯 KEYWORDS PARA AI4US:")
for h, _ in conteo.most_common(10):
    print(f"  → {h} mexico | {h} gratis | {h} precio pesos")

json.dump({"conteo": dict(conteo), "detalle": detalle},
    open(os.path.expanduser("~/llm4us/yt_links.json"),"w"), ensure_ascii=False, indent=2)
print("\n💾 ~/llm4us/yt_links.json")

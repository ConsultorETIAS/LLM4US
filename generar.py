import os, json, time, requests
from pathlib import Path

API_KEY  = "PEGA_TU_KEY_AISTUDIO_AQUI"
TC       = 20.30
REPO_DIR = os.path.expanduser("~/llm4us")
OUT_DIR  = f"{REPO_DIR}/docs/herramientas"
Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

TOOLS = [
    ("Kling AI",    "video",  "China", 10, "Wan AI gratis",       "Foto a video ultra realista viral en TikTok"),
    ("DeepSeek R1", "chat",   "China",  0, "Qwen 2.5 gratis",     "30x mas barato que o1"),
    ("Suno",        "musica", "USA",    8, "Udio precio similar",  "Canciones desde texto en 30 segundos"),
    ("Gamma",       "slides", "USA",   10, "Kimi genera docs",     "Presentaciones desde texto en 60 seg"),
    ("ElevenLabs",  "voz",    "USA",    5, "FishAudio 100 gratis", "Clonacion de voz viral entre creadores"),
]

SYS = """Eres editor de AI4US, plaza de IA para Mexico y LATAM.
Creas guias utiles para usuarios hispanohablantes sin tarjeta internacional.
Precios SIEMPRE en MXN a $20.30 USD. Tono: amigo, no manual corporativo.
Responde SOLO con JSON valido. Sin markdown. Sin texto extra."""

def api(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    r = requests.post(
        url,
        params={"key": API_KEY},
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{"text": SYS + "\n\n" + prompt}]
            }],
            "generationConfig": {
                "maxOutputTokens": 1400,
                "temperature": 0.7
            }
        },
        timeout=90
    )
    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    if "```" in txt:
        partes = txt.split("```")
        txt = partes[1] if len(partes) > 1 else partes[0]
        if txt.startswith("json"):
            txt = txt[4:]
    return json.loads(txt.strip().rstrip("`").strip())

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<style>
:root{{--am:#f5c842;--ng:#0a0a0a;--vd:#2dce6e;--rd:#e63030;--gr:#1a1a1a}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--ng);color:#f0ede6;font-family:sans-serif;max-width:860px;margin:0 auto;padding:0 0 3rem}}
header{{background:var(--am);color:var(--ng);padding:1rem 1.5rem;font-weight:900;font-size:1.4rem}}
header span{{background:var(--ng);color:var(--am);padding:0 .3em}}
header div{{font-size:.72rem;font-weight:400;margin-top:.3rem;opacity:.7}}
main{{padding:1.5rem}}
h1{{font-size:clamp(1.8rem,5vw,2.8rem);font-weight:900;line-height:1.1;margin-bottom:1rem}}
h1 em{{color:var(--am);font-style:normal;display:block}}
h2{{color:var(--am);margin:2rem 0 .8rem;font-size:1rem;text-transform:uppercase;letter-spacing:.08em}}
p{{line-height:1.7;margin-bottom:.8rem}}
.meta{{display:flex;gap:1.5rem;flex-wrap:wrap;margin-bottom:1.5rem}}
.mi{{font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#888}}
.mi strong{{display:block;color:#f0ede6;font-size:.78rem}}
.v{{background:var(--vd);color:var(--ng);padding:1rem 1.2rem;font-weight:700;margin:1.2rem 0}}
.planes{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
@media(max-width:500px){{.planes{{grid-template-columns:1fr}}}}
.plan{{background:var(--gr);border:1px solid #2a2a2a;padding:1rem}}
.pn{{font-size:.62rem;text-transform:uppercase;letter-spacing:.12em;color:#888;margin-bottom:.4rem}}
.pm{{font-size:2rem;font-weight:900;color:var(--am);line-height:1}}
.pu{{font-size:.75rem;color:#888;margin-top:.2rem}}
.pi{{font-size:.85rem;margin-top:.7rem;color:#ccc;line-height:1.5}}
.pl{{font-size:.8rem;color:var(--rd);margin-top:.4rem}}
.acc{{background:var(--gr);padding:1.2rem;margin:1rem 0;border:1px solid #2a2a2a}}
.bg{{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.9rem}}
.b{{font-size:.68rem;padding:.25rem .65rem;border:1px solid;font-weight:700}}
.bs{{border-color:var(--vd);color:var(--vd)}}
.bn{{border-color:var(--rd);color:var(--rd)}}
ol{{padding-left:1.4rem}}
li{{margin-bottom:.5rem;font-size:.9rem;line-height:1.5}}
.truco{{background:#0f0f0f;border-left:4px solid var(--am);padding:1rem 1.2rem;margin:1.5rem 0}}
.truco strong{{color:var(--am);display:block;margin-bottom:.5rem}}
.asia{{background:#0f0f0f;border-left:3px solid var(--rd);padding:.9rem 1.1rem;margin:.8rem 0}}
.asia small{{color:#888;font-size:.82rem;display:block;margin-top:.3rem}}
details{{border-bottom:1px solid #2a2a2a;padding:.7rem 0}}
summary{{cursor:pointer;font-weight:600;font-size:.9rem;list-style:none;padding:.2rem 0}}
summary::-webkit-details-marker{{display:none}}
details p{{margin-top:.5rem;font-size:.85rem;color:#ccc;padding-left:1rem;line-height:1.6;margin-bottom:0}}
.cta{{display:block;background:var(--am);color:var(--ng);padding:1.1rem;text-align:center;font-weight:900;text-decoration:none;font-size:1rem;margin:2rem 0}}
footer{{border-top:2px solid #2a2a2a;padding:1.2rem 1.5rem;font-size:.75rem;color:#888;text-align:center}}
footer a{{color:var(--am);text-decoration:none}}
</style>
</head>
<body>
<header>AI4<span>US</span><div>La Plaza de la IA para Mexico y LATAM</div></header>
<main>
<div class="meta">
<div class="mi"><strong>{categoria}</strong>Categoria</div>
<div class="mi"><strong>{origen}</strong>Origen</div>
<div class="mi"><strong>Marzo 2026</strong>Actualizado</div>
<div class="mi"><strong>$20.30 MXN</strong>Por 1 USD</div>
</div>
<h1>{nombre} <em>en Mexico 2026</em></h1>
<div class="v">💡 {veredicto}</div>
<h2>Que es exactamente</h2><p>{que_es}</p>
<h2>Cuanto cuesta en pesos</h2>
<div class="planes">
<div class="plan"><div class="pn">Gratuito</div><div class="pm">$0 MXN</div><div class="pu">$0 USD</div><div class="pi">{gi}</div><div class="pl">Limite: {gl}</div></div>
<div class="plan"><div class="pn">Pro</div><div class="pm">${pmxn} MXN/mes</div><div class="pu">${pusd} USD/mes</div><div class="pi">Sin limites</div></div>
</div>
<h2>Como acceder desde Mexico</h2>
<div class="acc">
<div class="bg"><span class="b {cd}">Debito MX: {td}</span><span class="b {cv}">VPN: {tv}</span><span class="b bs">Disponible en MX: Si</span></div>
<ol>{pasos}</ol>
</div>
<div class="truco"><strong>Lo que el influencer no te dijo</strong>{truco}</div>
<h2>Alternativa asiatica mas barata</h2>
<div class="asia"><strong>{alt}</strong><small>{palt}</small></div>
<h2>Preguntas desde Mexico</h2>
<details><summary>{f1p}</summary><p>{f1r}</p></details>
<details><summary>{f2p}</summary><p>{f2r}</p></details>
<details><summary>{f3p}</summary><p>{f3r}</p></details>
<a class="cta" href="/LLM4US/">Explorar mas herramientas en AI4US</a>
</main>
<footer><a href="/LLM4US/">AI4US — La Plaza de la IA para LATAM</a><br>Marzo 2026 · $20.30 MXN/USD · #AI4US #IAsinBarreras</footer>
</body></html>"""

def hacer_html(d, nombre, slug, pusd, pmxn, alt, cat, origen):
    pasos = "".join(f"<li>{p}</li>" for p in d.get("pasos", []))
    return HTML.format(
        titulo=d.get("titulo", f"{nombre} en Mexico 2026"),
        descripcion=d.get("descripcion", ""),
        slug=slug, nombre=nombre, categoria=cat, origen=origen,
        veredicto=d.get("veredicto", ""),
        que_es=d.get("que_es", ""),
        gi=d.get("gratis_incluye", ""),
        gl=d.get("gratis_limite", ""),
        pusd=pusd, pmxn=int(pmxn),
        cd="bs" if d.get("acepta_debito_mx", True) else "bn",
        td="Si" if d.get("acepta_debito_mx", True) else "No",
        cv="bs" if not d.get("requiere_vpn", False) else "bn",
        tv="No necesaria" if not d.get("requiere_vpn", False) else "Necesaria",
        pasos=pasos,
        truco=d.get("truco", ""),
        alt=alt,
        palt=d.get("por_que_asia", ""),
        f1p=d.get("faq1p", ""), f1r=d.get("faq1r", ""),
        f2p=d.get("faq2p", ""), f2r=d.get("faq2r", ""),
        f3p=d.get("faq3p", ""), f3r=d.get("faq3r", ""),
    )

print("=" * 48)
print("  AI4US pSEO Generator — Termux Edition")
print("  Motor: Gemini 1.5 Flash (gratis)")
print("=" * 48)

generadas = []

for i, (nombre, cat, origen, pusd, alt, viral) in enumerate(TOOLS):
    slug = nombre.lower().replace(" ", "-").replace(".", "-")
    pmxn = pusd * TC
    print(f"\n[{i+1}/5] {nombre}...")

    prompt = f"""Genera JSON AI4US para: {nombre}
Categoria:{cat} | Origen:{origen}
Plan pro: ${pusd} USD = ${pmxn:.0f} MXN/mes
Alternativa asiatica: {alt}
Viral porque: {viral}

Responde SOLO con este JSON sin texto adicional:
{{
  "titulo": "{nombre} en Mexico 2026 - precio en pesos y como usarlo",
  "descripcion": "Guia de {nombre} para Mexico: precio en pesos, acceso sin tarjeta gringa. {cat} IA 2026.",
  "veredicto": "una oracion directa cuando usarlo vs alternativa con precio concreto",
  "que_es": "dos parrafos. primero que hace con ejemplo en CDMX. segundo por que es viral ahora",
  "gratis_incluye": "que da exactamente el plan gratuito",
  "gratis_limite": "la limitacion mas importante del plan gratis",
  "acepta_debito_mx": true,
  "requiere_vpn": false,
  "pasos": ["paso 1 con URL", "paso 2 como registrarse", "paso 3 como pagar desde Mexico"],
  "truco": "dato util que el influencer no dijo, minimo 2 oraciones",
  "por_que_asia": "cuando conviene usar {alt} en vez de {nombre}",
  "faq1p": "Funciona {nombre} en espanol",
  "faq1r": "respuesta honesta sobre soporte en espanol",
  "faq2p": "Puedo usar {nombre} gratis desde Mexico",
  "faq2r": "limites exactos del plan gratis",
  "faq3p": "{nombre} o {alt} cual uso",
  "faq3r": "veredicto directo en 2 oraciones"
}}"""

    try:
        datos = api(prompt)
        html = hacer_html(datos, nombre, slug, pusd, pmxn, alt, cat, origen)
        ruta = f"{OUT_DIR}/{slug}-mexico.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  OK: {slug}-mexico.html")
        generadas.append(slug)
        time.sleep(2)
    except Exception as e:
        print(f"  ERROR: {e}")
        time.sleep(3)

print(f"\n{len(generadas)}/5 paginas generadas")

if generadas:
    print("Subiendo a GitHub...")
    os.chdir(REPO_DIR)
    os.system('git add docs/herramientas/')
    os.system('git commit -m "AI4US: 5 paginas pSEO LATAM"')
    ok = os.system('git push')
    if ok == 0:
        print("\nListo. URLs activas en 30 segundos:")
        for s in generadas:
            print(f"  https://consultoretias.github.io/LLM4US/herramientas/{s}-mexico.html")
    else:
        print("\nError git push. Ejecuta: cd ~/llm4us && git push")
else:
    print("Verifica tu API key de AI Studio en linea 4.")

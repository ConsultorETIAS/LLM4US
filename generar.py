














#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI4US pSEO Generator - FIX 404
Android 14 + Termux + Google AI Studio
Endpoint actualizado: gemini-2.0-flash
"""

import os
import json
import time
import sys
import subprocess
from pathlib import Path

# Fix UTF-8 en Termux/Android
sys.stdout.reconfigure(encoding='utf-8')

# === CONFIGURACIÓN ===
API_KEY = "AIzaSyBPkK7lbcclU9qpVZSGSvLYVOXaIjcp-i0"  # Tu key aquí
TC = 20.30

# Directorios
REPO_DIR = os.path.expanduser("~/llm4us")
OUT_DIR = Path(REPO_DIR) / "docs" / "herramientas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOOLS = [
    {
        "nombre": "Kling AI",
        "slug": "kling-ai",
        "categoria": "video",
        "origen": "China",
        "usd": 10,
        "alt": "Wan AI (gratis)",
        "target_creador": "elussicreativo, Brita IA",
        "keywords": "kling ai mexico, kling ai español gratis",
        "viral": "Videos foto a video viral TikTok México"
    },
    {
        "nombre": "DeepSeek R1",
        "slug": "deepseek-r1",
        "categoria": "chat",
        "origen": "China", 
        "usd": 0,
        "alt": "Qwen 2.5 (Alibaba)",
        "target_creador": "Eduardo Vázquez IA, DotCSV",
        "keywords": "deepseek mexico, deepseek gratis sin vpn",
        "viral": "30x más barato que OpenAI o1"
    },
    {
        "nombre": "Suno",
        "slug": "suno",
        "categoria": "musica",
        "origen": "USA",
        "usd": 8,
        "alt": "Udio (precio similar)",
        "target_creador": "Canales música generativa",
        "keywords": "suno mexico, suno musica ia español",
        "viral": "Canciones desde texto en 30 segundos"
    },
    {
        "nombre": "Gamma",
        "slug": "gamma",
        "categoria": "slides",
        "origen": "USA",
        "usd": 10,
        "alt": "Kimi (genera docs gratis)",
        "target_creador": "Eduardo Vázquez IA",
        "keywords": "gamma app mexico, presentaciones ia gratis",
        "viral": "Presentaciones desde texto en 60 segundos"
    },
    {
        "nombre": "ElevenLabs",
        "slug": "elevenlabs",
        "categoria": "voz",
        "origen": "USA",
        "usd": 5,
        "alt": "FishAudio (100 clones gratis)",
        "target_creador": "ORA IA",
        "keywords": "elevenlabs mexico, clonar voz gratis",
        "viral": "Clonación voz viral creadores mexicanos"
    }
]

SYS_PROMPT = """Eres editor de AI4US, plaza IA para México/LATAM.
Interceptamos tráfico de creadores que promueven herramientas sin contexto local.
Tono: amigo experto, directo, útil. Precios en MXN ($20.30/USD).
Responde SOLO JSON válido. Sin markdown."""

def llamar_gemini(prompt):
    """FIX: Endpoint actualizado gemini-2.0-flash"""
    import requests
    
    # ENDPOINT CORREGIDO - usa 'latest' o '001'
    MODEL = "gemini-2.0-flash"  # Alternativa: gemini-2.0-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    
    try:
        r = requests.post(
            url,
            params={"key": API_KEY},
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"role": "user", "parts": [{"text": SYS_PROMPT + "\n\n" + prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048,
                    "topP": 0.8,
                    "topK": 40
                }
            },
            timeout=90
        )
        
        # Debug: mostrar error detallado si falla
        if r.status_code != 200:
            print(f"   Status: {r.status_code}")
            print(f"   Respuesta: {r.text[:200]}")
            return None
            
        data = r.json()
        
        # Verificar estructura de respuesta
        if "candidates" not in data:
            print(f"   Error: No 'candidates' en respuesta")
            print(f"   Respuesta: {json.dumps(data, indent=2)[:300]}")
            return None
            
        texto = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Limpiar markdown
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0]
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0]
            
        return json.loads(texto.strip())
        
    except json.JSONDecodeError as e:
        print(f"   Error JSON: {e}")
        print(f"   Texto: {texto[:200]}...")
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{meta_desc}">
<style>
:root{{--am:#f5c842;--ng:#0a0a0a;--vd:#2dce6e;--rd:#e63030;--gr:#1a1a1a;--tx:#f0ede6}}
*{{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif}}
body{{background:var(--ng);color:var(--tx);line-height:1.6;max-width:900px;margin:0 auto;padding:0 1rem}}
header{{background:var(--am);color:var(--ng);padding:1rem;font-weight:900;font-size:1.2rem}}
header span{{background:var(--ng);color:var(--am);padding:.2rem .4rem;margin-left:.2rem}}
.target{{background:#1a1510;border:1px dashed #664400;padding:.8rem;margin:1rem 0;font-size:.8rem;color:#888;border-radius:4px}}
h1{{font-size:clamp(1.5rem,5vw,2.2rem);font-weight:900;margin:1rem 0;line-height:1.2}}
h1 em{{color:var(--am);font-style:normal;display:block;font-size:.6em;margin-top:.2rem}}
.meta{{display:flex;gap:1rem;flex-wrap:wrap;font-size:.75rem;color:#888;margin-bottom:1rem}}
.meta span{{background:var(--gr);padding:.3rem .6rem;border-radius:4px}}
.veredicto{{background:var(--vd);color:var(--ng);padding:1rem;font-weight:700;border-radius:8px;margin:1rem 0}}
h2{{color:var(--am);font-size:1rem;margin:1.5rem 0 .5rem;text-transform:uppercase;letter-spacing:.05em}}
.precios{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
@media(max-width:600px){{.precios{{grid-template-columns:1fr}}}}
.plan{{background:var(--gr);padding:1rem;border-radius:8px;border:2px solid #333}}
.plan.paid{{border-color:var(--am)}}
.plan-name{{font-size:.7rem;text-transform:uppercase;color:#888}}
.plan-price{{font-size:2rem;font-weight:900;color:var(--am)}}
.plan-price small{{display:block;font-size:.4em;color:#888;font-weight:400}}
.limit{{color:var(--rd);font-size:.8rem;margin-top:.5rem}}
.acceso{{background:var(--gr);padding:1rem;border-radius:8px;margin:1rem 0}}
.badgets{{display:flex;gap:.5rem;margin-bottom:1rem;flex-wrap:wrap}}
.badge{{font-size:.65rem;padding:.3rem .6rem;border-radius:20px;font-weight:700}}
.badge.ok{{background:#1a3d1a;color:var(--vd)}}
.badge.bad{{background:#3d1a1a;color:var(--rd)}}
ol{{padding-left:1.5rem}}
li{{margin-bottom:.8rem}}
.truco{{background:#0f0f0f;border-left:4px solid var(--am);padding:1rem;margin:1rem 0}}
.truco strong{{color:var(--am);display:block;margin-bottom:.3rem}}
.alt{{background:var(--gr);border-left:4px solid var(--rd);padding:1rem;margin:1rem 0}}
.alt strong{{color:var(--rd)}}
.alt small{{display:block;color:#888;font-size:.8rem;margin-top:.3rem}}
details{{background:var(--gr);margin-bottom:.5rem;border-radius:8px}}
summary{{padding:1rem;cursor:pointer;font-weight:600;list-style:none}}
summary::marker{{display:none}}
details p{{padding:0 1rem 1rem;color:#ccc;font-size:.9rem}}
a.cta{{display:block;background:var(--am);color:var(--ng);text-align:center;padding:1rem;text-decoration:none;font-weight:900;border-radius:8px;margin:2rem 0}}
footer{{border-top:2px solid #333;padding:2rem 1rem;text-align:center;color:#666;font-size:.8rem;margin-top:2rem}}
</style>
</head>
<body>
<header>AI4<span>US</span><div style="font-size:.7rem;font-weight:400;opacity:.7">Herramientas IA sin barreras para LATAM</div></header>

<div class="target">🎯 Interceptando búsquedas de: <strong>{target_creador}</strong></div>

<h1>{nombre} <em>en México 2026: Precio real en pesos</em></h1>

<div class="meta">
<span>📁 {categoria}</span>
<span>🌍 {origen}</span>
<span>📅 Marzo 2026</span>
<span>💱 $20.30 MXN/USD</span>
</div>

<div class="veredicto">✅ {veredicto}</div>

<h2>¿Qué es?</h2>
<p>{que_es}</p>

<h2>💰 Precios en México</h2>
<div class="precios">
<div class="plan">
<div class="plan-name">Gratis</div>
<div class="plan-price">$0 <small>MXN/mes</small></div>
<p style="font-size:.9rem;color:#ccc;margin-top:.5rem">{gratis_desc}</p>
<div class="limit">⚠️ {gratis_limite}</div>
</div>
<div class="plan paid">
<div class="plan-name">Pro</div>
<div class="plan-price">${precio_mxn} <small>MXN/mes (${precio_usd} USD)</small></div>
<p style="font-size:.9rem;color:#ccc;margin-top:.5rem">Sin límites, acceso completo</p>
</div>
</div>

<h2>🚀 Acceso desde México</h2>
<div class="acceso">
<div class="badgets">
<span class="badge {badge_debito}">Débito MX: {txt_debito}</span>
<span class="badge {badge_vpn}">VPN: {txt_vpn}</span>
<span class="badge ok">Disponible: Sí</span>
</div>
<ol>
<li><strong>{paso1_titulo}:</strong> {paso1_desc}</li>
<li><strong>{paso2_titulo}:</strong> {paso2_desc}</li>
<li><strong>{paso3_titulo}:</strong> {paso3_desc}</li>
</ol>
</div>

<div class="truco">
<strong>💡 Lo que el influencer no te dijo</strong>
{truco}
</div>

<h2>🌏 Alternativa asiática: {alt_nombre}</h2>
<div class="alt">
<strong>{alt_nombre}</strong> — {alt_desc}
<small>{alt_ventaja}</small>
</div>

<h2>❓ FAQs</h2>
<details>
<summary>{faq1_pregunta}</summary>
<p>{faq1_respuesta}</p>
</details>
<details>
<summary>{faq2_pregunta}</summary>
<p>{faq2_respuesta}</p>
</details>
<details>
<summary>{faq3_pregunta}</summary>
<p>{faq3_respuesta}</p>
</details>

<a href="/LLM4US/" class="cta">🔍 Más herramientas en AI4US</a>

<footer>
<strong>AI4US</strong> — La Plaza de la IA para México y LATAM<br>
Marzo 2026 · Sin afiliados, solo información útil<br>
<a href="https://github.com/ConsultorETIAS/LLM4US">GitHub</a>
</footer>
</body></html>"""

def generar_pagina(tool):
    """Genera una página pSEO"""
    nombre = tool["nombre"]
    slug = tool["slug"]
    usd = tool["usd"]
    mxn = int(usd * TC)
    
    print(f"\n🔄 {nombre}...")
    
    prompt = f"""Genera JSON para {nombre} ({tool['categoria']}, {tool['origen']})
Precio: ${usd} USD = ${mxn} MXN | Alternativa: {tool['alt']}
Target: {tool['target_creador']}

JSON requerido:
{{
"titulo": "{nombre} en México 2026: precio en pesos y guía real",
"meta_desc": "Guía {nombre} México. Precio pesos, acceso débito, alternativa {tool['alt']}.",
"veredicto": "Cuándo usar {nombre} vs {tool['alt']} (1 oración)",
"que_es": "2 párrafos: qué hace + ejemplo CDMX + por qué viral",
"gratis_desc": "Qué incluye plan gratis",
"gratis_limite": "Límite principal plan gratis",
"acepta_debito_mx": true,
"requiere_vpn": false,
"paso1_titulo": "Registro",
"paso1_desc": "URL y cómo registrarse desde México",
"paso2_titulo": "Verificación", 
"paso2_desc": "Cómo verificar cuenta",
"paso3_titulo": "Pago/Acceso",
"paso3_desc": "Cómo pagar con débito mexicano o usar gratis",
"truco": "Dato útil que influencers ocultan (2 oraciones)",
"alt_nombre": "{tool['alt']}",
"alt_desc": "Descripción alternativa asiática",
"alt_ventaja": "Ventaja vs {nombre}",
"faq1_pregunta": "¿{nombre} funciona en español de México?",
"faq1_respuesta": "Respuesta honesta sobre idioma",
"faq2_pregunta": "¿Gratis desde México sin VPN?",
"faq2_respuesta": "Límites y requisitos",
"faq3_pregunta": "¿{nombre} o {tool['alt']}?",
"faq3_respuesta": "Veredicto directo 2 oraciones"
}}"""

    datos = llamar_gemini(prompt)
    if not datos:
        return None
    
    try:
        html = TEMPLATE_HTML.format(
            titulo=datos.get("titulo", f"{nombre} México 2026"),
            meta_desc=datos.get("meta_desc", ""),
            target_creador=tool["target_creador"],
            nombre=nombre,
            categoria=tool["categoria"].upper(),
            origen=tool["origen"],
            veredicto=datos.get("veredicto", ""),
            que_es=datos.get("que_es", ""),
            gratis_desc=datos.get("gratis_desc", ""),
            gratis_limite=datos.get("gratis_limite", ""),
            precio_mxn=mxn,
            precio_usd=usd,
            badge_debito="ok" if datos.get("acepta_debito_mx") else "bad",
            txt_debito="Sí" if datos.get("acepta_debito_mx") else "No directo",
            badge_vpn="bad" if datos.get("requiere_vpn") else "ok",
            txt_vpn="Sí" if datos.get("requiere_vpn") else "No",
            paso1_titulo=datos.get("paso1_titulo", "Paso 1"),
            paso1_desc=datos.get("paso1_desc", ""),
            paso2_titulo=datos.get("paso2_titulo", "Paso 2"),
            paso2_desc=datos.get("paso2_desc", ""),
            paso3_titulo=datos.get("paso3_titulo", "Paso 3"),
            paso3_desc=datos.get("paso3_desc", ""),
            truco=datos.get("truco", ""),
            alt_nombre=datos.get("alt_nombre", tool["alt"]),
            alt_desc=datos.get("alt_desc", ""),
            alt_ventaja=datos.get("alt_ventaja", ""),
            faq1_pregunta=datos.get("faq1_pregunta", ""),
            faq1_respuesta=datos.get("faq1_respuesta", ""),
            faq2_pregunta=datos.get("faq2_pregunta", ""),
            faq2_respuesta=datos.get("faq2_respuesta", ""),
            faq3_pregunta=datos.get("faq3_pregunta", ""),
            faq3_respuesta=datos.get("faq3_respuesta", "")
        )
        
        ruta = OUT_DIR / f"{slug}-mexico.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"   ✅ {slug}-mexico.html")
        return slug
        
    except Exception as e:
        print(f"   ❌ Error render: {e}")
        return None

def git_deploy():
    """Sube a GitHub"""
    print("\n📤 GitHub...")
    try:
        os.chdir(REPO_DIR)
        subprocess.run(["git", "config", "user.email", "ai4us@local"], capture_output=True)
        subprocess.run(["git", "config", "user.name", "AI4US"], capture_output=True)
        subprocess.run(["git", "add", "docs/herramientas/"], check=True)
        subprocess.run(["git", "commit", "-m", f"AI4US {time.strftime('%Y-%m-%d')}"], check=True)
        r = subprocess.run(["git", "push"], capture_output=True, text=True)
        return r.returncode == 0
    except Exception as e:
        print(f"   ⚠️ {e}")
        return False

# === MAIN ===
print("=" * 50)
print("🤖 AI4US Generator")
print("Fix: gemini-2.0-flash")
print("=" * 50)

if "AIzaSy" not in API_KEY:
    print("❌ Falta API_KEY línea 15")
    sys.exit(1)

generadas = []
for tool in TOOLS:
    if slug := generar_pagina(tool):
        generadas.append(slug)
    time.sleep(2)

print(f"\n{'='*50}")
print(f"📊 {len(generadas)}/5 generadas")

if generadas and git_deploy():
    print("🚀 Deploy OK")
    for s in generadas:
        print(f"   https://consultoretias.github.io/LLM4US/herramientas/{s}-mexico.html")
else:
    print("⚠️ Deploy manual: git push")




















































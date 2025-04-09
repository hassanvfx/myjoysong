import os
from pathlib import Path
from urllib.parse import quote

# Cambia esto si usas otro nombre de repo
BASE_PATH = "myjoysong"
BASE_DIR = Path("songs")
OUTPUT_HTML = "index.html"

html_parts = [
    "<!DOCTYPE html>",
    "<html lang='es'>",
    "<head>",
    "  <meta charset='UTF-8'>",
    "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
    "  <title>JOY & SONG</title>",
    "  <style>",
    "    * { box-sizing: border-box; }",
    "    body { font-family: sans-serif; margin: 0; display: flex; flex-direction: column; }",
    "    .container { display: flex; flex-direction: column; min-height: 100vh; }",
    "    @media(min-width: 768px) { .container { flex-direction: row; } }",
    "    nav { background: #f0f0f0; padding: 1rem; min-width: 220px; display: flex; flex-direction: column; gap: 1rem; }",
    "    nav button { font-size: 1.1rem; padding: 0.75rem 1rem; border: none; cursor: pointer; border-radius: 8px; background: #e0e0e0; text-align: left; }",
    "    nav button.active { background: #c0c0c0; font-weight: bold; }",
    "    main { flex: 1; padding: 2rem; }",
    "    section { display: none; }",
    "    section.active { display: block; }",
    "    audio { width: 100%; max-width: 500px; margin-bottom: 1rem; display: block; }",
    "    .logo-btn { background: #222 !important; color: white; font-size: 1.4rem; text-align: center; cursor: default; }",
    "    .logo-btn:hover { background: #222 !important; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <div class='container'>",
    "    <nav id='menu'>",
    "      <button class='logo-btn' disabled>🎶 JOY & SONG</button>"
]

# Leer categorías
genres = [g for g in sorted(BASE_DIR.iterdir()) if g.is_dir()]

# Generar botones del menú
for genre in genres:
    genre_name = genre.name
    html_parts.append(f"      <button onclick=\"selectCategory('{quote(genre_name)}')\" id='btn-{quote(genre_name)}'>{genre_name}</button>")

html_parts.extend([
    "    </nav>",
    "    <main id='content'>"
])

# Generar secciones de canciones
for genre in genres:
    genre_name = genre.name
    section_id = quote(genre_name)
    html_parts.append(f"      <section id='section-{section_id}'>")
    html_parts.append(f"        <h2>{genre_name}</h2>")

    for song in sorted(genre.glob("*.mp3")):
        song_name = song.stem.replace("_", " ").title()
        song_path = f"{BASE_PATH}/{song.as_posix()}"
        html_parts.append(f"        <p>{song_name}</p>")
        html_parts.append(f"        <audio controls src='{song_path}'></audio>")

    html_parts.append("      </section>")

html_parts.extend([
    "    </main>",
    "  </div>",
    "  <script>",
    "    function selectCategory(cat) {",
    "      const sections = document.querySelectorAll('section');",
    "      const buttons = document.querySelectorAll('nav button');",
    "      sections.forEach(sec => sec.classList.remove('active'));",
    "      buttons.forEach(btn => btn.classList.remove('active'));",
    "      const target = document.getElementById('section-' + cat);",
    "      const btn = document.getElementById('btn-' + cat);",
    "      if (target) target.classList.add('active');",
    "      if (btn) btn.classList.add('active');",
    "      const url = new URL(window.location);",
    "      url.searchParams.set('categoria', cat);",
    "      history.pushState({}, '', url);",
    "    }",
    "    function init() {",
    "      const params = new URLSearchParams(window.location.search);",
    "      const cat = params.get('categoria');",
    "      if (cat && document.getElementById('section-' + cat)) {",
    "        selectCategory(cat);",
    "      } else if (document.querySelector('section')) {",
    "        const first = document.querySelector('section').id.replace('section-', '');",
    "        selectCategory(first);",
    "      }",
    "    }",
    "    window.onload = init;",
    "  </script>",
    "</body>",
    "</html>"
])

# Guardar el HTML
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print(f"✅ ¡Página generada en '{OUTPUT_HTML}' lista para GitHub Pages en '{BASE_PATH}/'!")

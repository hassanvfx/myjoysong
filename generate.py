import os
import unicodedata
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path("songs")
OUTPUT_HTML = "index.html"

def normalize_name(name):
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_only = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    ascii_only = ascii_only.replace("ñ", "n").replace("Ñ", "n")
    ascii_only = ascii_only.lower().replace(" ", "_")
    return ascii_only

# Renombrar carpetas y archivos
for genre_path in list(BASE_DIR.iterdir()):
    if genre_path.is_dir():
        normalized_genre = normalize_name(genre_path.name)
        new_genre_path = genre_path.parent / normalized_genre
        if genre_path != new_genre_path:
            os.rename(genre_path, new_genre_path)
            print(f"📁 Renombrado: {genre_path.name} → {new_genre_path.name}")
        for song_file in new_genre_path.glob("*.mp3"):
            normalized_song = normalize_name(song_file.name)
            new_song_path = song_file.parent / normalized_song
            if song_file != new_song_path:
                os.rename(song_file, new_song_path)
                print(f"🎵 Renombrado: {song_file.name} → {new_song_path.name}")

# Leer estructura normalizada
genres = [g for g in sorted(BASE_DIR.iterdir()) if g.is_dir()]

# Iniciar HTML
html_parts = [
    "<!DOCTYPE html>",
    "<html lang='es'>",
    "<head>",
    "  <meta charset='UTF-8'>",
    "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
    "  <title>Joy & Song</title>",
    "  <style>",
    "    * { box-sizing: border-box; }",
    "    body { font-family: sans-serif; margin: 0; display: flex; flex-direction: column; scroll-behavior: smooth; }",
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
    "    .whatsapp-btn {",
    "         background: #25D366 !important;",
    "         color: white !important;",
    "         font-size: 1.1rem;",
    "         padding: 0.75rem 1rem;",
    "         border: none;",
    "         border-radius: 8px;",
    "         cursor: pointer;",
    "         text-align: left;",
    "         width: 100%;",
    "    }",
    "    .whatsapp-btn:hover {",
    "         background: #1ebe5d !important;",
    "    }",
    "  </style>",
    "</head>",
    "<body>",
    "  <div class='container'>",
    "    <nav id='menu'>",
    "      <button class='logo-btn' disabled>🎹 JOY & SONG</button>",
    "      <a href='https://wa.me/5215574179877' target='_blank' style='text-decoration: none;'>",
    "        <button class='whatsapp-btn'>📞 PIDE TU CANCION</button>",
    "      </a>"
]

# Menú de navegación
for genre in genres:
    genre_name = genre.name
    display_name = genre_name.replace('_', ' ').title()
    html_parts.append(f"      <button onclick=\"selectCategory('{quote(genre_name)}')\" id='btn-{quote(genre_name)}'>{display_name}</button>")

html_parts.extend([
    "    </nav>",
    "    <main id='content'>"
])

# Secciones de música
for genre in genres:
    genre_name = genre.name
    section_id = quote(genre_name)
    display_name = genre_name.replace('_', ' ').title()
    html_parts.append(f"      <section id='section-{section_id}'>")
    html_parts.append(f"        <h2>{display_name}</h2>")

    for song in sorted(genre.glob("*.mp3")):
        song_name = song.stem.replace("_", " ").title()
        song_path = song.as_posix()
        html_parts.append(f"        <p>{song_name}</p>")
        html_parts.append(f"        <audio controls src='{song_path}'></audio>")

    html_parts.append("      </section>")

# Footer y JS
html_parts.extend([
    "    </main>",
    "  </div>",
    "  <script>",
    "    function scrollToContent() {",
    "      const content = document.getElementById('content');",
    "      if (content) content.scrollIntoView({ behavior: 'smooth' });",
    "    }",
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
    "      document.title = 'Joy & Song – ' + btn.innerText;",
    "      scrollToContent();",
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

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print("✅ HTML actualizado con scroll, título dinámico, pianito 🎹 y el botón de WhatsApp. ¡Listo para publicar!")

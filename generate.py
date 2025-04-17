import os
import unicodedata
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path("songs")
OUTPUT_HTML = "index.html"

def normalize_name(name):
    nfkd = unicodedata.normalize("NFKD", name)
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
        
        for item in list(new_genre_path.iterdir()):
            if item.is_dir():
                normalized_subfolder = normalize_name(item.name)
                new_subfolder_path = item.parent / normalized_subfolder
                if item != new_subfolder_path:
                    os.rename(item, new_subfolder_path)
                    print(f"📁 Renombrado: {item.name} → {new_subfolder_path.name}")
                for song_file in new_subfolder_path.glob("*.mp3"):
                    normalized_song = normalize_name(song_file.name)
                    new_song_path = song_file.parent / normalized_song
                    if song_file != new_song_path:
                        os.rename(song_file, new_song_path)
                        print(f"🎵 Renombrado: {song_file.name} → {new_song_path.name}")
            elif item.is_file() and item.suffix.lower() == ".mp3":
                normalized_song = normalize_name(item.name)
                new_song_path = item.parent / normalized_song
                if item != new_song_path:
                    os.rename(item, new_song_path)
                    print(f"🎵 Renombrado: {item.name} → {new_song_path.name}")

genres = [g for g in sorted(BASE_DIR.iterdir()) if g.is_dir()]

html_parts = [
    "<!DOCTYPE html>",
    "<html lang='es'>",
    "<head>",
    "  <meta charset='UTF-8'>",
    "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
    "  <title>Joy & Song</title>",
    "  <style>",
    "    * { box-sizing: border-box; }",
    "    body { font-family: sans-serif; margin: 0; display: flex; flex-direction: column; scroll-behavior: smooth; background: #f8f8f8; }",
    "    .container { display: flex; flex-direction: row; min-height: 100vh; }",
    "    @media(max-width: 768px) { .container { flex-direction: column; } }",
    "    header#mobile-header { display: none; text-align: center; padding: 0.5rem; background: #222; }",
    "    header#mobile-header img { max-width: 100px; height: auto; }",
    "    @media(max-width:768px) { header#mobile-header { display: block; } nav .nav-logo { display: none; } }",
    "    nav { background: #222; padding: 1rem; min-width: 220px; display: flex; flex-direction: column; gap: 1rem; }",
    "    #mobile-toggle { display: none; padding: 0.75rem 1.5rem; font-size: 1.1rem; margin-bottom: 1rem; cursor: pointer; background: #444; color: #fff; border: none; border-radius: 8px; transition: background 0.3s; }",
    "    @media (max-width: 768px) { #mobile-toggle { display: block; margin: 1rem auto; } nav { display: none; } }",
    "    .social-buttons { display: flex; justify-content: space-around; gap: 0.5rem; }",
    "    .social-button { font-size: 0.9rem; padding: 0.5rem; text-align: center; text-decoration: none; border-radius: 5px; border: 1px solid transparent; }",
    "    .social-button.youtube { background: #222; border-color: #ff0000; color: #ff0000; }",
    "    .social-button.spotify { background: #222; border-color: #1DB954; color: #1DB954; }",
    "    .social-button img { max-width: 30px; max-height: 30px; vertical-align: middle; }",
    "    nav button { font-size: 1.1rem; padding: 0.75rem 1rem; border: none; cursor: pointer; border-radius: 8px; background: #444; color: #fff; text-align: left; transition: background 0.3s; }",
    "    nav button:hover { background: #555; }",
    "    nav button.active { background: #000; color: #fff; font-weight: bold; }",
    "    main { flex: 1; padding: 2rem; background: #fff; }",
    "    .banner { background: #222; color: #fff; padding: 1rem; text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; }",
    "    section { display: none; margin-bottom: 2rem; }",
    "    section.active { display: block; }",
    "    audio { width: 100%; max-width: 500px; margin-top: 0.5rem; display: block; }",
    "    .whatsapp-btn {",
    "      background: #1B8E34 !important;",
    "      color: white !important;",
    "      font-size: 1.1rem;",
    "      padding: 0.5rem 1rem;",
    "      border: none;",
    "      border-radius: 8px;",
    "      cursor: pointer;",
    "      text-align: center;",
    "      display: inline-block;",
    "      margin-bottom: 0.5rem;",
    "      transition: background 0.3s;",
    "    }",
    "    .whatsapp-btn:hover { background: #15712A !important; }",
    "    .nav-logo { max-width: 200px; height: auto; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <header id='mobile-header'>",
    "    <img src='images/logo.jpg' alt='Logo Mobile'>",
    "  </header>",
    "  <div class='container'>",
    "    <button id='mobile-toggle' onclick='showMenu()'>VER MENU COMPLETO</button>",
    "    <nav id='menu'>",
    "      <img src='images/logo.jpg' alt='Logo' class='nav-logo'>",
    "      <div class='social-buttons'>",
    "        <a href='https://www.youtube.com/@myjoysong' target='_blank' class='social-button youtube'><img src='images/youtube.png' alt='YouTube'> YouTube</a>",
    "        <a href='https://open.spotify.com/artist/5RhN6e7pSwsEOkjBBIBSGQ?si=1Ua3S2KCRSO8zftqhk8CTQ' target='_blank' class='social-button spotify'><img src='images/spotify.png' alt='Spotify'> Spotify</a>",
    "      </div>",
    "      <a href='https://wa.me/5215574179877' target='_blank' style='text-decoration: none;'>",
    "        <button class='whatsapp-btn'><img src='images/whatsapp.svg' alt='WhatsApp' style='vertical-align: middle; max-width:20px; margin-right: 5px;'> PIDE TU CANCION</button>",
    "      </a>"
]

# Botones de géneros
for genre in genres:
    gn = genre.name
    disp = gn.replace('_', ' ').title()
    html_parts.append(f"      <button onclick=\"selectCategory('{quote(gn)}')\" id='btn-{quote(gn)}'>{disp}</button>")
html_parts.append("      <button onclick=\"selectCategory('all')\" id='btn-all'>TODOS LOS HITS</button>")

html_parts.extend([
    "    </nav>",
    "    <main id='content'>",
    "      <div class='banner'>CANCIONES 100% TU VIDA Y TU MUSICA FAVORITA</div>"
])

# Secciones por género con botón como caption bajo el título
for genre in genres:
    gn = genre.name
    sid = quote(gn)
    disp = gn.replace('_', ' ').title()
    html_parts.append(f"      <section id='section-{sid}'>")
    html_parts.append(f"        <h2>{disp}</h2>")
    
    subs = sorted(item for item in genre.iterdir() if item.is_dir())
    if subs:
        for sub in subs:
            sub_disp = sub.name.replace('_', ' ').title()
            html_parts.append(f"        <h3>{sub_disp}</h3>")
            for song in sorted(sub.glob("*.mp3")):
                title = song.stem.replace("_", " ").title()
                path = song.as_posix()
                html_parts.append(f"        <p>{title}</p>")
                html_parts.append(
                    "        <a href='https://wa.me/5215574179877?text="
                    + quote(f"#quiero {title}")
                    + "' target='_blank'><button class='whatsapp-btn'>Personalizar esta canción</button></a>"
                )
                html_parts.append(f"        <audio controls src='{path}'></audio>")
    else:
        for song in sorted(genre.glob("*.mp3")):
            title = song.stem.replace("_", " ").title()
            path = song.as_posix()
            html_parts.append(f"        <p>{title}</p>")
            html_parts.append(
                "        <a href='https://wa.me/5215574179877?text="
                + quote(f"#quiero {title}")
                + "' target='_blank'><button class='whatsapp-btn'>Personalizar esta canción</button></a>"
            )
            html_parts.append(f"        <audio controls src='{path}'></audio>")
    html_parts.append("      </section>")

# Sección "Todos los Hits"
html_parts.append("      <section id='section-all'>")
html_parts.append("        <h2>TODOS LOS HITS</h2>")
for genre in genres:
    gdisp = genre.name.replace('_', ' ').title()
    direct = sorted(genre.glob("*.mp3"))
    if direct:
        html_parts.append(f"        <h3>{gdisp}</h3>")
        for song in direct:
            title = song.stem.replace("_", " ").title()
            path = song.as_posix()
            html_parts.append(f"        <p>{title}</p>")
            html_parts.append(
                "        <a href='https://wa.me/5215574179877?text="
                + quote(f"#quiero {title}")
                + "' target='_blank'><button class='whatsapp-btn'>Personalizar esta canción</button></a>"
            )
            html_parts.append(f"        <audio controls src='{path}'></audio>")
    subs = sorted(item for item in genre.iterdir() if item.is_dir())
    for sub in subs:
        header = f"{gdisp} - {sub.name.replace('_',' ').title()}"
        html_parts.append(f"        <h3>{header}</h3>")
        for song in sorted(sub.glob("*.mp3")):
            title = song.stem.replace("_", " ").title()
            path = song.as_posix()
            html_parts.append(f"        <p>{title}</p>")
            html_parts.append(
                "        <a href='https://wa.me/5215574179877?text="
                + quote(f"#quiero {title}")
                + "' target='_blank'><button class='whatsapp-btn'>Personalizar esta canción</button></a>"
            )
            html_parts.append(f"        <audio controls src='{path}'></audio>")
html_parts.append("      </section>")

# Scripts
html_parts.extend([
    "    </main>",
    "  </div>",
    "  <script>",
    "    function showMenu() { document.getElementById('menu').style.display = 'flex'; document.getElementById('mobile-toggle').style.display = 'none'; }",
    "    function hideMenu() { document.getElementById('menu').style.display = 'none'; document.getElementById('mobile-toggle').style.display = 'block'; }",
    "    function scrollToContent() { const c = document.getElementById('content'); if(c) c.scrollIntoView({ behavior: 'smooth' }); }",
    "    function selectCategory(cat) {",
    "      const secs = document.querySelectorAll('section'), btns = document.querySelectorAll('nav button');",
    "      secs.forEach(s=>s.classList.remove('active')); btns.forEach(b=>b.classList.remove('active'));",
    "      const t = document.getElementById('section-'+cat), b = document.getElementById('btn-'+cat);",
    "      if(t) t.classList.add('active'); if(b) b.classList.add('active');",
    "      const u = new URL(window.location); u.searchParams.set('categoria', cat); history.pushState({}, '', u);",
    "      document.title = 'Joy & Song – ' + (b ? b.innerText : ''); scrollToContent(); if(window.innerWidth<=768) hideMenu();",
    "    }",
    "    function init() { const p=new URLSearchParams(window.location.search).get('categoria'); if(p&&document.getElementById('section-'+p)) selectCategory(p); else if(document.querySelector('section')) selectCategory(document.querySelector('section').id.replace('section-','')); }",
    "    window.onload = function() { init(); let current=null; document.querySelectorAll('audio').forEach(a=>{ a.addEventListener('play',function(){ if(current&&current!==this){ current.pause(); current.currentTime=0; } current=this; }); a.addEventListener('ended',function(){ const sec=document.querySelector('section.active'); if(sec){ const auds=Array.from(sec.querySelectorAll('audio')), idx=auds.indexOf(this); if(idx!==-1&&idx<auds.length-1) auds[idx+1].play(); } }); }); };",
    "  </script>",
    "</body>",
    "</html>"
])

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print("✅ HTML actualizado: botón contenido como caption y texto '#quiero <canción>' añadido.")

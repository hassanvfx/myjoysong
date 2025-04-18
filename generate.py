import os
import unicodedata
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path("songs")
OUTPUT_HTML = "index.html"
#ready
def normalize_name(name):
    """Normaliza nombres de archivos y carpetas"""
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_only = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    ascii_only = ascii_only.replace("ñ", "n").replace("Ñ", "n")
    ascii_only = ascii_only.lower().replace(" ", "_")
    return ascii_only

def rename_folders_and_files():
    """Renombra carpetas y archivos normalizando sus nombres"""
    for genre_path in list(BASE_DIR.iterdir()):
        if genre_path.is_dir():
            normalized_genre = normalize_name(genre_path.name)
            new_genre_path = genre_path.parent / normalized_genre
            if genre_path != new_genre_path:
                os.rename(genre_path, new_genre_path)
                print(f"📁 Renombrado: {genre_path.name} → {new_genre_path.name}")
            
            process_genre_folder(new_genre_path)

def process_genre_folder(genre_path):
    """Procesa carpetas de género y sus contenidos"""
    for item in list(genre_path.iterdir()):
        if item.is_dir():
            normalized_subfolder = normalize_name(item.name)
            new_subfolder_path = item.parent / normalized_subfolder
            if item != new_subfolder_path:
                os.rename(item, new_subfolder_path)
                print(f"📁 Renombrado: {item.name} → {new_subfolder_path.name}")
            
            rename_mp3_files(new_subfolder_path)
        elif item.is_file() and item.suffix.lower() == ".mp3":
            rename_mp3_file(item)

def rename_mp3_files(folder_path):
    """Renombra todos los archivos MP3 en una carpeta"""
    for song_file in folder_path.glob("*.mp3"):
        rename_mp3_file(song_file)

def rename_mp3_file(song_file):
    """Renombra un archivo MP3 individual"""
    normalized_song = normalize_name(song_file.name)
    new_song_path = song_file.parent / normalized_song
    if song_file != new_song_path:
        os.rename(song_file, new_song_path)
        print(f"🎵 Renombrado: {song_file.name} → {new_song_path.name}")

def format_display_name(name):
    """Formatea un nombre para mostrar"""
    return name.replace('_', ' ').title()

def generate_css():
    """Genera el código CSS para la página"""
    return """
    * { box-sizing: border-box; }
    body { font-family: sans-serif; margin: 0; display: flex; flex-direction: column; scroll-behavior: smooth; background: #f8f8f8; }
    .container { display: flex; flex-direction: row; min-height: 100vh; }
    @media(max-width: 768px) { .container { flex-direction: column; } }
    
    /* Header mobile: siempre visible en mobile */
    header#mobile-header {
        display: none;
        text-align: center;
        padding: 0.5rem;
        background: #222;
    }
    header#mobile-header img {
        max-width: 100px;
        height: auto;
    }
    @media(max-width:768px) {
        header#mobile-header { display: block; }
        nav .nav-logo { display: none; }
    }
    
    nav { background: #222; padding: 1rem; min-width: 220px; display: flex; flex-direction: column; gap: 1rem; }
    
    /* Botón para alternar menú en mobile */
    #mobile-toggle {
        display: none;
        width: auto;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        cursor: pointer;
        background: #444;
        color: #fff;
        border: none;
        border-radius: 8px;
        transition: background 0.3s;
    }
    @media (max-width: 768px) {
        #mobile-toggle { display: block; margin: 1rem auto; }
        nav { display: none; flex-direction: column; }
    }
    
    /* Social buttons con íconos limitados en tamaño */
    .social-buttons { display: flex; justify-content: space-around; gap: 0.5rem; }
    .social-button { font-size: 0.9rem; padding: 0.5rem; text-align: center; text-decoration: none; border-radius: 5px; border: 1px solid transparent; }
    .social-button.youtube { background: #222; border-color: #ff0000; color: #ff0000; }
    .social-button.spotify { background: #222; border-color: #1DB954; color: #1DB954; }
    .social-button img { max-width: 30px; max-height: 30px; vertical-align: middle; }
    
    /* Botones de género y opciones */
    nav button { font-size: 1.1rem; padding: 0.75rem 1rem; border: none; cursor: pointer; border-radius: 8px; background: #444; color: #fff; text-align: left; transition: background 0.3s; }
    nav button:hover { background: #555; }
    nav button.active { background: #000; color: #fff; font-weight: bold; }
    main { flex: 1; padding: 2rem; background: #fff; }
    
    /* Estilos para el cintillo/banner */
    .banner {
        background: #222;
        color: #fff;
        padding: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    section { display: none; }
    section.active { display: block; }
    audio { width: 100%; max-width: 500px; margin-bottom: 1rem; display: block; }
    
    /* WhatsApp button styling */
    .whatsapp-btn {
        background: #1B8E34 !important;
        color: white !important;
        font-size: 1.1rem;
        padding: 0.75rem 1rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
        width: 100%;
        transition: background 0.3s;
    }
    .whatsapp-btn:hover {
        background: #15712A !important;
    }
    
    /* WhatsApp button styling2 */
    .whatsapp-btn2 {
        background: #1B8E34 !important;
        color: white !important;
        font-size: 1.1rem;
        padding: 0.75rem 1rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
        width: auto;
        transition: background 0.3s;
        margin-bottom: 0.5rem;
    }
    .whatsapp-btn2:hover {
        background: #15712A !important;
    }
    
    .nav-logo { max-width: 200px; height: auto; }
    """

def generate_javascript():
    """Genera el código JavaScript para la página"""
    return """
    function showMenu() {
      document.getElementById('menu').style.display = 'flex';
      document.getElementById('mobile-toggle').style.display = 'none';
    }
    
    function hideMenu() {
      document.getElementById('menu').style.display = 'none';
      document.getElementById('mobile-toggle').style.display = 'block';
    }
    
    function scrollToContent() {
      const content = document.getElementById('content');
      if (content) content.scrollIntoView({ behavior: 'smooth' });
    }
    
    function selectCategory(cat) {
      const sections = document.querySelectorAll('section');
      const buttons = document.querySelectorAll('nav button');
      sections.forEach(sec => sec.classList.remove('active'));
      buttons.forEach(btn => btn.classList.remove('active'));
      const target = document.getElementById('section-' + cat);
      const btn = document.getElementById('btn-' + cat);
      if (target) target.classList.add('active');
      if (btn) btn.classList.add('active');
      const url = new URL(window.location);
      url.searchParams.set('categoria', cat);
      history.pushState({}, '', url);
      document.title = 'Joy & Song – ' + (btn ? btn.innerText : '');
      scrollToContent();
      if (window.innerWidth <= 768) { hideMenu(); }
    }
    
    function init() {
      const params = new URLSearchParams(window.location.search);
      const cat = params.get('categoria');
      if (cat && document.getElementById('section-' + cat)) {
        selectCategory(cat);
      } else if (document.querySelector('section')) {
        const first = document.querySelector('section').id.replace('section-', '');
        selectCategory(first);
      }
    }
    
    window.onload = function() {
      init();
      const audios = document.querySelectorAll('audio');
      let currentAudio = null;
      audios.forEach(audio => {
        audio.addEventListener('play', function() {
          if (currentAudio && currentAudio !== this) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
          }
          currentAudio = this;
        });
        audio.addEventListener('ended', function() {
          const activeSection = document.querySelector('section.active');
          if (activeSection) {
            const sectionAudios = Array.from(activeSection.querySelectorAll('audio'));
            const index = sectionAudios.indexOf(this);
            if (index !== -1 && index < sectionAudios.length - 1) {
              sectionAudios[index + 1].play();
            }
          }
        });
      });
    };
    """

def generate_whatsapp_button(song_name):
    """Genera un botón de WhatsApp para personalizar una canción"""
    return (
        f"<a href='https://wa.me/5215574179877?text=%23quiero%20{quote(song_name)}' target='_blank'>"
        "<button class='whatsapp-btn2'>Personalizar esta canción</button>"
        "</a>"
    )

def render_song(song_file):
    """Renderiza un elemento de canción con su audio y botón"""
    song_name = song_file.stem.replace("_", " ").title()
    song_path = song_file.as_posix()
    html = []
    html.append(f"<p>{song_name}</p>")
    html.append(generate_whatsapp_button(song_name))
    html.append(f"<audio controls src='{song_path}'></audio>")
    return "\n".join(html)

def render_genre_section(genre):
    """Renderiza la sección de un género musical"""
    genre_name = genre.name
    section_id = quote(genre_name)
    display_name = format_display_name(genre_name)
    html = []
    html.append(f"<section id='section-{section_id}'>")
    html.append(f"<h2>{display_name}</h2>")
    
    subfolders = sorted(item for item in genre.iterdir() if item.is_dir())
    if subfolders:
        for sub in subfolders:
            sub_display = format_display_name(sub.name)
            html.append(f"<h3>{sub_display}</h3>")
            for song_file in sorted(sub.glob("*.mp3")):
                html.append(render_song(song_file))
    else:
        for song_file in sorted(genre.glob("*.mp3")):
            html.append(render_song(song_file))
    html.append("</section>")
    return "\n".join(html)

def render_all_hits_section(genres):
    """Renderiza la sección "Todos los Hits" con todas las canciones"""
    html = []
    html.append("<section id='section-all'>")
    html.append("<h2>TODOS LOS HITS</h2>")
    
    for genre in genres:
        genre_display = format_display_name(genre.name)
        direct_songs = sorted(genre.glob("*.mp3"))
        if direct_songs:
            html.append(f"<h3>{genre_display}</h3>")
            for song_file in direct_songs:
                html.append(render_song(song_file))
        
        subfolders = sorted(item for item in genre.iterdir() if item.is_dir())
        for sub in subfolders:
            header = f"{genre_display} - {format_display_name(sub.name)}"
            html.append(f"<h3>{header}</h3>")
            for song_file in sorted(sub.glob("*.mp3")):
                html.append(render_song(song_file))
    
    html.append("</section>")
    return "\n".join(html)

def render_nav_buttons(genres):
    """Renderiza los botones de navegación por género"""
    html = []
    for genre in genres:
        genre_name = genre.name
        display_name = format_display_name(genre_name)
        html.append(f"<button onclick=\"selectCategory('{quote(genre_name)}')\" id='btn-{quote(genre_name)}'>{display_name}</button>")
    html.append("<button onclick=\"selectCategory('all')\" id='btn-all'>TODOS LOS HITS</button>")
    return "\n".join(html)

def generate_html():
    """Genera el documento HTML completo"""
    # Primero renombrar carpetas y archivos
    rename_folders_and_files()
    
    # Recopilar géneros
    genres = [g for g in sorted(BASE_DIR.iterdir()) if g.is_dir()]
    
    # Construir el HTML
    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='es'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "  <title>Joy & Song</title>",
        "  <style>",
        generate_css(),
        "  </style>",
        "</head>",
        "<body>",
        "  <header id='mobile-header'>",
        "      <img src='images/logo.jpg' alt='Logo Mobile'>",
        "  </header>",
        "  <div class='container'>",
        "    <button id='mobile-toggle' onclick='showMenu()'>VER MENU COMPLETO</button>",
        "    <nav id='menu'>",
        "      <img src='images/logo.jpg' alt='Logo' class='nav-logo'>",
        "      <div class='social-buttons'>",
        "         <a href='https://www.youtube.com/@myjoysong' target='_blank' class='social-button youtube'>",
        "           <img src='images/youtube.png' alt='YouTube'> YouTube",
        "         </a>",
        "         <a href='https://open.spotify.com/artist/5RhN6e7pSwsEOkjBBIBSGQ?si=1Ua3S2KCRSO8zftqhk8CTQ' target='_blank' class='social-button spotify'>",
        "           <img src='images/spotify.png' alt='Spotify'> Spotify",
        "         </a>",
        "      </div>",
        "      <a href='https://wa.me/5215574179877' target='_blank' style='text-decoration: none;'>",
        "        <button class='whatsapp-btn'><img src='images/whatsapp.svg' alt='WhatsApp' style='vertical-align: middle; max-width:20px; margin-right: 5px;'> PIDE TU CANCION</button>",
        "      </a>",
        render_nav_buttons(genres),
        "    </nav>",
        "    <main id='content'>",
        "      <div class='banner'>CANCIONES 100% TU VIDA Y TU MUSICA FAVORITA</div>"
    ]

    # Agregar secciones por género
    for genre in genres:
        html_parts.append(render_genre_section(genre))
    
    # Agregar sección "Todos los Hits"
    html_parts.append(render_all_hits_section(genres))

    # Agregar scripts y cierre del documento
    html_parts.extend([
        "    </main>",
        "  </div>",
        "  <script>",
        generate_javascript(),
        "  </script>",
        "</body>",
        "</html>"
    ])

    return "\n".join(html_parts)

def main():
    """Función principal que genera el archivo HTML"""
    html_content = generate_html()
    
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ HTML actualizado correctamente con botón de personalización para cada canción.")

if __name__ == "__main__":
    main()
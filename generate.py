import os
import unicodedata
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path("songs")
OUTPUT_HTML = "index.html"

def normalize_name(name):
    """Normaliza un nombre eliminando acentos, espacios y caracteres especiales"""
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_only = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    ascii_only = ascii_only.replace("ñ", "n").replace("Ñ", "n")
    ascii_only = ascii_only.lower().replace(" ", "_")
    return ascii_only

def rename_items(base_path):
    """Renombra recursivamente carpetas y archivos MP3 según la función normalize_name"""
    if base_path.is_dir():
        normalized_path_name = normalize_name(base_path.name)
        new_path = base_path.parent / normalized_path_name
        
        # Renombrar la carpeta actual si es necesario
        if base_path != new_path:
            os.rename(base_path, new_path)
            print(f"📁 Renombrado: {base_path.name} → {new_path.name}")
            base_path = new_path
        
        # Procesar elementos dentro de la carpeta
        for item in list(base_path.iterdir()):
            if item.is_dir():
                rename_items(item)
            elif item.is_file() and item.suffix.lower() == ".mp3":
                normalized_file_name = normalize_name(item.name)
                new_file_path = item.parent / normalized_file_name
                if item != new_file_path:
                    os.rename(item, new_file_path)
                    print(f"🎵 Renombrado: {item.name} → {new_file_path.name}")

def get_css():
    """Retorna el CSS completo para la página"""
    return """
    * { box-sizing: border-box; }
    body { font-family: sans-serif; margin: 0; display: flex; flex-direction: column; scroll-behavior: smooth; background: #f8f8f8; }
    .container { display: flex; flex-direction: row; min-height: 100vh; }
    @media(max-width: 768px) { .container { flex-direction: column; } }
    
    /* Estilos para el indicador de carga */
    .audio-container { position: relative; margin-bottom: 1rem; }
    .loading-overlay { 
        position: absolute; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%; 
        background: #fff; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        z-index: 2;
    }
    .loading-spinner {
        display: inline-block;
        width: 1.5rem;
        height: 1.5rem;
        margin-right: 0.5rem;
        border: 3px solid rgba(0, 0, 0, 0.1);
        border-radius: 50%;
        border-top-color: #222;
        animation: spin 1s ease-in-out infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Header mobile */
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
    
    /* Navegación */
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
    
    /* Social buttons */
    .social-buttons { display: flex; justify-content: space-around; gap: 0.5rem; }
    .social-button { font-size: 0.9rem; padding: 0.5rem; text-align: center; text-decoration: none; border-radius: 5px; border: 1px solid transparent; }
    .social-button.youtube { background: #222; border-color: #ff0000; color: #ff0000; }
    .social-button.spotify { background: #222; border-color: #1DB954; color: #1DB954; }
    .social-button img { max-width: 30px; max-height: 30px; vertical-align: middle; }
    
    /* Botones de navegación */
    nav button { font-size: 1.1rem; padding: 0.75rem 1rem; border: none; cursor: pointer; border-radius: 8px; background: #444; color: #fff; text-align: left; transition: background 0.3s; }
    nav button:hover { background: #555; }
    nav button.active { background: #000; color: #fff; font-weight: bold; }
    
    /* Contenido principal */
    main { flex: 1; padding: 2rem; background: #fff; }
    
    /* Banner */
    .banner {
         background: #222;
         color: #fff;
         padding: 1rem;
         text-align: center;
         font-size: 1.5rem;
         font-weight: bold;
         margin-bottom: 1rem;
    }
    
    /* Secciones */
    section { display: none; }
    section.active { display: block; }
    audio { width: 100%; max-width: 500px; margin-bottom: 1rem; display: block; }
    
    /* Botones WhatsApp */
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
    }
    .whatsapp-btn2:hover {
         background: #15712A !important;
    }
    
    /* Logo */
    .nav-logo { max-width: 200px; height: auto; }
    """

def get_javascript():
    """Retorna el JavaScript completo para la página"""
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
    
    function setupAudioHandlers() {
      const audios = document.querySelectorAll('audio');
      let currentAudio = null;
      
      audios.forEach(audio => {
        // Manejar la carga de audio
        audio.addEventListener('canplaythrough', function() {
          // Ocultar el overlay de carga cuando el audio esté listo
          const loadingOverlay = this.parentNode.querySelector('.loading-overlay');
          if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
          }
        });
        
        // Gestionar errores de carga
        audio.addEventListener('error', function() {
          const loadingOverlay = this.parentNode.querySelector('.loading-overlay');
          if (loadingOverlay) {
            loadingOverlay.innerHTML = '<span style="color: #ff0000;">Error al cargar el audio</span>';
          }
        });
        
        // Gestionar reproducción única
        audio.addEventListener('play', function() {
          if (currentAudio && currentAudio !== this) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
          }
          currentAudio = this;
        });
        
        // Gestionar reproducción automática del siguiente
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
    }
    
    window.onload = function() {
      init();
      setupAudioHandlers();
    };
    """

def create_song_html(song_file):
    """Genera el HTML para una canción individual"""
    song_name = song_file.stem.replace("_", " ").title()
    song_path = song_file.as_posix()
    
    html = []
    html.append(f"<p>{song_name}</p>")
    html.append(
        f"<a href='https://wa.me/5215574179877?text=%23quiero%20{quote(song_name)}' target='_blank'>"
        f"<button class='whatsapp-btn2'>Personalizar esta canción</button>"
        f"</a>"
    )
    html.append(f"""<div class="audio-container">
        <div class="loading-overlay">
            <div class="loading-spinner"></div>
            <span>Cargando audio...</span>
        </div>
        <audio controls src='{song_path}' oncanplaythrough="this.parentNode.querySelector('.loading-overlay').style.display='none'"></audio>
    </div>""")
    
    return "\n".join(html)

def create_genre_section(genre, section_id):
    """Genera el HTML para una sección de género"""
    display_name = genre.name.replace('_', ' ').title()
    html = []
    html.append(f"<section id='section-{section_id}'>")
    html.append(f"<h2>{display_name}</h2>")
    
    # Procesar subcarpetas si existen
    subfolders = sorted(item for item in genre.iterdir() if item.is_dir())
    if subfolders:
        for sub in subfolders:
            sub_display = sub.name.replace('_', ' ').title()
            html.append(f"<h3>{sub_display}</h3>")
            
            # Procesar canciones en la subcarpeta
            for song_file in sorted(sub.glob("*.mp3")):
                html.append(create_song_html(song_file))
    else:
        # Procesar canciones directamente en el género
        for song_file in sorted(genre.glob("*.mp3")):
            html.append(create_song_html(song_file))
    
    html.append("</section>")
    return "\n".join(html)

def create_all_hits_section(genres):
    """Genera el HTML para la sección de 'Todos los Hits'"""
    html = []
    html.append("<section id='section-all'>")
    html.append("<h2>TODOS LOS HITS</h2>")
    
    for genre in genres:
        genre_display = genre.name.replace('_', ' ').title()
        
        # Canciones directamente en el género
        direct_songs = sorted(genre.glob("*.mp3"))
        if direct_songs:
            html.append(f"<h3>{genre_display}</h3>")
            for song_file in direct_songs:
                html.append(create_song_html(song_file))
        
        # Canciones en subcarpetas
        subfolders = sorted(item for item in genre.iterdir() if item.is_dir())
        for sub in subfolders:
            header = f"{genre_display} - {sub.name.replace('_',' ').title()}"
            html.append(f"<h3>{header}</h3>")
            
            for song_file in sorted(sub.glob("*.mp3")):
                html.append(create_song_html(song_file))
    
    html.append("</section>")
    return "\n".join(html)

def create_navigation_buttons(genres):
    """Genera los botones de navegación para los géneros"""
    html = []
    
    # Botones para cada género
    for genre in genres:
        genre_name = genre.name
        display_name = genre_name.replace('_', ' ').title()
        html.append(f"<button onclick=\"selectCategory('{quote(genre_name)}')\" id='btn-{quote(genre_name)}'>{display_name}</button>")
    
    # Botón para todos los hits
    html.append("<button onclick=\"selectCategory('all')\" id='btn-all'>TODOS LOS HITS</button>")
    
    return "\n".join(html)

def generate_html():
    """Genera el archivo HTML completo"""
    # Renombrar archivos y carpetas
    for genre_path in list(BASE_DIR.iterdir()):
        if genre_path.is_dir():
            rename_items(genre_path)
    
    # Obtener géneros ordenados
    genres = [g for g in sorted(BASE_DIR.iterdir()) if g.is_dir()]
    
    # Estructura básica HTML
    html = [
        "<!DOCTYPE html>",
        "<html lang='es'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "  <title>Joy & Song</title>",
        f"  <style>{get_css()}</style>",
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
        "      </a>"
    ]
    
    # Añadir botones de navegación
    html.append(create_navigation_buttons(genres))
    
    # Cerrar la navegación y abrir el contenido principal
    html.extend([
        "    </nav>",
        "    <main id='content'>",
        "      <div class='banner'>CANCIONES 100% TU VIDA Y TU MUSICA FAVORITA</div>"
    ])
    
    # Añadir secciones de géneros
    for genre in genres:
        genre_name = genre.name
        section_id = quote(genre_name)
        html.append(create_genre_section(genre, section_id))
    
    # Añadir sección "Todos los Hits"
    html.append(create_all_hits_section(genres))
    
    # Cerrar contenido principal y añadir scripts
    html.extend([
        "    </main>",
        "  </div>",
        f"  <script>{get_javascript()}</script>",
        "</body>",
        "</html>"
    ])
    
    # Escribir archivo HTML
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    
    print("✅ HTML actualizado correctamente con botón de personalización para cada canción.")

# Ejecutar la generación HTML
if __name__ == "__main__":
    generate_html()
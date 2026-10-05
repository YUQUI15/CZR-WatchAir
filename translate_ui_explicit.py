import os
import re

directories = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\component"
]

TRANSLATIONS = {
    # Navigation & Core UI
    "Filters": "Filtros",
    "Signatures": "Firmas",
    "Reports": "Reportes",
    "Settings": "Ajustes",
    "Live": "En vivo",
    "FIELDWATCH": "CZR WatchAir",
    "Fieldwatch": "CZR WatchAir",
    "FIELDWATCH  ·  PAUSED": "CZR WatchAir  ·  PAUSADO",
    "FIELDWATCH  ·  SIT": "CZR WatchAir  ·  SESIÓN",
    "FIELDWATCH  ·  SIT  ·  PAUSED": "CZR WatchAir  ·  SESIÓN  ·  PAUSADO",
    
    # Reports Screen
    "Debrief, sits, log.": "Informes, sesiones, registro.",
    "Fieldwatch reports": "Reportes de CZR WatchAir",
    "Debrief": "Informe de campo",
    "Path": "Ruta",
    "Compare": "Comparar",
    "Sit": "Sesión",
    "Live list (last 15m)": "Lista en vivo (últimos 15m)",
    "Debrief PDF": "PDF de Informe",
    "Share debrief text": "Compartir texto",
    "AI Export (text)": "Exportar IA (texto)",
    "Compare sits": "Comparar sesiones",
    "Start sit": "Iniciar sesión",
    "End sit": "Terminar sesión",
    "Pause display": "Pausar vista",
    "Display paused · radios still scanning and logging. Filters still apply when you run again. Tap Live to run the list again.": "Vista pausada · escaneando y registrando. Los filtros aplican al reanudar. Toque En vivo para continuar.",
    "A sit is a named window of radios heard here. The selection below drives Path, Debrief, and Compare’s this-sit side: open sit, a selected saved sit, or last 15 minutes if you never start one.": "Una sesión es una ventana de tiempo. La selección controla Ruta, Informes y Comparaciones: sesión abierta, guardada o los últimos 15 min.",
    
    # Filters
    "Who is shown.": "Quién se muestra.",
    "Show only": "Mostrar solo",
    "Hide these": "Ocultar estos",
    "Watched only": "Solo vigilados",
    "Named radios only": "Solo radios nombradas",
    "Hide my radios": "Ocultar mis radios",
    "Hide observer notes": "Ocultar notas",
    "Hide custom name": "Ocultar nombre personalizado",
    "Clear all": "Limpiar todo",
    "Save current as…": "Guardar actual como…",
    "Name or OUI": "Nombre u OUI",
    
    # Signatures
    "All signatures": "Todas las firmas",
    "Update stock catalog from GitHub": "Actualizar catálogo desde GitHub",
    "Restore defaults": "Restaurar predeterminados",
    "Export signatures": "Exportar firmas",
    "Import signatures from a file": "Importar firmas",
    "Create signature": "Crear firma",
    "Edit signature": "Editar firma",
    
    # Device Detail
    "Device detail": "Detalle del dispositivo",
    "First seen": "Visto por primera vez",
    "Last seen": "Visto por última vez",
    "How loud here (RSSI)": "Intensidad local (RSSI)",
    "How often it advertises": "Frecuencia de anuncio",
    "Claimed transmit power": "Potencia de transmisión",
    "Center frequencies": "Frecuencias centrales",
    "Channel / frequency": "Canal / frecuencia",
    "Appearance code": "Código de apariencia",
    "Advertised name": "Nombre anunciado",
    "Custom name": "Nombre personalizado",
    "Share detail text": "Compartir detalles",
    
    # Common words
    "Cancel": "Cancelar",
    "Save": "Guardar",
    "Delete": "Eliminar",
    "Hide": "Ocultar",
    "Close": "Cerrar",
    "Ok": "Aceptar",
    "Yes": "Sí",
    "No": "No",
    "None": "Ninguno"
}

def escape_regex(s):
    # Just escape normal regex chars
    return re.escape(s)

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    for en, es in TRANSLATIONS.items():
        # Match only exact strings inside quotes
        pattern1 = re.compile(r'"' + escape_regex(en) + r'"')
        if pattern1.search(content):
            content = pattern1.sub('"' + es + '"', content)
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Translated: {filepath}")

if __name__ == "__main__":
    for d in directories:
        if not os.path.exists(d): continue
        for file in os.listdir(d):
            if file.endswith('.kt'):
                translate_file(os.path.join(d, file))
    print("Done translating UI files.")

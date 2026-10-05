import os
import re

UI_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui"
DOMAIN_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain"

REPLACEMENTS = {
    # Main Navigation & Tabs
    r'"Live"': r'"En vivo"',
    r'"Hunt"': r'"Rastrear"',
    r'"Reports"': r'"Reportes"',
    r'"Signatures"': r'"Firmas"',
    r'"Settings"': r'"Ajustes"',
    r'"Fleets"': r'"Flotas"',
    r'"Bookmarks"': r'"Marcadores"',
    
    # Common Actions
    r'"Export"': r'"Exportar"',
    r'"Share"': r'"Compartir"',
    r'"Cancel"': r'"Cancelar"',
    r'"Save"': r'"Guardar"',
    r'"Delete"': r'"Eliminar"',
    r'"Clear"': r'"Limpiar"',
    r'"Close"': r'"Cerrar"',
    r'"Back"': r'"Atrás"',
    r'"Start"': r'"Iniciar"',
    r'"Stop"': r'"Detener"',
    r'"Pause"': r'"Pausar"',
    r'"Resume"': r'"Reanudar"',
    r'"Scan"': r'"Escanear"',
    
    # Hunt & Tri
    r'"Reset this hunt"': r'"Reiniciar rastreo"',
    r'"Back to detail"': r'"Volver al detalle"',
    r'"Beep"': r'"Pitido"',
    r'"Vibrate"': r'"Vibrar"',
    r'"Loudest this hunt"': r'"Más fuerte en este rastreo"',
    r'"last heard"': r'"última vez visto"',
    r'"no live RSSI"': r'"sin RSSI en vivo"',
    r'"Mesh Trilateration"': r'"Trilateración Mesh"',
    r'"Mark Point"': r'"Marcar Punto"',
    r'"Calculate Target"': r'"Calcular Objetivo"',
    
    # Settings & Info
    r'"Device Detail"': r'"Detalle del Dispositivo"',
    r'"Scanning"': r'"Escaneando"',
    r'"Paused"': r'"Pausado"',
    r'"Light Mode"': r'"Modo Claro"',
    r'"Night Mode"': r'"Modo Nocturno"',
    r'"About"': r'"Acerca de"',
    
    # Device classes & general
    r'"Unknown"': r'"Desconocido"',
    r'"Phone"': r'"Teléfono"',
    r'"Wearable"': r'"Wearable"',
    r'"Audio"': r'"Audio"',
    r'"Computer"': r'"Computadora"',
    r'"Vehicle"': r'"Vehículo"',
    r'"Tracker"': r'"Rastreador"',
    
    # specific ui phrases
    r'"Pause display"': r'"Pausar pantalla"',
    r'"Clear screen"': r'"Limpiar pantalla"',
    r'"Toggle overlay"': r'"Alternar superposición"',
}

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Translated: {filepath}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.kt'):
                translate_file(os.path.join(root, file))

if __name__ == "__main__":
    process_directory(UI_DIR)
    process_directory(DOMAIN_DIR)
    print("Translation complete.")

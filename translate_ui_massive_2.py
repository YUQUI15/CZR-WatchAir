import os
import re

directories = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\component"
]

TRANSLATIONS = {
    "Radar": "Radar",
    "List": "Lista",
    "Timeline": "Línea de tiempo",
    "Hybrid": "Híbrido",
    "By class": "Por clase",
    "Pause": "Pausar",
    "Paused": "Pausado",
    "Resume": "Reanudar",
    "Display": "Vista",
    "Reset view": "Restaurar vista",
    "Zoom": "Zoom",
    "Scan": "Escanear",
    "Scanning": "Escaneando",
    "Stop scan": "Detener escaneo",
    "Close": "Cerrar",
    "Back": "Atrás",
    "Sort by": "Ordenar por",
    "Strongest": "Más fuerte",
    "Newest": "Más nuevo",
    "Name": "Nombre",
    "Distance": "Distancia",
    "Class": "Clase",
    "Unknown": "Desconocido",
    "Devices": "Dispositivos",
    "Radios": "Radios",
    "Bluetooth": "Bluetooth",
    "Wi-Fi": "Wi-Fi",
    "Export": "Exportar",
    "Import": "Importar",
    "Refresh": "Actualizar",
    "Edit": "Editar",
    "Clear": "Limpiar",
    "Yes": "Sí",
    "No": "No",
    "Ok": "Aceptar",
    "Cancel": "Cancelar",
    "None": "Ninguno",
    "Error": "Error",
    "Success": "Éxito",
    "Saved": "Guardado",
    "Deleted": "Eliminado",
    "Loading...": "Cargando...",
    "Please wait": "Por favor espere",
    "Are you sure?": "¿Está seguro?",
    "Confirm": "Confirmar",
    "Warning": "Advertencia",
    "Info": "Información",
    "Status": "Estado"
}

def escape_regex(s):
    return re.escape(s)

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    for en, es in TRANSLATIONS.items():
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
    print("Done applying massive UI translations part 2.")

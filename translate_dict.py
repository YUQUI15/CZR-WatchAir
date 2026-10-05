import os
import re

UI_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair"

TRANSLATIONS = {
    "Remove": "Eliminar",
    "AI Export": "Exportar IA",
    "Continue": "Continuar",
    "Name A–Z": "Nombre A–Z",
    "Saved": "Guardado",
    "Hide these": "Ocultar estos",
    "Rename sit": "Renombrar sesión",
    "Start sit": "Iniciar sesión",
    "Not now": "Ahora no",
    "Grant permissions": "Otorgar permisos",
    "Log saved": "Registro guardado",
    "The file was written to the folder you picked. In the system picker, use the menu to choose the SD card if you want it off internal storage.": "El archivo se guardó en la carpeta seleccionada. En el selector del sistema, usa el menú para elegir la tarjeta SD si deseas sacarlo del almacenamiento interno.",
    "Log cleared": "Registro limpiado",
    "Rotated files were deleted. New detections will start a fresh log.": "Los archivos rotados fueron eliminados. Las nuevas detecciones iniciarán un registro nuevo.",
    "Detail": "Detalle",
    "Strongest signal": "Señal más fuerte",
    "Strongest (avg 30s)": "Más fuerte (promedio 30s)",
    "Newest heard": "Visto más reciente",
    "Newest alert": "Alerta más reciente",
    "Newest arrival": "Llegada más reciente",
    "New at bottom": "Nuevos al final",
    "Signatures first": "Firmas primero",
    "Off — Stale after only": "Desactivado — Caduco después de solo",
    "Hold ${sec}s after last packet": "Mantener ${sec}s después del último paquete",
    "Mark seen": "Marcar como visto",
    "Reset seen": "Restablecer visto",
    "Start over": "Empezar de nuevo",
    "More display options below": "Más opciones de visualización abajo",
    "Got it": "Entendido",
    "Create signature": "Crear firma",
    "Manufacturer": "Fabricante",
    "Service data": "Datos de servicio",
    "Add field": "Agregar campo",
    "Remove decode map": "Eliminar mapa de decodificación",
    "Remove decode map?": "¿Eliminar mapa de decodificación?",
    "Clears all fields on this signature. Live no longer shows the code mark. Raw advertisements stay. This cannot be undone except by adding fields again.": "Borra todos los campos en esta firma. La vista en vivo ya no mostrará la marca de código. Los anuncios en crudo permanecerán. Esto no se puede deshacer excepto agregando campos nuevamente.",
    "More": "Más",
    "Hide extra": "Ocultar extra",
    "Only if…": "Solo si…",
    "Named values…": "Valores con nombre…",
    "Strong": "Fuerte",
    "Add value": "Agregar valor",
    "equals": "es igual a",
    "not equals": "no es igual a",
    "mask": "máscara",
    "none of bits": "ninguno de los bits",
    "payload length": "longitud del payload",
    "little": "pequeño (little endian)",
    "big": "grande (big endian)",
    "Save name": "Guardar nombre",
    "Create signature from device": "Crear firma desde dispositivo",
    "Share as text": "Compartir como texto",
    "Save notes": "Guardar notas",
    "Both": "Ambos",
    "Wi-Fi only": "Solo Wi-Fi",
    "BLE only": "Solo BLE",
    "Show only": "Mostrar solo",
    "Reset filter": "Restablecer filtro",
    "Reset filter?": "¿Restablecer filtro?",
    "Reset": "Restablecer",
    "Delete preset?": "¿Eliminar preset?",
    "Class A–Z": "Clase A–Z",
    "Add rule": "Agregar regla",
    "Delete signature": "Eliminar firma",
    "Delete this signature?": "¿Eliminar esta firma?",
    "Selected color": "Color seleccionado",
    "Show all": "Mostrar todo",
    "Collapse empty": "Colapsar vacíos",
    "Observer notes": "Notas del observador",
    "Alerted this session": "Alertado en esta sesión",
    "Clear all ${radios.size} named radios": "Limpiar todas las ${radios.size} radios nombradas",
    "Clear named radios?": "¿Limpiar radios nombradas?",
    "Remove ${radios.size} named radios. Signature watches stay.": "Elimina ${radios.size} radios nombradas. Las vigilancias de firma permanecen.",
    "Named radio": "Radio nombrada",
    "End sit": "Terminar sesión",
    "Rename": "Renombrar",
    "Delete all sits": "Eliminar todas las sesiones",
    "Debrief (text)": "Informe (texto)",
    "Debrief (PDF)": "Informe (PDF)",
    "Compare (text)": "Comparar (texto)",
    "Compare (PDF)": "Comparar (PDF)",
    "Signature candidates": "Candidatos a firma",
    "Reset / clear log": "Restablecer / limpiar registro",
    "Clear the log?": "¿Limpiar el registro?",
    "This deletes all rotated CSV/JSON files on the phone. It cannot be undone. Live scanning will start a new empty log.": "Esto elimina todos los archivos CSV/JSON rotados en el teléfono. No se puede deshacer. El escaneo en vivo iniciará un nuevo registro vacío.",
    "Clear log": "Limpiar registro",
    "Delete this sit?": "¿Eliminar esta sesión?",
    "Removes the saved sit from this phone. The log is unchanged.": "Elimina la sesión guardada de este teléfono. El registro no se modifica.",
    "Delete all sits?": "¿Eliminar todas las sesiones?",
    "Removes saved sits from this phone. An open sit is not deleted. The log is unchanged.": "Elimina las sesiones guardadas de este teléfono. Una sesión abierta no se elimina. El registro no se modifica.",
    "Delete all": "Eliminar todo",
    "Save to SD card / storage…": "Guardar en tarjeta SD / almacenamiento…",
    "Scan intensity  ·  $label": "Intensidad de escaneo  ·  $label",
    "Developer options required": "Se requieren opciones de desarrollador",
    "Open developer options": "Abrir opciones de desarrollador",
    "Open Android settings": "Abrir ajustes de Android",
    "Named radios ($radioWatchN)": "Radios nombradas ($radioWatchN)",
    "Test alert": "Alerta de prueba",
    "Rotate at $rotateDrag KB": "Rotar a los $rotateDrag KB",
    "Stale after ${staleDrag}s": "Caduco después de ${staleDrag}s",
    "Export signatures": "Exportar firmas",
    "Save signatures to SD card / storage…": "Guardar firmas en tarjeta SD / almacenamiento…",
    "Import signatures…": "Importar firmas…",
    "Update stock catalog from GitHub": "Actualizar catálogo de fábrica desde GitHub",
    "Restore default signatures & presets": "Restaurar firmas y presets predeterminados",
    "Export settings": "Exportar ajustes",
    "Save settings to SD card / storage…": "Guardar ajustes en tarjeta SD / almacenamiento…",
    "Import settings…": "Importar ajustes…",
    "Show Live tour": "Mostrar tour En vivo",
    "Restore defaults?": "¿Restaurar predeterminados?",
    "Restore": "Restaurar",
    "This phone": "Este teléfono",
    "LAN multicast": "LAN multicast",
    "Custom": "Personalizado",
    "Extra attention": "Atención adicional",
    "Payload location": "Ubicación del payload",
    "Watchlist": "Lista de vigilancia",
    "All signatures": "Todas las firmas",
    "Light Mode (Pastel Palette)": "Modo Claro (Paleta Pastel)",
    "Night Mode": "Modo Nocturno",
    "Light Mode": "Modo Claro"
}

def escape_regex(s):
    # Escape special characters for regex, but keep interpolation variables intact
    return re.escape(s).replace(r'\$\{sec\}', r'\$\{sec\}').replace(r'\$\{radios\.size\}', r'\$\{radios\.size\}').replace(r'\$label', r'\$label').replace(r'\$rotateDrag', r'\$rotateDrag').replace(r'\$\{staleDrag\}', r'\$\{staleDrag\}').replace(r'\$radioWatchN', r'\$radioWatchN')


def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace these EXACT strings inside quotes.
    # So we search for "String" and replace with "SpanishString"
    modified = False
    
    for en, es in TRANSLATIONS.items():
        # Handle cases where it is inside Text("...") or contentDescription = "..."
        # But honestly, replacing the exact string literal in the file is safe because they are very specific sentences
        
        pattern1 = re.compile(r'"' + escape_regex(en) + r'"')
        if pattern1.search(content):
            content = pattern1.sub('"' + es + '"', content)
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Translated: {filepath}")

if __name__ == "__main__":
    for root, _, files in os.walk(UI_DIR):
        for file in files:
            if file.endswith('.kt'):
                filepath = os.path.join(root, file)
                translate_file(filepath)
    print("Done translating dictionary.")

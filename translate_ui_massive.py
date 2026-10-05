import os
import re
import json

directories = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\component"
]

TRANSLATIONS = {
    "Could not build AI export": "No se pudo crear exportación IA",
    "Could not clear log": "No se pudo limpiar el registro",
    "Could not export": "No se pudo exportar",
    "Could not export settings": "No se pudo exportar ajustes",
    "Could not export signatures": "No se pudo exportar firmas",
    "Could not import catalog": "No se pudo importar catálogo",
    "Could not import catalog.": "No se pudo importar catálogo.",
    "Could not import settings": "No se pudo importar ajustes",
    "Could not import signatures": "No se pudo importar firmas",
    "Could not open the selected location": "No se pudo abrir la ubicación",
    "Could not reach GitHub": "No se pudo contactar a GitHub",
    "Could not reach the catalog on GitHub. Try again later, or use Import signatures from a file.": "No se pudo contactar el catálogo en GitHub. Intente luego o importe desde archivo.",
    "Could not read that file.": "No se pudo leer ese archivo.",
    "Could not read that sit.": "No se pudo leer esa sesión.",
    "Could not read the log": "No se pudo leer el registro",
    "Could not read this sit.": "No se pudo leer esta sesión.",
    "Could not save settings": "No se pudo guardar ajustes",
    "Could not save signatures": "No se pudo guardar firmas",
    "Could not share device detail": "No se pudo compartir detalles del dispositivo",
    "Could not write compare AI export": "No se pudo guardar exportación de comparación",
    "Could not write debrief": "No se pudo crear informe",
    "Could not write debrief PDF": "No se pudo crear PDF",
    "Could not write sit compare": "No se pudo crear comparación",
    "Could not write sit compare PDF": "No se pudo crear PDF de comparación",
    "Could not write to the location you picked.": "No se pudo escribir en la ubicación elegida.",
    "Custom name": "Nombre personalizado",
    "Data prefix hex": "Prefijo de datos (hex)",
    "Debrief PDF": "PDF de informe",
    "Debrief and AI Export use this window until you end it. The Live list is unchanged.": "El Informe y Exportación IA usan esta ventana hasta terminarla. La lista En vivo no cambia.",
    "Decode fields": "Decodificar campos",
    "Decoded fields": "Campos decodificados",
    "Delete field": "Eliminar campo",
    "Delete rule": "Eliminar regla",
    "Delete value": "Eliminar valor",
    "Disclaimer and license": "Descargo y licencia",
    "Display — Radar, list, timeline, hybrid, By class.": "Vista — Radar, lista, línea de tiempo, híbrido, Por clase.",
    "Each rule has its own switch. Off keeps the rule but it does not match. ": "Cada regla tiene su interruptor. Apagado guarda la regla pero no coincide.",
    "Empty list = no extra include (Live unchanged). Picks stay if you turn this off and on again.": "Lista vacía = sin inclusión extra. Las elecciones se guardan si lo apaga y prende.",
    "Encryption / login": "Cifrado / acceso",
    "End sit to pick a saved one for Path and Debrief.": "Termine la sesión para elegir una guardada para Ruta e Informes.",
    "Export Fieldwatch logs": "Exportar registros",
    "Export failed": "Falló exportación",
    "Extra filter logic": "Filtros adicionales",
    "Fieldwatch AI export — $title": "Exportación IA CZR WatchAir — $title",
    "Fieldwatch AI export — last 15 minutes": "Exportación IA — últimos 15 min",
    "Fieldwatch GPX": "CZR WatchAir GPX",
    "Fieldwatch KML": "CZR WatchAir KML",
    "Fieldwatch WiGLE CSV": "CZR WatchAir WiGLE CSV",
    "Fieldwatch device detail — $title": "Detalle de dispositivo CZR WatchAir — $title",
    "Fieldwatch field debrief — last 15 minutes": "Informe de campo — últimos 15 min",
    "Fieldwatch log (CSV)": "Registro (CSV)",
    "Fieldwatch log (JSON lines)": "Registro (JSON lines)",
    "Fieldwatch needs the radios": "CZR WatchAir requiere radios",
    "Fieldwatch settings": "Ajustes de CZR WatchAir",
    "Fieldwatch signatures": "Firmas de CZR WatchAir",
    "Fieldwatch sit compare": "Comparación de sesión",
    "Filters → Show only / Hide these. Class sits (Finder tags, Cameras, …) are those chips — Save current as… if you want a preset.": "Filtros → Mostrar/Ocultar estos. Las clases (Cámaras, etc) son esos chips — Guardar actual como... si quiere un preset.",
    "Fine filter": "Filtro fino",
    "First / last seen": "Visto primera/última vez",
    "Flags (raw)": "Banderas (raw)",
    "Freeze the picture. Tap Live again to run.": "Congele la pantalla. Toque En vivo para continuar.",
    "Gathering sit…": "Recopilando sesión...",
    "Heard range this session": "Rango escuchado esta sesión",
    "Hidden SSID": "SSID Oculto",
    "Hidden — the AP is beaconing but not publishing a name": "Oculto — el AP emite pero no publica nombre",
    "Hide Fast Pair account-key": "Ocultar llaves Fast Pair",
    "Hide custom name": "Ocultar nombre personalizado",
    "Hide my radios": "Ocultar mis radios",
    "Hide observer notes": "Ocultar notas de observador",
    "Hide radios already here so only new ones show on Live. ": "Oculta radios que ya estaban aquí para mostrar solo nuevas.",
    "Hide scan options": "Ocultar opciones de escaneo",
    "Hide selected signatures": "Ocultar firmas seleccionadas",
    "Hide these still applies (Watched only + Hide Surveillance drops bookmarked cameras). ": "Ocultar estos todavía aplica (Solo vigilados + Ocultar Vigilancia descarta cámaras guardadas).",
    "Hide this burst": "Ocultar esta ráfaga",
    "Hiding 1 flood radio": "Ocultando 1 radio spam",
    "Hiding sitting access points until the next Wi-Fi scan. New Bluetooth still shows right away.": "Ocultando APs estáticos hasta el próximo escaneo Wi-Fi.",
    "Import": "Importar",
    "In motion (walk/vehicle) through mixed RF.": "En movimiento por RF mixta.",
    "Include": "Incluir",
    "Include class": "Incluir clase",
    "Live": "En vivo",
    "Live list": "Lista en vivo",
    "Live list is hiding older beacons so new arrivals pop up. ": "La lista En vivo oculta balizas antiguas para que destaquen las nuevas.",
    "Log": "Registro",
    "Log format": "Formato de registro",
    "Log starts when you run Fieldwatch. You can clear it to drop the past. Sit export writes the same window as Debrief and Path.": "El registro inicia al abrir la app. Puede limpiarlo para descartar el pasado. Exportar sesión guarda lo mismo que el Informe.",
    "Logic rule": "Regla lógica",
    "Match bytes": "Bytes coincidentes",
    "Missing catalog fields: ": "Faltan campos de catálogo: ",
    "Must be 1 to 3 bytes (2 to 6 hex chars). Example: 180A": "Debe ser de 1 a 3 bytes (2 a 6 hex).",
    "Must be 1 to 32 bytes (2 to 64 hex chars).": "Debe ser de 1 a 32 bytes.",
    "No Bluetooth scans — you turned it off.": "Sin escaneos Bluetooth — apagado.",
    "No Bluetooth, no Wi-Fi.": "Sin Bluetooth, sin Wi-Fi.",
    "No Wi-Fi scans — you turned it off.": "Sin escaneos Wi-Fi — apagado.",
    "None.": "Ninguno.",
    "OUI / company": "OUI / compañía",
    "Raw bytes": "Bytes crudos",
    "Recent (15m)": "Reciente (15m)",
    "Remote ID / UAS": "Remote ID / UAS",
    "Reset": "Restablecer",
    "Reset / clear log": "Limpiar registro",
    "Reset UI settings": "Restablecer interfaz",
    "Reset this hunt": "Reiniciar este rastreo",
    "Restore default settings": "Restaurar ajustes",
    "Save": "Guardar",
    "Save current as…": "Guardar actual como…",
    "Select": "Seleccionar",
    "Settings": "Ajustes",
    "Share": "Compartir",
    "Share debrief text": "Compartir texto del informe",
    "Share device detail": "Compartir detalles",
    "Share sit compare text": "Compartir texto de comparación",
    "Show": "Mostrar",
    "Show all": "Mostrar todo",
    "Show only": "Mostrar solo",
    "Show scan options": "Mostrar opciones de escaneo",
    "Show selected signatures": "Mostrar firmas seleccionadas",
    "Signature": "Firma",
    "Signatures": "Firmas",
    "Signatures only": "Solo firmas",
    "Since log start": "Desde inicio de registro",
    "Sit": "Sesión",
    "Sit $sit": "Sesión $sit",
    "Sit 1 is the older / baseline sit; sit 2 is the newer / contrast sit.": "Sesión 1 es la sesión base; sesión 2 es la más nueva.",
    "Sit export": "Exportar sesión",
    "Start": "Iniciar",
    "Start sit": "Iniciar sesión",
    "Station-side Wi-Fi (probes/clients) still needs a dedicated sniffer — Fieldwatch cannot see them.": "El Wi-Fi (sondas/clientes) necesita un sniffer dedicado — la app no puede verlos.",
    "Stop": "Detener",
    "Text size": "Tamaño de texto",
    "Theme": "Tema",
    "Turn off Wi-Fi and Bluetooth to drop everything to 0.": "Apague Wi-Fi y Bluetooth para dejar todo en 0.",
    "Unmatched rotating BLE omitted from lists ($omittedRand). Counts include them. Sit export has every radio.": "BLE rotativo sin coincidencia omitido ($omittedRand). Los totales los incluyen. La exportación tiene todas.",
    "Update stock catalog": "Actualizar catálogo",
    "Update stock catalog from GitHub": "Actualizar desde GitHub",
    "Update…": "Actualizar…",
    "Use Live → Pause to inspect a busy list. Watch tracker signatures if this sit was noisy.": "Use En vivo → Pausa para inspeccionar listas muy llenas.",
    "Vendor / OUI prefix": "Prefijo OUI / Vendedor",
    "Waiting for file…": "Esperando archivo…",
    "Waiting for sit…": "Esperando sesión…",
    "Walk farther (50+ m) with GPS tagging on, then re-run Debrief.": "Camine más de 50m con GPS, luego re-ejecute el Informe.",
    "Watch": "Vigilar",
    "Watched only": "Solo vigilados",
    "Yes": "Sí",
    "You have no saved sits yet.": "No tiene sesiones guardadas.",
    "iOS devices cycle through a predictable MAC sequence when tracking. Name one, and Fieldwatch watches the sequence.": "Los iOS ciclan a través de una secuencia MAC predecible al rastrear. Nombre una, y la app vigilará la secuencia."
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
    print("Done applying massive UI translations.")

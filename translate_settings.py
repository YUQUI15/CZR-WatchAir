import os
import re

files_to_check = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen\SettingsScreen.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\FieldwatchAppUi.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\LiveChromeTour.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen\FiltersScreen.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen\DeviceDetailScreen.kt"
]

TRANSLATIONS = {
    # App UI & Top Bar
    "FIELDWATCH": "CZR WatchAir",
    "Filters": "Filtros",
    "Who is shown.": "Quién se muestra.",
    
    # Settings Headers & Common
    "Night mode": "Modo nocturno",
    "Keep screen on": "Mantener pantalla encendida",
    "Privacy mode": "Modo privacidad",
    "Faster Wi-Fi AP scans": "Escaneos Wi-Fi más rápidos",
    "High performance": "Alto rendimiento",
    "Wi-Fi scanning": "Escaneo Wi-Fi",
    "Write detections to disk": "Guardar detecciones en disco",
    "System notification": "Notificación del sistema",
    "Watchlist alerts": "Alertas de vigilancia",
    "Beep on watched signature": "Pitido en firmas vigiladas",
    "Voice on watched signature": "Voz en firmas vigiladas",
    "What to say": "Qué decir",
    "Jump to new watched detection": "Saltar a nueva detección",
    "Tag detections with GPS": "Etiquetar con GPS",
    "Online place names and maps": "Nombres y mapas en línea",
    "Settings backup": "Respaldo de ajustes",
    "Unrestricted battery": "Batería sin restricciones",
    "Battery saver": "Ahorro de batería",
    "Allow background usage": "Uso en segundo plano",
    "TAK / CoT feed": "Salida TAK / CoT",
    "TAK / CoT": "TAK / CoT",
    "What to send": "Qué enviar",

    # Long Descriptions in Settings
    "Off by default. Red-on-black field display so chips, text, and signal marks ": "Apagado por defecto. Pantalla en rojo sobre negro para que marcas y textos ",
    "do not dump green or blue into a dark sit. Background stays dark. ": "no arrojen brillo verde o azul en la oscuridad. El fondo se mantiene oscuro. ",
    "Phone brightness is unchanged.": "El brillo del teléfono no cambia.",
    
    "On by default. Stops the display from sleeping while Fieldwatch is open so BLE is not parked when the phone blanks. Scanning still runs in the notification if you leave the app. Turn it off when you pocket the phone.": "Encendido por defecto. Evita que la pantalla se apague mientras CZR WatchAir está abierto para no detener BLE. El escaneo sigue en segundo plano. Apáguelo al guardarlo en el bolsillo.",
    
    "Hides the last three octets of every MAC on Live, radar, timeline, detail, Hunt, Named radios, and watchlist cards as **:**:** so the screen and sit reports do not show full addresses. GPS last-fix and Debrief / AI Export / detail Share coordinates become “masked”; street names are omitted from those sit reports. The first three octets (OUI / vendor prefix) stay. Off by default. The map on Reports → Path still loads when Online place names and maps is on. Logs, matching, filters, Hunt math, Moving with you, and saved signatures still use the real MAC and GPS. A TAK / CoT feed, if you turned it on, is paused while this is on so full MACs and coordinates are not sent onto the LAN. Turn this off when you need the full address or coordinates on screen.": "Oculta los últimos tres octetos de cada MAC en reportes y listas como **:**:**. Las coordenadas exportadas en informes se 'enmascaran'. Los registros, la búsqueda y la trilateración siguen usando la MAC real internamente. Apagado por defecto.",
    
    "Wi-Fi is a batch radio: the phone grabs every AP at once, then must wait. High performance asks about every 30s — that is the fastest cadence that stays under the OS limit of four scans per two minutes. BLE still streams in between.": "Wi-Fi se escanea por lotes: Alto rendimiento pide escaneos cada ~30s (el límite de Android es 4 cada 2 minutos). BLE fluye entre medio.",
    
    "Stock Android allows about four AP scans per two minutes. Faster scans only run after you turn off Wi-Fi scan throttling in Developer options. Fieldwatch checks that OS switch before turning this on, and cannot change it for you.": "Android de fábrica permite ~4 escaneos Wi-Fi en 2 min. Esto solo funciona tras apagar 'Limitación de escaneo Wi-Fi' en Opciones de Desarrollador. La app solo verifica ese estado, no puede cambiarlo por usted.",
    
    "On by default. Requests live GPS/network updates and stamps each hear (Live detail, Moving with you, ": "Encendido por defecto. Pide GPS en vivo y sella cada detección (Detalles, Rastreo, ",
    "Debrief, and lat/lon on new log rows). Last-known-only is ignored if older than 30 s. ": "Informes y archivos). Se ignora el último conocido si tiene más de 30s.",
    "Use high-accuracy Location or the path stays 0. Turn off if you do not want operator coordinates on logs. ": "Use Ubicación de alta precisión. Apague si no desea registrar coordenadas del operador.",
    
    "On by default. Master switch for bookmarked signatures and devices. Off: no beep, vibration, flash, jump, or shade card. Bookmarking still works — you just will not be told when that radio appears.": "Encendido por defecto. Interruptor maestro para alertas. Apagado: no hay pitido ni flash. Los marcadores seguirán funcionando pero sin notificaciones.",
    
    "The double pip on media volume when a bookmarked signature or device first appears, or returns after leaving. Sitting detections do not beep again. Independent of Voice — use beep, voice, or both. Raise media volume if you hear nothing, then tap Test alert.": "Doble pitido en el volumen multimedia cuando aparece una radio vigilada. Detecciones quietas no vuelven a sonar. Independiente de la voz. Suba el volumen si no escucha.",
    
    "On by default. Speaks on the same media volume as the pip. Independent of Beep: with Beep on, voice follows the pip; with Beep off, voice only. Not Hunt. If a phrase is already being spoken, a second hit is skipped. Phones with no text-to-speech still beep if Beep is on.": "Encendido por defecto. Habla en el volumen multimedia. Independiente del pitido. Si ya se está hablando, la segunda voz se salta.",
    
    "When a new watched signature or device appears, Live scrolls to that row so you can see the flash. Works with beep, voice, or both. Weak hits sit at the bottom of a strength-ranked list. Turn this off if you do not want the list to move.": "Cuando aparece una nueva alerta, la vista En vivo se desplaza a ella para que la vea. Funciona con pitido/voz. Apague si no desea que la lista salte sola.",
    
    "Optional. Posts a silent shade card when a watched radio appears. Off by default — the beep and flash are enough, and skipping the card keeps the scan loop lighter.": "Opcional. Muestra una notificación silenciosa cuando aparece una radio vigilada. Apagado por defecto.",
    
    "On by default. When the phone has internet, Debrief / AI Export reverse-geocode GPS stamps ": "Encendido por defecto. Con internet, Informe / Exportar IA usa nombres de lugares reales ",
    "to street/city, and Reports → Path loads OpenStreetMap tiles under the trace. ": "y muestra mapas en la ruta. ",
    "Turn off to keep streets and map tiles out of reports and Path. ": "Apáguelo para mantener las calles fuera de los reportes.",
    
    "Settings switches, the current filter, filter presets, named radios, and signature watches. ": "Ajustes, filtros, nombres personalizados y firmas vigiladas. ",
    "Not the catalog — that is Export signatures. Not logs or GPS. ": "No el catálogo, eso es Exportar firmas. Tampoco los registros de GPS.",
    "Export the catalog (stock plus any you added or edited) to share with another Fieldwatch or as a backup. Import adds new rows and extra rules; it does not delete anything. Same id or the same match rules are skipped so a pack can be imported twice. Update stock catalog from GitHub replaces stock rows (including Extra attention) from the v2 pack on the repo; bookmarks, Settings, and signatures you added stay. Needs internet. Offline: Import signatures from a file. Restore defaults below still wipes customs.": "Exporta el catálogo para respaldar. Importar añade pero no borra. Actualizar catálogo reemplaza las filas de fábrica desde GitHub (requiere internet).",
    
    "Rewrites the catalog (stock rows, class colors, Decode fields), stock bookmarks, ": "Reescribe el catálogo, marcadores de fábrica, ",
    "stock filter chips, and default Settings switches. Custom signatures and chips you ": "filtros, y opciones por defecto. Firmas y filtros personalizados ",
    "saved are wiped. Export signatures and Export settings first if you want a backup. ": "se borrarán. Exporte primero si desea un respaldo. ",
    "This cannot be undone.": "Esta acción es irreversible.",
    
    "Mirrors Android Unrestricted (not Optimized). Some phones (Samsung among them) do not ": "Refleja el ajuste Sin restricciones de Android. Algunos teléfonos no ",
    "open onto that choice. If you only see Allow background usage, tap that row to ": "abren esa opción directo. Si ve 'Permitir en segundo plano', toque ",
    "click through and select Unrestricted. Fieldwatch updates when you return.": "y seleccione Sin restricciones. La app se actualiza al regresar.",
    
    "Mirrors Android Allow background usage. Tap to open Fieldwatch’s Battery page and ": "Refleja Permitir uso en segundo plano de Android. ",
    "use that switch. Fieldwatch updates when you return. Off: the OS can kill the scan ": "Use el interruptor. Apagado: el SO puede matar la app ",
    "as soon as you leave. Not Keep screen on.": "tan pronto salga de ella.",
    
    "Some phones (Samsung among them) do not open onto Unrestricted / ": "Algunos teléfonos no abren directo en Sin Restricciones. ",
    "tap that row (the words, not the blue switch) to click through, ": "Toque la fila (las palabras, no el interruptor) ",
    "then select Unrestricted. Fieldwatch will match that when you return.": "y luego seleccione Sin restricciones.",
    
    "The next screen is Fieldwatch’s Battery page. Use the Allow background usage switch. ": "La siguiente es la página de Batería. Active el interruptor de segundo plano. ",
    "Fieldwatch will match that setting when you return.": "La app se actualizará cuando regrese.",
    
    "Logging is on. New detections are appended to the rotating file.": "El registro está encendido. Las nuevas detecciones se guardan en el archivo rotativo.",
    "Logging is off. Scanning still runs; nothing new is written until you turn this back on.": "El registro está apagado. El escaneo sigue, pero no se guarda nada hasta encenderlo.",
    "The rotating file is JSON lines (one hear per line). Reports → Log → Format writes CSV, JSON lines, GPX, KML, or WiGLE when you Share or Save.": "El archivo es JSON lines. Reportes → Formato exportará CSV o GPX al Guardar o Compartir.",
    "Debrief, Sit export, Log export, and Reset / clear log are on the Reports tab.": "Exportaciones, Informes y Limpiar registro están en la pestaña Reportes.",
    "Share, Save, and Reset / clear log are on the Reports tab.": "Compartir, Guardar y Limpiar registro están en Reportes.",
    
    "Off by default. Sends Cursor-on-Target UDP markers to ATAK, WinTAK, or iTAK. ": "Apagado por defecto. Envía CoT UDP a ATAK, WinTAK, o iTAK.",
    "Passive Wi-Fi + BLE only. ": "Solo Wi-Fi Pasivo + BLE.",
    "Custom is a unicast IPv4 or hostname. UDP only — a TAK server’s TCP 8087 is not this feed. ": "Personalizado es un IPv4 o dominio (solo UDP).",
    "Custom: type a unicast IPv4 or hostname. UDP only. A TAK server’s TCP 8087 is not this feed. ": "Personalizado es un IPv4 o dominio (solo UDP).",
    
    "All signatures (off): every labeled radio — noisy in a plaza. Unmatched radios never go. ": "Todas las firmas (apagado): ruidoso en multitudes.",
    "Watchlist (off): bookmarked signatures and named radios with Alert on. ": "Lista de vigilancia (apagado): firmas marcadas y radios nombradas.",
    "Payload location (on): advertised lat/lon from a decode map — required for stock Remote ID, which has no Extra attention mark. ": "Ubicación del Payload (encendido): lat/lon de mapa de decodificación.",
    "Independent chips. Extra attention (on): body-cam, glasses, recording wearables, pentest, public-safety APs. ": "Chips independientes. Atención adicional (encendido): cámaras corporales, wearables de grabación, seguridad.",
    
    "Heard-here pins sit at this phone’s GPS at the loudest hear (closest approach) and are labeled (here). ": "Puntos de Escuchado-Aquí se sitúan en el GPS del teléfono con el registro más fuerte y la etiqueta (here).",
    "Heard-here holds the loudest hear, not the last, and callsigns end in (here). ": "Guarda la escucha más fuerte, no la última, con etiqueta (here).",
    "Walking away does not drag the pin; a louder hear moves it. Keep-alives refresh the same lat/lon every ~10 s so ATAK does not drop it. ": "Alejarse no arrastra el marcador; una escucha más fuerte lo mueve.",
    "That is your GPS at hear-time, not an independent fix on the other radio. ": "Ese es su GPS en ese momento, no de la otra radio.",
    "A pin still needs coordinates: advertised payload, or GPS tagging with a live fix. ": "Un marcador necesita coordenadas: payload anunciado o etiqueta GPS.",
    "Heard-here TAK pins also need this; advertised payload coordinates (Remote ID) do not.": "Los marcadores TAK necesitan esto; las coordenadas anunciadas (Remote ID) no.",
    "Advertised lat/lon (stock Remote ID) sit on the aircraft; the same Remote ID ": "Lat/lon anunciada (Remote ID de fábrica) se ubican en la aeronave.",
    "keeps one marker that moves (UAS ID, not the rotating BLE MAC). ": "mantiene un marcador que se mueve.",
    "Remote ID keeps one aircraft marker (UAS ID) plus a pilot pin when that location decoded.": "Remote ID mantiene el marcador del dron y el del piloto cuando decodifica.",
    "A decoded pilot location is a second pin. Gone radios are dropped on ATAK instead of sitting 120 s. ": "Una ubicación decodificada del piloto es un segundo punto.",
    "Tap a marker in ATAK for remarks (name, MAC, RSSI, signatures). ": "Toque un marcador en ATAK para más observaciones (nombre, RSSI).",
    
    "Custom names for one MAC. Alert is optional. Filters → Named radios only shows them on Live. Signature watches stay on Signatures.": "Nombres personalizados para una MAC. La alerta es opcional. Filtros → Radios nombradas las muestra.",
    
    "Stock Android cannot promiscuously capture Wi-Fi stations; access points and BLE advertisers are what the radios expose.": "Android de fábrica no puede capturar estaciones Wi-Fi de forma promiscua; solo APs y BLE.",
    
    "This phone is older than Android 11, so Fieldwatch cannot read the OS Wi-Fi scan-throttle switch. Faster AP scanning stays off.": "Este teléfono es anterior a Android 11, por lo que CZR WatchAir no puede leer el estado de limitación Wi-Fi.",
    "Android is still throttling Wi-Fi scans (about four per two minutes). Fieldwatch will not turn Faster Wi-Fi AP scans on until that is off.\\n\\n": "Android aún está limitando escaneos Wi-Fi. La app no habilitará escaneos rápidos hasta apagar esto.\\n\\n",
    "Enable Developer options (tap Build number seven times in About phone), then Settings → Developer options → Wi-Fi scan throttling → Off. Come back and flip this switch again.": "Habilite Opciones de Desarrollador, y apague Limitación de Búsqueda Wi-Fi. Vuelva aquí después.",
    "Saved on, but not in effect — Android Wi-Fi scan throttling is still on. Turn that off in Developer options, then return here.": "Guardado pero sin efecto — la limitación Wi-Fi sigue encendida en Desarrollador.",
    "Needs Android 11+ so Fieldwatch can read whether the OS is still throttling scans. This phone cannot confirm that, so the switch stays off.": "Necesita Android 11+ para leer la limitación de escaneo Wi-Fi.",
    
    "Chrome overlay on Live: Tune is Display (Radar, list, By class), Pause, Filters, Signatures, Reports, Settings. First-run after the license; this button shows it again.": "Guía en pantalla en vivo: Configuración de vista, Filtros, Firmas, Reportes. Este botón lo muestra de nuevo.",
    "Copyright (c) 2026 Off Grid Pete LLC. All rights reserved.": "Copyright (c) 2026 Off Grid Pete LLC. Adaptado para CZR WatchAir.",
    
    "Feed status  ·  paused (Privacy mode)": "Estado de red · pausado (Modo Privacidad)",
    "Feed status  ·  no send yet this session": "Estado de red · no ha enviado esta sesión",
    "This phone’s IPv4  ·  none": "IPv4 del teléfono · ninguno",
    "Wi-Fi waiting on OS": "Wi-Fi esperando al SO",
    "Wi-Fi next 99s": "Wi-Fi próx 99s",
    "1 gone": "1 ido",
    
    "Use this after a factory reset or on a new phone.": "Utilice esto después de reiniciar de fábrica o en un teléfono nuevo.",
    "  ·  $whenAt": "  ·  $whenAt"
}

def escape_regex(s):
    return re.escape(s).replace(r'\$label', r'\$label').replace(r'\$radioWatchN', r'\$radioWatchN').replace(r'\$rotateDrag', r'\$rotateDrag').replace(r'\$whenAt', r'\$whenAt')

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
    for filepath in files_to_check:
        if os.path.exists(filepath):
            translate_file(filepath)
    print("Done translating settings explicitly.")

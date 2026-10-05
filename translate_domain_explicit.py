import os
import re

files_to_check = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DebriefReport.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DebriefPdf.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\SitExport.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DeviceExplain.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\SitDiff.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\Sit.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DeviceDetailText.kt"
]

TRANSLATIONS = {
    "Co-travel is split by class: finder tags (AirTag / Find My, SmartTag, Tile, Chipolo, Pebblebee, loud pocket Apple), retail beacons (iBeacon, Minew, Estimote, Kontakt.io, Atrius cart tag), and wearables (Garmin, Fitbit, Oura).": "El viaje conjunto se divide por clase: etiquetas de búsqueda (AirTag / Find My, SmartTag, Tile, Chipolo, Pebblebee), balizas minoristas (iBeacon, Minew, Estimote, Kontakt.io, carrito Atrius), y wearables (Garmin, Fitbit, Oura).",
    "Phone GPS at hear-time, not the other radio’s location and not a camera pole. Stays are clusters within about 40 m; hops between them are transit. Coordinates are not repeated on every Wi-Fi/BLE line.": "GPS del teléfono al momento de escuchar, no la ubicación de la otra radio. Las paradas son grupos dentro de unos 40 m; los saltos entre ellos son tránsito. Las coordenadas no se repiten en cada línea.",
    "A MAC alert or a signature alert is drawn once. A decoded latitude and longitude is the last advertised position. Anything else is the strongest hear. A number is that place (Path key).": "Una alerta MAC o de firma se dibuja una vez. Una lat/lon decodificada es la última posición anunciada. Todo lo demás es la señal más fuerte escuchada. Un número es ese lugar.",
    "Retail beacons with you (iBeacon / Minew / Estimote / Kontakt.io / Atrius cart tag — fixtures; a pushed cart will co-travel)": "Balizas minoristas con usted (iBeacon/Minew/Estimote/Kontakt.io — accesorios fijos; un carrito empujado viajará con usted)",
    "Unusual for a retail/location beacon — they do not typically move with you. Account for it; not the same as a Find My tail.": "Inusual para una baliza minorista: no suelen moverse con usted. Considérenlo; no es lo mismo que un rastreo de Find My.",
    "If one did, account for it (a cart you pushed, your own test tag, a badge, or a short path that still overlaps a fixture).": "Si alguna lo hizo, considérelo (un carrito que empujó, su propia etiqueta, una credencial o una ruta corta).",
    "Location beacons do not typically move with you. Account for it (own test tag, badge, or a short overlap with a fixture).": "Las balizas de ubicación no suelen moverse con usted. Considérenlo (su propia etiqueta de prueba, credencial o un cruce corto).",
    "Insufficient movement to distinguish a radio that stayed with you from one you passed. Walk or drive farther and re-run.": "Movimiento insuficiente para distinguir una radio que se quedó con usted de una que pasó. Camine o conduzca más lejos y vuelva a ejecutar.",
    "No finder tag, retail beacon, or wearable stayed with you. House tags and other radios you only passed are not listed.": "Ninguna etiqueta de búsqueda, baliza minorista o wearable se quedó con usted. Las etiquetas de casa u otras radios que solo pasó no se enumeran.",
    "Callouts below are only radios that stayed with the path. Radios you passed (store fixtures, house tags) are omitted.": "Solo se destacan las radios que permanecieron en la ruta. Las radios que pasó (instalaciones, etiquetas de casa) se omiten.",
    "Typical of a watch that joined the sit (you put it on, or someone walking with you). Not typically a planted tracker.": "Típico de un reloj que se unió a la sesión (se lo puso, o alguien camina con usted). Normalmente no es un rastreador plantado.",
    "Could be yours or planted in the car/bag/on you before you started. Account for each MAC — do not dismiss as yours.": "Podría ser suyo o estar plantado en el coche/bolso/usted antes de empezar. Considere cada MAC — no lo descarte como suyo.",
    "Fieldwatch cannot tell your own tag or phone from a tracker planted in the car, bag, or on you before you started.": "La app no puede distinguir su propia etiqueta de un rastreador plantado en el automóvil, bolso o en usted antes de comenzar.",
    "GPS tagging is OFF. Turn on Settings → Tag detections with GPS to record where you were when radios were heard.": "El etiquetado GPS está APAGADO. Active Ajustes → Detecciones con GPS para registrar dónde estaba.",
    "GPS tagging is off, so a following test was not performed. Enable “Tag detections with GPS” and walk to test.": "El etiquetado GPS está apagado, no se realizó una prueba de seguimiento. Active 'Detecciones con GPS' y camine para probar.",
    "Watches and rings usually move with the person wearing them — often your own kit or someone walking with you.": "Los relojes y anillos generalmente se mueven con la persona — a menudo su propio equipo o alguien que camina con usted.",
    "Locally administered BSSID. Vehicle, mesh, and guest APs often keep this address. Not a rotating phone MAC.": "BSSID administrado localmente. Los vehículos, mallas y APs de invitados a menudo mantienen esta dirección. No es una MAC rotativa de teléfono.",
    "No extra flags. Signature hits, Extra attention, and tracking callouts already cover named pattern matches.": "Sin banderas adicionales. Los aciertos de firmas, Atención adicional y seguimientos ya cubren patrones nombrados.",
    "Unmatched rotating BLE omitted from lists ($omittedRand). Counts include them. Sit export has every radio.": "BLE rotativos no coincidentes omitidos ($omittedRand). Los totales los incluyen. La exportación tiene cada radio.",
    "That can mean someone started following you (their phone or tag), or a device was added during the trip.": "Eso puede significar que alguien comenzó a seguirlo, o se agregó un dispositivo durante el viaje.",
    "This debrief includes advertised aircraft positions from radios that broadcast a latitude and longitude.": "Este informe incluye posiciones de aeronaves anunciadas por radios que transmiten una latitud y longitud.",
    "· No GPS-stamped radios tied to this stay (tagging may have started after they were first heard).": "· No hay radios con sello GPS vinculadas a esta parada (el etiquetado pudo comenzar después de escucharlas).",
    "Station-side Wi-Fi (probes/clients) still needs a dedicated sniffer — Fieldwatch cannot see them.": "El Wi-Fi del lado de la estación (sondas/clientes) aún necesita un rastreador dedicado — la app no puede verlos.",
    "Your captions on radios heard in either window. Same KIND+MAC as Named radios. Not catalog Notes.": "Sus leyendas en radios escuchadas en cualquier ventana. Misma TIPO+MAC que Radios nombradas. No notas del catálogo.",
    "Location beacons are usually fixtures in a store or venue — they do not typically move with you.": "Las balizas de ubicación suelen ser instalaciones en una tienda o lugar — normalmente no se mueven con usted.",
    "iBeacon / Minew / Estimote / Kontakt.io / Atrius cart tag radios that stayed with your GPS path.": "Radios iBeacon / Minew / Estimote / Kontakt.io / Atrius que se quedaron en su ruta GPS.",
    "Retail beacon(s) also stayed with the path (unusual — fixtures do not typically move with you):": "Balizas minoristas también se mantuvieron en la ruta (inusual — las instalaciones no se mueven con usted):",
    "Street names are approximate. Do not treat a street as the location of a matched camera or tag.": "Los nombres de las calles son aproximados. No trate una calle como la ubicación exacta de una cámara o etiqueta.",
    "Your captions on radios heard in this window. Same KIND+MAC as Named radios. Not catalog Notes.": "Sus leyendas en radios escuchadas en esta ventana. Misma TIPO+MAC que Radios nombradas. No notas de catálogo.",
    "Locally administered address. The local bit is set, so this is not an IEEE factory assignment.": "Dirección administrada localmente. El bit local está configurado, no es una asignación de fábrica IEEE.",
    "They are not typically planted trackers. Account for each MAC. Not a finding and not identity.": "Normalmente no son rastreadores plantados. Considere cada MAC. No es un hallazgo ni una identidad.",
    "Finder tags (AirTag / Find My, SmartTag, Tile, Chipolo, Pebblebee) and loud pocket Apple BLE.": "Etiquetas de búsqueda (AirTag / Find My, SmartTag, Tile, Chipolo, Pebblebee) y BLE de Apple de bolsillo.",
    "Enable Tag detections with GPS and walk 50+ m, then run Debrief again for a following test.": "Habilite las detecciones con GPS, camine más de 50m y vuelva a ejecutar el Informe para una prueba de seguimiento.",
    "No finder tag, retail beacon, or wearable clearly stayed with your GPS path in this window.": "Ninguna etiqueta, baliza minorista o wearable se mantuvo claramente en su ruta GPS en esta ventana.",
    "Typical of a watch or ring you or a companion are wearing. Not typically a planted tracker.": "Típico de un reloj o anillo que usted o un compañero llevan puesto. Normalmente no es un rastreador plantado.",
    "Finder tags (AirTag / SmartTag / Tile / Chipolo / Pebblebee / Find My / loud pocket Apple)": "Etiquetas de búsqueda (AirTag / SmartTag / Tile / Chipolo / Pebblebee / Find My / Apple BLE)",
    "are the tracking test. Retail beacons and wearables that co-travel are listed separately —": "son la prueba de seguimiento. Balizas minoristas y wearables que viajan juntos se enumeran por separado —",
    "House tags and other radios the operator only passed are omitted — they are not tracking.": "Las etiquetas de casa y otras radios que el operador solo pasó se omiten — no están siguiendo.",
    "Possible trackers with you (finder tags, whole sit — yours or planted before you started)": "Posibles rastreadores con usted (etiquetas, sesión completa — suyas o plantadas antes de comenzar)",
    "Radios you marked mine. Heard in this window. Still listed. No beep while the mark is on.": "Radios marcadas como suyas. Escuchadas en esta ventana. Aún listadas. Sin pitido mientras la marca esté activa.",
    "Turn on Settings → Tag detections with GPS, walk or drive 50+ m, then run Debrief again.": "Active Ajustes → Detecciones con GPS, camine o conduzca más de 50m y vuelva a ejecutar Informe.",
    "Use Live → Pause to inspect a busy list. Watch tracker signatures if this sit was noisy.": "Use En Vivo → Pausa para inspeccionar una lista ocupada. Observe firmas de rastreadores si esta sesión fue ruidosa.",
    "Operationally sensitive — neighbor SSIDs, MACs, operator GPS, advertised aircraft track": "Operacionalmente sensible — SSIDs vecinos, MACs, GPS del operador, rutas de aeronaves anunciadas",
    "Fieldwatch (app.czrwatchair) · stock Android · receive-only Wi-Fi AP + BLE advertiser": "CZR WatchAir (app.czrwatchair) · Android de fábrica · AP Wi-Fi (solo recepción) + BLE",
    "This debrief includes operator GPS samples used for distance and the following test.": "Este informe incluye muestras GPS del operador utilizadas para la distancia y la prueba de seguimiento.",
    "Turn on GPS tagging and walk before you can test whether a tracker is following you.": "Active el etiquetado GPS y camine antes de poder probar si un rastreador lo está siguiendo.",
    "Finder tags that were not heard when this sit started, then stayed with your path.": "Etiquetas de búsqueda que no se escucharon al inicio de esta sesión, luego se quedaron en su ruta.",
    "MAC tails (**:**:**) and GPS coordinates masked. Logs on the phone are unchanged.": "Colas MAC (**:**:**) y coordenadas GPS ocultas. Los registros en el teléfono no han cambiado.",
    "they do not typically move with you (beacons) or are usually own kit (wearables).": "normalmente no se mueven con usted (balizas) o suelen ser equipo propio (wearables).",
    "Radios this phone heard. Kind + MAC. BLE rotation is a new row. Not a radio fix.": "Radios que escuchó este teléfono. Tipo + MAC. La rotación BLE es una fila nueva. No es una fijación de radio.",
    "Random / privacy address. The MAC can change, so this is not a lasting identity.": "Dirección aleatoria / de privacidad. La MAC puede cambiar, por lo que no es una identidad duradera.",
    "- Following test: insufficient movement (need ~45 m span). Do not infer a tail.": "- Prueba de seguimiento: movimiento insuficiente (se necesitan ~45 m). No infiera un rastreo.",
    "Not identity. Find My MAC rotation will not stitch a tail that changes address.": "Sin identidad. La rotación de MAC de Find My no unirá un rastreo que cambie de dirección.",
    "Two walks on one north-up frame. Green = this sit. Slate = second sit. $pinNote": "Dos caminatas en un marco. Verde = esta sesión. Pizarra = segunda sesión. $pinNote",
    "off (Settings → Online place names in Debrief). No reverse-geocode this export.": "apagado (Ajustes → Nombres de lugares en línea). No hay geocodificación inversa.",
    "Experimental. Not a legal identity. Stock Android radios — this is what the OS": "Experimental. No es una identidad legal. Radios de Android de fábrica — esto es lo que el SO",
    "With you the whole sit — yours or planted before you started. Account for it.": "Con usted toda la sesión — suyo o plantado antes de comenzar. Considérelo.",
    "≥ 2/3 of GPS stamps at −75 dBm or louder, last stamp not 12 dB below loudest.": "≥ 2/3 de sellos GPS a −75 dBm o más fuerte, último sello no 12 dB por debajo del más fuerte.",
    "No signature hits and no GPS co-travel of trackers in this 15-minute window.": "Sin aciertos de firmas y sin co-viaje GPS de rastreadores en esta ventana de 15 minutos.",
    "Possible tail (finder tags, first heard after this sit started, then stayed)": "Posible cola (etiquetas, escuchadas por primera vez después de iniciar esta sesión)",
    "Retail beacons with you (unusual — fixtures do not typically move with you):": "Balizas minoristas con usted (inusual — las instalaciones no se mueven con usted):",
    "Wearables with you (Garmin / Fitbit / Oura — usually own kit or a companion)": "Wearables con usted (Garmin/Fitbit/Oura — usualmente equipo propio o un compañero)",
    "an Iteris BlueTOAD / Vantage Velocity roadside Bluetooth travel-time reader": "un lector de tiempo de viaje Bluetooth de carretera Iteris BlueTOAD / Vantage Velocity",
    "(no Appearance, Class of Device, or well-known service that names a type).": "(sin Apariencia, Clase de Dispositivo o servicio conocido que nombre un tipo).",
    "GPS tagging is OFF. Fieldwatch cannot test whether a radio moved with you.": "Etiquetado GPS APAGADO. La app no puede probar si una radio se movió con usted.",
    "Pattern match, not identity, not a skimmer detector, not a safety finding.": "Coincidencia de patrón, no identidad, ni detector de skimmer, ni hallazgo de seguridad.",
    "Wearable(s) stayed with the path (usually your watch/ring or a companion):": "Wearable(s) permanecieron en la ruta (usualmente su reloj/anillo o un compañero):",
    "One stay — you did not move far enough in this window to split locations.": "Una parada — no se movió lo suficiente en esta ventana para dividir ubicaciones.",
    "Possible tail extra gates (walks): trail covers ≥ half the operator path,": "Posibles caminatas adicionales: el rastro cubre ≥ la mitad de la ruta del operador,",
    "a Roku streaming stick or Roku TV (often a hidden Wi-Fi Direct remote AP)": "un Roku streaming stick o Roku TV (a menudo un AP remoto Wi-Fi Direct oculto)",
    "High randomized BLE ($rand) — typical of phones, not a tracking finding.": "BLE altamente aleatorizado ($rand) — típico de teléfonos, no es un hallazgo de rastreo.",
    "Marked mine. First heard after the sit started and stayed with the path.": "Marcado como mío. Escuchado después de que comenzara la sesión y se quedó en la ruta.",
    "Dense public / retail / street: many APs and phone-like randomized BLE.": "Público denso / minorista / calle: muchos APs y BLE aleatorizados de teléfonos.",
    "No GPS-tagged $which in this sit. Settings → Tag detections with GPS.": "Sin $which etiquetado con GPS. Ajustes → Detecciones con GPS.",
    ". Account for a test tag or badge before treating it as a follower.": ". Considere una etiqueta de prueba o credencial antes de tratarlo como un seguidor.",
    "Account for every MAC — Fieldwatch cannot tell yours from a plant.": "Considere cada MAC — CZR WatchAir no puede distinguir la suya de una plantada.",
    "Likely a dwelling or small office — few sitting APs, limited BLE.": "Probablemente una vivienda o pequeña oficina — pocos APs estáticos, BLE limitado.",
    "No — broadcast-only (you can hear it, not join it from this scan)": "No — solo transmisión (puede escucharlo, no unirse a él desde este escaneo)",
    "Likely a building with standing infrastructure APs plus patrons.": "Probablemente un edificio con infraestructura de APs fijos y clientes.",
    "Street names came from the phone’s system geocoder while online.": "Los nombres de calles provinieron del geocodificador del sistema del teléfono.",
    "Not the same as a Find My tail. Not a finding and not identity.": "No es lo mismo que un rastreo Find My. No es un hallazgo ni una identidad.",
    "an Adtran fiber gateway (often CenturyLink / Quantum Fiber OEM)": "una puerta de enlace de fibra Adtran",
    "Limited-discoverable: briefly looking for a nearby connection.": "Descubrible limitadamente: buscando brevemente una conexión cercana.",
    "No finder tag clearly stayed with the GPS path in this window.": "Ninguna etiqueta se mantuvo claramente en la ruta GPS en esta ventana.",
    "Walk farther (50+ m) with GPS tagging on, then re-run Debrief.": "Camine más lejos (más de 50 m) con GPS, luego vuelva a ejecutar el Informe.",
    "Garmin / Fitbit / Oura radios that stayed with your GPS path.": "Radios Garmin / Fitbit / Oura que se mantuvieron en su ruta GPS.",
    "Radios you marked mine. Heard in either window. Still listed.": "Radios marcadas como suyas. Escuchadas en cualquier ventana. Aún listadas.",
    "a Franklin Technology 5G home-internet gateway (RG3100 class)": "una puerta de enlace 5G Franklin Technology",
    "an ASSA ABLOY lock, Yale lock, HID reader, or Seos credential": "una cerradura ASSA ABLOY, cerradura Yale, lector HID o credencial Seos",
    "Operationally sensitive — neighbor SSIDs, MACs, operator GPS": "Operacionalmente sensible — SSIDs vecinos, MACs, GPS del operador",
    "Treat as a possible tail until you visually account for it.": "Trátelo como una posible cola hasta que lo verifique visualmente.",
    "BLE-only: no classic Bluetooth (headsets/file-send radio).": "Solo BLE: sin Bluetooth clásico (auriculares/radio de envío de archivos).",
    "Google Fast Pair is present (common on buds and speakers).": "Google Fast Pair presente (común en auriculares y altavoces).",
    "It is on the air, but it did not advertise a product class": "Está en el aire, pero no anunció una clase de producto",
    "Only radios that stayed with the operator path are listed.": "Solo se listan las radios que permanecieron en la ruta del operador.",
    "a Cradlepoint vehicle router (often public-safety / fleet)": "un router de vehículo Cradlepoint (a menudo seguridad pública / flotas)",
    "This is what the device is advertising, not a visual ID.": "Esto es lo que el dispositivo está anunciando, no una identificación visual.",
    "Heard, but not at two GPS points. Cannot test co-travel.": "Escuchado, pero no en dos puntos GPS. No se puede probar viaje conjunto.",
    "a GM in-car hotspot (Cadillac / GMC / Buick / Chevrolet)": "un punto de acceso de coche GM (Cadillac / GMC / Buick / Chevrolet)",
    "FIELD DEBRIEF": "INFORME DE CAMPO",
    "FIELDWATCH FIELD DEBRIEF": "INFORME DE CAMPO DE CZR WATCHAIR",
    "FIELDWATCH SIT COMPARE": "COMPARACIÓN DE SESIÓN DE CZR WATCHAIR",
    "Field debrief": "Informe de campo",
    "Executive summary": "Resumen ejecutivo",
    "GPS co-travel": "Viaje conjunto por GPS",
    "Where you were (operator GPS)": "Dónde estuvo (GPS del operador)",
    "Notable BLE:": "BLE Destacados:",
    "Summary": "Resumen",
    "Top devices": "Dispositivos principales",
    "Classes": "Clases",
    "Tracking alert": "Alerta de seguimiento"
}

def escape_regex(s):
    return re.escape(s).replace(r'\$\{sec\}', r'\$\{sec\}').replace(r'\$omittedRand', r'\$omittedRand').replace(r'\$pinNote', r'\$pinNote').replace(r'\$rand', r'\$rand').replace(r'\$which', r'\$which')

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
    print("Done translating domain files.")

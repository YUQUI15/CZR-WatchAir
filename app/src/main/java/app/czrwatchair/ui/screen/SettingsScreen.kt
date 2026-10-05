package app.czrwatchair.ui.screen

import android.app.ActivityManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.PowerManager
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import app.czrwatchair.ui.component.FieldwatchFilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import app.czrwatchair.ui.component.FieldwatchActionButton
import app.czrwatchair.ui.component.FieldwatchOutlinedField
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import app.czrwatchair.ui.component.FieldwatchSlider
import androidx.compose.material3.Surface
import app.czrwatchair.ui.component.FieldwatchSwitch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import app.czrwatchair.R
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import app.czrwatchair.domain.AlertVoiceWhat
import app.czrwatchair.domain.AppSettings
import app.czrwatchair.domain.ScanIntensity
import app.czrwatchair.domain.TakDefaults
import app.czrwatchair.domain.TakFeedStatus
import app.czrwatchair.domain.TakPublish
import app.czrwatchair.domain.TakUdpPreset
import app.czrwatchair.radio.WifiRadio
import app.czrwatchair.ui.NestedTabInsets
import app.czrwatchair.ui.NestedTopBar
import app.czrwatchair.ui.FieldwatchUi
import app.czrwatchair.ui.FieldwatchViewModel
import app.czrwatchair.ui.component.SectionCard
import app.czrwatchair.ui.component.FieldwatchFilterChip
import app.czrwatchair.ui.component.StableCaption
import app.czrwatchair.ui.component.StickyHeight
import java.net.Inet4Address
import java.net.NetworkInterface

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun SettingsScreen(
    state: FieldwatchUi,
    vm: FieldwatchViewModel,
    onRadioBookmarks: () -> Unit,
    onShowLiveTour: () -> Unit = {},
) {
    val context = LocalContext.current
    val settings = state.settings
    val saveSignatures = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri -> uri?.let(vm::saveSignaturesToUri) }
    val importSignatures = rememberLauncherForActivityResult(
        ActivityResultContracts.OpenDocument(),
    ) { uri -> uri?.let(vm::importSignaturesFromUri) }
    val saveSettings = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri -> uri?.let(vm::saveSettingsToUri) }
    val importSettings = rememberLauncherForActivityResult(
        ActivityResultContracts.OpenDocument(),
    ) { uri -> uri?.let(vm::importSettingsFromUri) }
    var confirmRestore by remember { mutableStateOf(false) }
    Scaffold(
        contentWindowInsets = NestedTabInsets,
        topBar = { NestedTopBar("Ajustes") },
    ) { pad ->
        Column(
            Modifier
                .padding(pad)
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            SectionCard("Apariencia") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Modo claro (paleta pastel)", Modifier.weight(1f))
                FieldwatchSwitch(settings.lightTheme, { on -> vm.updateSettings { it.copy(lightTheme = on) } })
            }
            Text(
                "Activado por defecto. Fondo claro con la paleta pastel de CZR WatchAir. Si lo apagas, la app vuelve a la pantalla oscura de campo. El modo nocturno siempre tiene prioridad.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Modo nocturno", Modifier.weight(1f))
                FieldwatchSwitch(settings.nightMode, { on -> vm.updateSettings { it.copy(nightMode = on) } })
            }
            Text(
                "Apagado por defecto. Pantalla en rojo sobre negro para que marcas y textos " +
                    "no arrojen brillo verde o azul en la oscuridad. El fondo se mantiene oscuro. " +
                    "El brillo del teléfono no cambia.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Mantener pantalla encendida", Modifier.weight(1f))
                FieldwatchSwitch(settings.keepScreenOn, { on -> vm.updateSettings { it.copy(keepScreenOn = on) } })
            }
            Text(
                "Encendido por defecto. Evita que la pantalla se apague mientras CZR WatchAir está abierto para no detener BLE. El escaneo sigue en segundo plano. Apáguelo al guardarlo en el bolsillo.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Modo privacidad", Modifier.weight(1f))
                FieldwatchSwitch(settings.demoMode, { on -> vm.updateSettings { it.copy(demoMode = on) } })
            }
            Text(
                "Oculta los últimos tres octetos de cada MAC en reportes y listas como **:**:**. Las coordenadas exportadas en informes se 'enmascaran'. Los registros, la búsqueda y la trilateración siguen usando la MAC real internamente. Apagado por defecto.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            }

            SectionCard("Escaneando") {
            val label = when (settings.intensity) {
                ScanIntensity.SAVER -> "Ahorro de batería"
                ScanIntensity.BALANCED -> "Balanced"
                ScanIntensity.PERFORMANCE -> "Alto rendimiento"
            }
            Text("Intensidad de escaneo  ·  $label")
            FieldwatchSlider(
                value = settings.intensity.ordinal.toFloat(),
                onValueChange = { v ->
                    val next = ScanIntensity.entries[v.toInt().coerceIn(0, 2)]
                    vm.updateSettings { it.copy(intensity = next) }
                },
                valueRange = 0f..2f,
                steps = 1,
            )
            Text(
                "Wi-Fi se escanea por lotes: Alto rendimiento pide escaneos cada ~30s (el límite de Android es 4 cada 2 minutos). BLE fluye entre medio.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            StableCaption(
                state.throttleHint.ifBlank { " " },
                "Wi-Fi esperando al SO",
                "Escaneo Wi-Fi",
                "Wi-Fi próx 99s",
                " ",
            )

            val lifecycleOwner = LocalLifecycleOwner.current
            var osThrottled by remember { mutableStateOf(WifiRadio.osScanThrottled(context)) }
            var backgroundAllowed by remember { mutableStateOf(isBackgroundUsageAllowed(context)) }
            var unrestricted by remember { mutableStateOf(isIgnoringBatteryOptimizations(context)) }
            var needDevOptions by remember { mutableStateOf(false) }
            var batteryGate by remember { mutableStateOf<BatteryAndroidGate?>(null) }
            DisposableEffect(lifecycleOwner) {
                val obs = LifecycleEventObserver { _, event ->
                    if (event == Lifecycle.Event.ON_RESUME) {
                        osThrottled = WifiRadio.osScanThrottled(context)
                        backgroundAllowed = isBackgroundUsageAllowed(context)
                        unrestricted = isIgnoringBatteryOptimizations(context)
                    }
                }
                lifecycleOwner.lifecycle.addObserver(obs)
                onDispose { lifecycleOwner.lifecycle.removeObserver(obs) }
            }
            val fastActive = settings.wifiFastScan && !osThrottled
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Escaneos Wi-Fi más rápidos", Modifier.weight(1f))
                FieldwatchSwitch(
                    checked = settings.wifiFastScan,
                    onCheckedChange = { on ->
                        if (!on) {
                            vm.updateSettings { it.copy(wifiFastScan = false) }
                        } else if (!osThrottled) {
                            vm.updateSettings { it.copy(wifiFastScan = true) }
                        } else {
                            needDevOptions = true
                        }
                    },
                )
            }
            StableCaption(
                when {
                    Build.VERSION.SDK_INT < 30 ->
                        "Necesita Android 11+ para leer la limitación de escaneo Wi-Fi."
                    fastActive ->
                        "On. Fieldwatch asks for a new AP list about every 8 seconds. Uses more battery and heat. If the OS starts refusing scans, it backs off."
                    settings.wifiFastScan && osThrottled ->
                        "Guardado pero sin efecto — la limitación Wi-Fi sigue encendida en Desarrollador."
                    else ->
                        "Android de fábrica permite ~4 escaneos Wi-Fi en 2 min. Esto solo funciona tras apagar 'Limitación de escaneo Wi-Fi' en Opciones de Desarrollador. La app solo verifica ese estado, no puede cambiarlo por usted."
                },
                "Necesita Android 11+ para leer la limitación de escaneo Wi-Fi.",
                "On. Fieldwatch asks for a new AP list about every 8 seconds. Uses more battery and heat. If the OS starts refusing scans, it backs off.",
                "Guardado pero sin efecto — la limitación Wi-Fi sigue encendida en Desarrollador.",
                "Android de fábrica permite ~4 escaneos Wi-Fi en 2 min. Esto solo funciona tras apagar 'Limitación de escaneo Wi-Fi' en Opciones de Desarrollador. La app solo verifica ese estado, no puede cambiarlo por usted.",
            )
            if (needDevOptions) {
                AlertDialog(
                    onDismissRequest = { needDevOptions = false },
                    title = { Text("Se requieren opciones de desarrollador") },
                    text = {
                        Text(
                            if (Build.VERSION.SDK_INT < 30) {
                                "Este teléfono es anterior a Android 11, por lo que CZR WatchAir no puede leer el estado de limitación Wi-Fi."
                            } else {
                                "Android aún está limitando escaneos Wi-Fi. La app no habilitará escaneos rápidos hasta apagar esto.\\n\\n" +
                                    "Habilite Opciones de Desarrollador, y apague Limitación de Búsqueda Wi-Fi. Vuelva aquí después."
                            },
                        )
                    },
                    confirmButton = {
                        if (Build.VERSION.SDK_INT >= 30) {
                            TextButton(
                                onClick = {
                                    needDevOptions = false
                                    runCatching {
                                        context.startActivity(Intent(Settings.ACTION_APPLICATION_DEVELOPMENT_SETTINGS))
                                    }
                                },
                            ) { Text("Abrir opciones de desarrollador") }
                        } else {
                            TextButton(onClick = { needDevOptions = false }) { Text("OK") }
                        }
                    },
                    dismissButton = {
                        if (Build.VERSION.SDK_INT >= 30) {
                            TextButton(onClick = { needDevOptions = false }) { Text("Ahora no") }
                        }
                    },
                )
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Uso en segundo plano", Modifier.weight(1f))
                FieldwatchSwitch(
                    checked = backgroundAllowed,
                    onCheckedChange = { batteryGate = BatteryAndroidGate.BACKGROUND },
                )
            }
            Text(
                "Refleja Permitir uso en segundo plano de Android. " +
                    "Use el interruptor. Apagado: el SO puede matar la app " +
                    "tan pronto salga de ella.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Batería sin restricciones", Modifier.weight(1f))
                FieldwatchSwitch(
                    checked = unrestricted,
                    onCheckedChange = { batteryGate = BatteryAndroidGate.UNRESTRICTED },
                )
            }
            Text(
                "Refleja el ajuste Sin restricciones de Android. Algunos teléfonos no " +
                    "abren esa opción directo. Si ve 'Permitir en segundo plano', toque " +
                    "y seleccione Sin restricciones. La app se actualiza al regresar.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (batteryGate != null) {
                val background = batteryGate == BatteryAndroidGate.BACKGROUND
                AlertDialog(
                    onDismissRequest = { batteryGate = null },
                    title = {
                        Text(if (background) "Uso en segundo plano" else "Batería sin restricciones")
                    },
                    text = {
                        Text(
                            if (background) {
                                "La siguiente es la página de Batería. Active el interruptor de segundo plano. " +
                                    "La app se actualizará cuando regrese."
                            } else {
                                "Algunos teléfonos no abren directo en Sin Restricciones. " +
                                    "Optimized / Restricted. If you only see Allow background usage, " +
                                    "Toque la fila (las palabras, no el interruptor) " +
                                    "y luego seleccione Sin restricciones."
                            },
                        )
                    },
                    confirmButton = {
                        TextButton(
                            onClick = {
                                val gate = batteryGate
                                batteryGate = null
                                openAppBatteryPage(
                                    context,
                                    highlightBackground = gate == BatteryAndroidGate.BACKGROUND,
                                )
                            },
                        ) { Text("Abrir ajustes de Android") }
                    },
                    dismissButton = {
                        TextButton(onClick = { batteryGate = null }) { Text("Ahora no") }
                    },
                )
            }
            }

            SectionCard("Lista de vigilancia") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Alertas de vigilancia", Modifier.weight(1f))
                FieldwatchSwitch(settings.alertsEnabled, { on -> vm.updateSettings { it.copy(alertsEnabled = on) } })
            }
            Text(
                "Encendido por defecto. Interruptor maestro para alertas. Apagado: no hay pitido ni flash. Los marcadores seguirán funcionando pero sin notificaciones.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            val radioWatchN = state.watchlist.count { it.deviceKey != null }
            FieldwatchActionButton(
                onClick = onRadioBookmarks,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Radios nombradas ($radioWatchN)") }
            Text(
                "Nombres personalizados para una MAC. La alerta es opcional. Filtros → Radios nombradas las muestra.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Pitido en firmas vigiladas", Modifier.weight(1f))
                FieldwatchSwitch(
                    settings.alertBeep,
                    { on -> vm.updateSettings { it.copy(alertBeep = on) } },
                    enabled = settings.alertsEnabled,
                )
            }
            Text(
                "Doble pitido en el volumen multimedia cuando aparece una radio vigilada. Detecciones quietas no vuelven a sonar. Independiente de la voz. Suba el volumen si no escucha.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Voz en firmas vigiladas", Modifier.weight(1f))
                FieldwatchSwitch(
                    settings.alertVoice,
                    { on -> vm.updateSettings { it.copy(alertVoice = on) } },
                    enabled = settings.alertsEnabled,
                )
            }
            Text(
                "Encendido por defecto. Habla en el volumen multimedia. Independiente del pitido. Si ya se está hablando, la segunda voz se salta.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text("Qué decir", style = MaterialTheme.typography.labelLarge)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                AlertVoiceWhat.entries.forEach { item ->
                    FieldwatchFilterChip(
                        selected = settings.alertVoiceWhat == item,
                        onClick = { vm.updateSettings { it.copy(alertVoiceWhat = item) } },
                        enabled = settings.alertsEnabled && settings.alertVoice,
                        label = { Text(item.label()) },
                    )
                }
            }
            Text(
                "For signature watches: Class is the Live glyph bucket (finder tags, audio, …). Signature is the catalog row (Apple AirTags, Axon, …). Class + signature (default) says both. A named radio with Alert on always says its custom name, even if it has no class. Test alert plays the signature mix you have on.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            FieldwatchActionButton(
                onClick = vm::testWatchBeep,
                modifier = Modifier.fillMaxWidth(),
                enabled = settings.alertsEnabled && (settings.alertBeep || settings.alertVoice),
            ) { Text("Alerta de prueba") }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Saltar a nueva detección", Modifier.weight(1f))
                FieldwatchSwitch(
                    settings.snapToBeep,
                    { on -> vm.updateSettings { it.copy(snapToBeep = on) } },
                    enabled = settings.alertsEnabled && (settings.alertBeep || settings.alertVoice),
                )
            }
            Text(
                "Cuando aparece una nueva alerta, la vista En vivo se desplaza a ella para que la vea. Funciona con pitido/voz. Apague si no desea que la lista salte sola.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Notificación del sistema", Modifier.weight(1f))
                FieldwatchSwitch(
                    settings.alertShade,
                    { on -> vm.updateSettings { it.copy(alertShade = on) } },
                    enabled = settings.alertsEnabled,
                )
            }
            Text(
                "Opcional. Muestra una notificación silenciosa cuando aparece una radio vigilada. Apagado por defecto.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            }

            SectionCard("Ubicación") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Etiquetar con GPS", Modifier.weight(1f))
                FieldwatchSwitch(settings.tagLocation, { on -> vm.updateSettings { it.copy(tagLocation = on) } })
            }
            Text(
                "Encendido por defecto. Pide GPS en vivo y sella cada detección (Detalles, Rastreo, " +
                    "Informes y archivos). Se ignora el último conocido si tiene más de 30s." +
                    "Ese es su GPS en ese momento, no de la otra radio." +
                    "Use Ubicación de alta precisión. Apague si no desea registrar coordenadas del operador." +
                    "Los marcadores TAK necesitan esto; las coordenadas anunciadas (Remote ID) no.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Nombres y mapas en línea", Modifier.weight(1f))
                FieldwatchSwitch(settings.onlineLookup, { on -> vm.updateSettings { it.copy(onlineLookup = on) } })
            }
            Text(
                "Encendido por defecto. Con internet, Informe / Exportar IA usa nombres de lugares reales " +
                    "y muestra mapas en la ruta. " +
                    "No Fieldwatch cloud, no API key. Offline or no geocoder: Debrief uses coordinates only and Path stays the current north-up trace — no error dialog. " +
                    "Apáguelo para mantener las calles fuera de los reportes." +
                    "Exportaciones, Informes y Limpiar registro están en la pestaña Reportes.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            }

            SectionCard("TAK / CoT") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Salida TAK / CoT", Modifier.weight(1f))
                FieldwatchSwitch(settings.takEnabled, { on -> vm.updateSettings { it.copy(takEnabled = on) } })
            }
            Text(
                "Apagado por defecto. Envía CoT UDP a ATAK, WinTAK, o iTAK." +
                    "This phone (${TakDefaults.LOOPBACK}:${TakDefaults.PORT}) is ATAK CIV on this handset. " +
                    "LAN multicast is ${TakDefaults.SA_HOST}:${TakDefaults.SA_PORT}. " +
                    "Personalizado es un IPv4 o dominio (solo UDP)." +
                    "Puntos de Escuchado-Aquí se sitúan en el GPS del teléfono con el registro más fuerte y la etiqueta (here)." +
                    "Alejarse no arrastra el marcador; una escucha más fuerte lo mueve." +
                    "Lat/lon anunciada (Remote ID de fábrica) se ubican en la aeronave." +
                    "mantiene un marcador que se mueve." +
                    "Una ubicación decodificada del piloto es un segundo punto." +
                    "Toque un marcador en ATAK para más observaciones (nombre, RSSI)." +
                    "Not direction-finding. Not a Remote ID plugin. Privacy mode pauses the feed.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (settings.takEnabled && settings.demoMode) {
                Text(
                    "Privacy mode is on — the feed is paused so full MACs and coordinates are not sent. Turn Privacy mode off to publish.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary,
                )
            }
            if (settings.takEnabled) {
                TakFeedSettings(settings, vm, state.takStatus)
            }
            }

            SectionCard("Logging") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Guardar detecciones en disco", Modifier.weight(1f))
                FieldwatchSwitch(settings.loggingEnabled, { on -> vm.updateSettings { it.copy(loggingEnabled = on) } })
            }
            StableCaption(
                if (settings.loggingEnabled) {
                    "El registro está encendido. Las nuevas detecciones se guardan en el archivo rotativo."
                } else {
                    "El registro está apagado. El escaneo sigue, pero no se guarda nada hasta encenderlo."
                },
                "El registro está encendido. Las nuevas detecciones se guardan en el archivo rotativo.",
                "El registro está apagado. El escaneo sigue, pero no se guarda nada hasta encenderlo.",
            )
            Text(
                "El archivo es JSON lines. Reportes → Formato exportará CSV o GPX al Guardar o Compartir.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            var rotateDrag by remember { mutableIntStateOf(settings.logRotateKb) }
            var rotateDragging by remember { mutableStateOf(false) }
            LaunchedEffect(settings.logRotateKb) {
                if (!rotateDragging) rotateDrag = settings.logRotateKb
            }
            Text("Rotar a los $rotateDrag KB")
            FieldwatchSlider(
                value = rotateDrag.toFloat(),
                onValueChange = {
                    rotateDragging = true
                    rotateDrag = it.toInt().coerceIn(128, 4096)
                },
                onValueChangeFinished = {
                    vm.updateSettings { s -> s.copy(logRotateKb = rotateDrag) }
                    rotateDragging = false
                },
                valueRange = 128f..4096f,
            )
            var staleDrag by remember { mutableIntStateOf(settings.staleSec) }
            var staleDragging by remember { mutableStateOf(false) }
            LaunchedEffect(settings.staleSec) {
                if (!staleDragging) staleDrag = settings.staleSec
            }
            Text("Caduco después de ${staleDrag}s")
            FieldwatchSlider(
                value = staleDrag.toFloat(),
                onValueChange = {
                    staleDragging = true
                    staleDrag = it.toInt().coerceIn(15, 180)
                },
                onValueChangeFinished = {
                    vm.updateSettings { s -> s.copy(staleSec = staleDrag) }
                    staleDragging = false
                },
                valueRange = 15f..180f,
            )
            StickyHeight("log-stats") {
                Text(
                    "${state.logLines} lines this session  ·  ${vm.logBytes() / 1024} KB on disk. " +
                        "Compartir, Guardar y Limpiar registro están en Reportes.",
                    style = MaterialTheme.typography.bodySmall,
                )
            }
            }

            SectionCard("Firmas") {
            Text(
                "Exporta el catálogo para respaldar. Importar añade pero no borra. Actualizar catálogo reemplaza las filas de fábrica desde GitHub (requiere internet).",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            FieldwatchActionButton(
                onClick = vm::startSignatureShare,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Exportar firmas") }
            FieldwatchActionButton(
                onClick = { saveSignatures.launch(vm.suggestedSignaturesName()) },
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Guardar firmas en tarjeta SD / almacenamiento…") }
            FieldwatchActionButton(
                onClick = {
                    importSignatures.launch(arrayOf("application/json", "text/plain", "*/*"))
                },
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Importar firmas…") }
            FieldwatchActionButton(
                onClick = vm::updateStockCatalogFromGitHub,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Actualizar catálogo de fábrica desde GitHub") }

            FieldwatchActionButton(
                onClick = { confirmRestore = true },
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text("Restaurar firmas y presets predeterminados")
            }
            }

            SectionCard("Respaldo de ajustes") {
            Text(
                "Ajustes, filtros, nombres personalizados y firmas vigiladas. " +
                    "No el catálogo, eso es Exportar firmas. Tampoco los registros de GPS." +
                    "Import replaces those on this phone; the catalog stays. " +
                    "Utilice esto después de reiniciar de fábrica o en un teléfono nuevo.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            FieldwatchActionButton(
                onClick = vm::startSettingsShare,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Exportar ajustes") }
            FieldwatchActionButton(
                onClick = { saveSettings.launch(vm.suggestedSettingsName()) },
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Guardar ajustes en tarjeta SD / almacenamiento…") }
            FieldwatchActionButton(
                onClick = {
                    importSettings.launch(arrayOf("application/json", "text/plain", "*/*"))
                },
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Importar ajustes…") }
            }

            FieldwatchActionButton(
                onClick = onShowLiveTour,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Mostrar tour En vivo") }
            Text(
                "Guía en pantalla en vivo: Configuración de vista, Filtros, Firmas, Reportes. Este botón lo muestra de nuevo.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Text(
                "Fieldwatch ${app.czrwatchair.BuildConfig.VERSION_NAME}  ·  Catalog ${state.catalogVersion}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "Solo Wi-Fi Pasivo + BLE." +
                    "Android de fábrica no puede capturar estaciones Wi-Fi de forma promiscua; solo APs y BLE.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            val footerLifecycle = LocalLifecycleOwner.current
            var ipv4 by remember { mutableStateOf(localIpv4Addresses()) }
            DisposableEffect(footerLifecycle) {
                val obs = LifecycleEventObserver { _, event ->
                    if (event == Lifecycle.Event.ON_RESUME) ipv4 = localIpv4Addresses()
                }
                footerLifecycle.lifecycle.addObserver(obs)
                onDispose { footerLifecycle.lifecycle.removeObserver(obs) }
            }
            Text(
                if (ipv4.isEmpty()) {
                    "IPv4 del teléfono · ninguno"
                } else {
                    "This phone’s IPv4  ·  ${ipv4.joinToString("  ·  ")}"
                },
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(Modifier.height(24.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.45f))
            CreditFooter()
        }
    }
    if (confirmRestore) {
        AlertDialog(
            onDismissRequest = { confirmRestore = false },
            title = { Text("¿Restaurar predeterminados?") },
            text = {
                Text(
                    "Reescribe el catálogo, marcadores de fábrica, " +
                        "filtros, y opciones por defecto. Firmas y filtros personalizados " +
                        "se borrarán. Exporte primero si desea un respaldo. " +
                        "Esta acción es irreversible.",
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        confirmRestore = false
                        vm.restoreDefaults()
                    },
                ) { Text("Restaurar") }
            },
            dismissButton = {
                TextButton(onClick = { confirmRestore = false }) { Text("Cancelar") }
            },
        )
    }
}

@Composable
private fun CreditFooter() {
    val context = LocalContext.current
    val muted = MaterialTheme.colorScheme.onSurfaceVariant
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 14.dp, bottom = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text(
            "Copyright (c) 2026 Off Grid Pete LLC. Adaptado para CZR WatchAir.",
            style = MaterialTheme.typography.labelSmall,
            color = muted,
        )
        Row(
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            SocialChip(
                icon = R.drawable.ic_instagram,
                label = "@OffGridPete",
                tint = muted,
                onClick = { openUrl(context, "https://instagram.com/OffGridPete") },
            )
            SocialChip(
                icon = R.drawable.ic_x,
                label = "@OGridPete",
                tint = muted,
                onClick = { openUrl(context, "https://x.com/OGridPete") },
            )
        }
    }
}

@Composable
private fun SocialChip(
    icon: Int,
    label: String,
    tint: Color,
    onClick: () -> Unit,
) {
    Surface(
        shape = RoundedCornerShape(99.dp),
        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.65f),
        modifier = Modifier.clickable(onClick = onClick),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(
                painter = painterResource(icon),
                contentDescription = label,
                tint = tint,
                modifier = Modifier.size(14.dp),
            )
            Spacer(Modifier.width(6.dp))
            Text(label, style = MaterialTheme.typography.labelMedium, color = tint)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TakFeedSettings(settings: AppSettings, vm: FieldwatchViewModel, status: TakFeedStatus) {
    val muted = MaterialTheme.colorScheme.onSurfaceVariant
    var hostText by remember { mutableStateOf(settings.takHost) }
    var portText by remember { mutableStateOf(settings.takPort.toString()) }
    LaunchedEffect(settings.takHost) { hostText = settings.takHost }
    LaunchedEffect(settings.takPort) { portText = settings.takPort.toString() }
    val preset = TakPublish.udpPreset(settings.takHost, settings.takPort)
    Text("Destination", style = MaterialTheme.typography.labelLarge)
    FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        FieldwatchFilterChip(
            selected = preset == TakUdpPreset.THIS_PHONE,
            onClick = {
                val (host, port) = TakPublish.applyPreset(TakUdpPreset.THIS_PHONE)
                vm.updateSettings { it.copy(takHost = host, takPort = port) }
            },
            enabled = !settings.demoMode,
            label = { Text("Este teléfono") },
        )
        FieldwatchFilterChip(
            selected = preset == TakUdpPreset.LAN_MULTICAST,
            onClick = {
                val (host, port) = TakPublish.applyPreset(TakUdpPreset.LAN_MULTICAST)
                vm.updateSettings { it.copy(takHost = host, takPort = port) }
            },
            enabled = !settings.demoMode,
            label = { Text("LAN multicast") },
        )
        FieldwatchFilterChip(
            selected = preset == TakUdpPreset.CUSTOM,
            onClick = {
                if (preset != TakUdpPreset.CUSTOM) {
                    val (host, port) = TakPublish.applyPreset(TakUdpPreset.CUSTOM)
                    vm.updateSettings { it.copy(takHost = host, takPort = port) }
                }
            },
            enabled = !settings.demoMode,
            label = { Text("Personalizado") },
        )
    }
    Text(
        "This phone: ${TakDefaults.LOOPBACK}:${TakDefaults.PORT} (ATAK CIV on this handset). " +
            "LAN multicast: ${TakDefaults.SA_HOST}:${TakDefaults.SA_PORT} (other ATAKs on this Wi-Fi). " +
            "Personalizado es un IPv4 o dominio (solo UDP)." +
            "If This phone does not plot, use Custom with this phone’s Wi-Fi IPv4 from the footer and port ${TakDefaults.PORT}.",
        style = MaterialTheme.typography.bodySmall,
        color = muted,
    )
    FieldwatchOutlinedField(
        value = hostText,
        onValueChange = { value ->
            hostText = value
            val trimmed = value.trim()
            if (trimmed.isNotEmpty()) {
                vm.updateSettings { it.copy(takHost = trimmed) }
            }
        },
        label = "Host",
        placeholder = TakDefaults.HOST,
        enabled = !settings.demoMode,
    )
    FieldwatchOutlinedField(
        value = portText,
        onValueChange = { value ->
            val filtered = value.filter { it.isDigit() }.take(5)
            portText = filtered
            filtered.toIntOrNull()?.let { n ->
                if (n in 1..65_535) {
                    vm.updateSettings { it.copy(takPort = n) }
                }
            }
        },
        label = "Port",
        placeholder = TakDefaults.PORT.toString(),
        supportingText = "UDP. ATAK CIV ${TakDefaults.PORT}. SA multicast ${TakDefaults.SA_PORT}. Not TCP 8087.",
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
        enabled = !settings.demoMode,
    )
    Text(takStatusLine(status), style = MaterialTheme.typography.bodySmall, color = muted)
    Text("Qué enviar", style = MaterialTheme.typography.labelLarge)
    FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        FieldwatchFilterChip(
            selected = settings.takAttention,
            onClick = { vm.updateSettings { it.copy(takAttention = !it.takAttention) } },
            enabled = !settings.demoMode,
            label = { Text("Atención adicional") },
        )
        FieldwatchFilterChip(
            selected = settings.takPayloadFix,
            onClick = { vm.updateSettings { it.copy(takPayloadFix = !it.takPayloadFix) } },
            enabled = !settings.demoMode,
            label = { Text("Ubicación del payload") },
        )
        FieldwatchFilterChip(
            selected = settings.takWatchlist,
            onClick = { vm.updateSettings { it.copy(takWatchlist = !it.takWatchlist) } },
            enabled = !settings.demoMode,
            label = { Text("Lista de vigilancia") },
        )
        FieldwatchFilterChip(
            selected = settings.takAllSignatures,
            onClick = { vm.updateSettings { it.copy(takAllSignatures = !it.takAllSignatures) } },
            enabled = !settings.demoMode,
            label = { Text("Todas las firmas") },
        )
    }
    Text(
        "Chips independientes. Atención adicional (encendido): cámaras corporales, wearables de grabación, seguridad." +
            "Ubicación del Payload (encendido): lat/lon de mapa de decodificación." +
            "Lista de vigilancia (apagado): firmas marcadas y radios nombradas." +
            "Todas las firmas (apagado): ruidoso en multitudes." +
            "Un marcador necesita coordenadas: payload anunciado o etiqueta GPS." +
            "Guarda la escucha más fuerte, no la última, con etiqueta (here)." +
            "Remote ID mantiene el marcador del dron y el del piloto cuando decodifica.",
        style = MaterialTheme.typography.bodySmall,
        color = muted,
    )
}

private fun takStatusLine(status: TakFeedStatus): String {
    if (status.paused) return "Estado de red · pausado (Modo Privacidad)"
    if (status.error != null) {
        val whenAt = takStatusWhen(status.at)
        return "Feed status  ·  error: ${status.error}" + if (whenAt.isNotEmpty()) "  ·  $whenAt" else ""
    }
    if (status.at <= 0L) {
        return "Estado de red · no ha enviado esta sesión"
    }
    val bits = ArrayList<String>(5)
    bits += "on the feed ${status.onFeed}"
    bits += "sent ${status.sent}"
    if (status.gone > 0) {
        bits += if (status.gone == 1) "1 ido" else "${status.gone} gone"
    }
    if (status.dest.isNotBlank()) bits += status.dest
    val whenAt = takStatusWhen(status.at)
    if (whenAt.isNotEmpty()) bits += whenAt
    val head = "Feed status  ·  ${bits.joinToString("  ·  ")}"
    return if (status.detail.isNotBlank() && status.sent == 0 && status.gone == 0) {
        "$head  ·  ${status.detail}"
    } else {
        head
    }
}

private fun takStatusWhen(at: Long): String {
    if (at <= 0L) return ""
    return java.time.Instant.ofEpochMilli(at)
        .atZone(java.time.ZoneId.systemDefault())
        .format(java.time.format.DateTimeFormatter.ofPattern("HH:mm:ss"))
}

private fun localIpv4Addresses(): List<String> {
    val found = LinkedHashSet<String>()
    val nifs = runCatching {
        java.util.Collections.list(NetworkInterface.getNetworkInterfaces())
    }.getOrDefault(emptyList())
    for (nif in nifs) {
        if (!nif.isUp || nif.isLoopback) continue
        for (addr in java.util.Collections.list(nif.inetAddresses)) {
            if (addr is Inet4Address && !addr.isLoopbackAddress && !addr.isLinkLocalAddress) {
                addr.hostAddress?.let { found += it }
            }
        }
    }
    return found.toList()
}

private fun isIgnoringBatteryOptimizations(context: Context): Boolean =
    context.getSystemService(PowerManager::class.java)
        ?.isIgnoringBatteryOptimizations(context.packageName) == true

private fun isBackgroundUsageAllowed(context: Context): Boolean =
    context.getSystemService(ActivityManager::class.java)?.isBackgroundRestricted != true

private enum class BatteryAndroidGate { BACKGROUND, UNRESTRICTED }

/**
 * Fieldwatch’s per-app Battery page. Samsung keeps Allow background usage and
 * Unrestricted on this same screen. [highlightBackground] asks Settings to
 * focus the background-usage switch when the OEM supports it.
 */
private fun openAppBatteryPage(context: Context, highlightBackground: Boolean) {
    val pkgUri = Uri.fromParts("package", context.packageName, null)
    val attempts = listOf(
        Intent("android.settings.VIEW_ADVANCED_POWER_USAGE_DETAIL").apply {
            data = pkgUri
            addCategory(Intent.CATEGORY_DEFAULT)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            putExtra("request_ignore_background_restriction", highlightBackground)
            if (!highlightBackground) {
                putExtra(":settings:fragment_args_key", "unrestricted_pref")
            }
        },
        Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = pkgUri
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        },
    )
    for (intent in attempts) {
        if (intent.resolveActivity(context.packageManager) == null) continue
        if (runCatching { context.startActivity(intent) }.isSuccess) return
    }
}

private fun openUrl(context: android.content.Context, url: String) {
    runCatching {
        context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    }
}

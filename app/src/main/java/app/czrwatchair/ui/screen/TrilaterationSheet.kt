package app.czrwatchair.ui.screen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import app.czrwatchair.domain.TrilaterationEngine
import app.czrwatchair.ui.FieldwatchViewModel
import app.czrwatchair.ui.component.FieldwatchActionButton
import java.util.Locale

/**
 * Localiza el emisor que se esta rastreando midiendo su senal desde 3 o mas lugares.
 * El usuario camina, marca un punto en cada sitio y la app calcula la posicion estimada.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrilaterationSheet(vm: FieldwatchViewModel, onDismiss: () -> Unit) {
    val tri by vm.tri.collectAsStateWithLifecycle()
    val sheet = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = sheet) {
        Column(
            Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .navigationBarsPadding()
                .padding(horizontal = 20.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                "Localizar por trilateración",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                "Camina hasta 3 lugares distintos (al menos ${TrilaterationEngine.MIN_SEPARATION_M.toInt()} m entre sí, " +
                    "sin quedar en línea recta). En cada uno espera unos segundos y pulsa «Marcar punto». " +
                    "Luego calcula la posición estimada del emisor.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                "Puntos marcados: ${tri.points.size}",
                fontWeight = FontWeight.Bold,
            )
            tri.points.forEachIndexed { i, p ->
                Text(
                    String.format(Locale.US, "%d.  %.5f, %.5f   %d dBm", i + 1, p.lat, p.lon, p.rssi.toInt()),
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.bodySmall,
                )
            }
            tri.message?.let {
                Text(it, color = MaterialTheme.colorScheme.onSurface, style = MaterialTheme.typography.bodyMedium)
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                FieldwatchActionButton(onClick = vm::markTriPoint, modifier = Modifier.weight(1f)) {
                    Text("Marcar punto")
                }
                FieldwatchActionButton(
                    onClick = vm::computeTri,
                    modifier = Modifier.weight(1f),
                    enabled = tri.points.size >= 3,
                ) {
                    Text("Calcular")
                }
            }
            FieldwatchActionButton(
                onClick = vm::clearTri,
                modifier = Modifier.fillMaxWidth(),
                enabled = tri.points.isNotEmpty() || tri.result != null,
            ) {
                Text("Reiniciar puntos")
            }
            tri.result?.let { r ->
                val coherence = when {
                    r.residualM <= 5.0 -> "alta"
                    r.residualM <= 15.0 -> "media"
                    else -> "baja (señal inestable u obstáculos)"
                }
                Text(
                    "Posición estimada",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    String.format(
                        Locale.US,
                        "A unos %d m hacia el %s (%d°) desde tu posición",
                        r.distanceM.toInt(),
                        TrilaterationEngine.cardinal(r.bearingDeg),
                        r.bearingDeg.toInt(),
                    ),
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    String.format(Locale.US, "%.5f, %.5f", r.lat, r.lon),
                    fontFamily = FontFamily.Monospace,
                )
                Text("Coherencia de las lecturas: $coherence", style = MaterialTheme.typography.bodyMedium)
            }
            Text(
                "Es una orientación aproximada: la señal cambia con paredes, cuerpo y antena. " +
                    "Funciona mejor al aire libre; en interiores úsala solo como pista.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

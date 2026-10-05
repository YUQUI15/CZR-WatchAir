package app.czrwatchair.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Phosphor = Color(0xFF3DFF9A)
/** Checked switch / slider fill — same hue as Phosphor, less neon. */
val PhosphorActive = Color(0xFF35D683)
val Amber = Color(0xFFFFB020)
val SignalRed = Color(0xFFFF3D5A)
val Cyan = Color(0xFF4FC3F7)
val Night = Color(0xFF0B0F14)
val Panel = Color(0xFF141A22)
val Panel2 = Color(0xFF1B232D)

private val DarkColors = darkColorScheme(
    primary = Phosphor,
    onPrimary = Color(0xFF003820),
    primaryContainer = Color(0xFF163326),
    onPrimaryContainer = Phosphor,
    secondary = Amber,
    onSecondary = Color(0xFF2A1A00),
    tertiary = Cyan,
    background = Night,
    onBackground = Color(0xFFD5DCE3),
    surface = Panel,
    onSurface = Color(0xFFD5DCE3),
    surfaceVariant = Panel2,
    onSurfaceVariant = Color(0xFF9AA6B2),
    outline = Color(0xFF2A3340),
    error = SignalRed,
)

/**
 * Red-on-black field display. Background stays dark; chrome and accents
 * are red ramps. Used only while Settings → Night mode is on.
 */
private val NightColors = darkColorScheme(
    primary = Color(0xFFFF5A5A),
    onPrimary = Color(0xFF2A0808),
    primaryContainer = Color(0xFF3A1212),
    onPrimaryContainer = Color(0xFFFF8A8A),
    secondary = Color(0xFFE07070),
    onSecondary = Color(0xFF2A0808),
    tertiary = Color(0xFFCC6666),
    background = Color(0xFF0B0808),
    onBackground = Color(0xFFFFC9C9),
    surface = Color(0xFF161010),
    onSurface = Color(0xFFFFC9C9),
    surfaceVariant = Color(0xFF1E1414),
    onSurfaceVariant = Color(0xFFC48A8A),
    outline = Color(0xFF5A3030),
    error = Color(0xFFFF7A7A),
)


/** Paleta pastel oficial de CZR WatchAir (modo claro). */
val PastelYellow = Color(0xFFF3EFA1)
val PastelRose = Color(0xFFFEAEBB)
val PastelPink = Color(0xFFF3B2DB)
val PastelPurple = Color(0xFFC19ADE)
val PastelBlue = Color(0xFF6FCFEB)
val PastelTeal = Color(0xFF99E6D8)

/** Acento intenso derivado del morado pastel: interruptores, deslizadores y bordes activos con contraste >= 3:1. */
val PastelActive = Color(0xFF9A7BB2)

/**
 * Modo claro con la paleta pastel. Los rellenos usan los tonos exactos de la paleta;
 * los textos y trazos usan tintas oscuras derivadas para mantener el contraste (WCAG AA).
 */
private val LightColors = lightColorScheme(
    primary = PastelBlue,
    onPrimary = Color(0xFF0B2A33),
    primaryContainer = PastelTeal,
    onPrimaryContainer = Color(0xFF06302A),
    secondary = PastelPurple,
    onSecondary = Color(0xFF2B1240),
    secondaryContainer = PastelPink,
    onSecondaryContainer = Color(0xFF3B0F2D),
    tertiary = PastelYellow,
    onTertiary = Color(0xFF3A3600),
    tertiaryContainer = PastelYellow,
    onTertiaryContainer = Color(0xFF3A3600),
    background = Color(0xFFFBFAFF),
    onBackground = Color(0xFF12171C),
    surface = Color.White,
    onSurface = Color(0xFF12171C),
    surfaceVariant = Color(0xFFEEE8F6),
    onSurfaceVariant = Color(0xFF46404F),
    surfaceTint = PastelBlue,
    outline = Color(0xFF9C8DB0),
    outlineVariant = Color(0xFFDDD3E8),
    error = Color(0xFFB3263E),
    onError = Color.White,
    errorContainer = PastelRose,
    onErrorContainer = Color(0xFF4A0A16),
)

val Mono = TextStyle(
    fontFamily = FontFamily.Monospace,
    fontWeight = FontWeight.Medium,
    fontSize = 12.sp,
    letterSpacing = 0.3.sp,
)

/**
 * Indica si la tinta de dibujo debe oscurecerse para leerse sobre fondo claro.
 * Se fija en [CZRWatchAirTheme] antes de componer el contenido; [nightIf] lo consulta
 * porque se invoca tambien desde lambdas de dibujo que no pueden leer CompositionLocal.
 */
object DayInk {
    @Volatile
    var light: Boolean = false
}

@Composable
fun FieldwatchTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    nightMode: Boolean = false,
    content: @Composable () -> Unit,
) {
    val scheme = when {
        nightMode -> NightColors
        darkTheme -> DarkColors
        else -> LightColors
    }
    DayInk.light = !nightMode && !darkTheme
    CompositionLocalProvider(LocalNightMode provides nightMode) {
        MaterialTheme(
            colorScheme = scheme,
            content = content,
        )
    }
}

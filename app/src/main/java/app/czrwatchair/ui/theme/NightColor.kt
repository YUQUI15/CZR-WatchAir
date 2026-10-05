package app.czrwatchair.ui.theme

import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb

val LocalNightMode = staticCompositionLocalOf { false }

/**
 * Map any sRGB color to a red luminance ramp (cockpit / field night display).
 * Relative brightness is kept so class chips stay distinguishable.
 */
fun nightForegroundArgb(argb: Int): Int {
    val a = (argb ushr 24) and 0xFF
    val r = (argb shr 16) and 0xFF
    val g = (argb shr 8) and 0xFF
    val b = argb and 0xFF
    val y = (0.2126f * r + 0.7152f * g + 0.0722f * b) / 255f
    val nr = (0.40f + 0.60f * y).coerceIn(0f, 1f)
    val ng = (0.05f + 0.16f * y).coerceIn(0f, 1f)
    val nb = (0.05f + 0.10f * y).coerceIn(0f, 1f)
    return (a shl 24) or
        (((nr * 255f).toInt() and 0xFF) shl 16) or
        (((ng * 255f).toInt() and 0xFF) shl 8) or
        ((nb * 255f).toInt() and 0xFF)
}

fun Color.asNightForeground(): Color = Color(nightForegroundArgb(toArgb()))

/**
 * Oscurece una tinta de dibujo (verde neon, ambar, cian, rojo...) para que se lea sobre
 * un fondo claro. Conserva el matiz y limita la luminosidad HSL a [MAX_LIGHTNESS].
 */
fun dayInkArgb(argb: Int): Int {
    val a = (argb ushr 24) and 0xFF
    val r = ((argb shr 16) and 0xFF) / 255f
    val g = ((argb shr 8) and 0xFF) / 255f
    val b = (argb and 0xFF) / 255f
    val max = maxOf(r, g, b)
    val min = minOf(r, g, b)
    val l = (max + min) / 2f
    val d = max - min
    val s = if (d == 0f) 0f else d / (1f - kotlin.math.abs(2f * l - 1f))
    val h = when {
        d == 0f -> 0f
        max == r -> 60f * (((g - b) / d) % 6f)
        max == g -> 60f * (((b - r) / d) + 2f)
        else -> 60f * (((r - g) / d) + 4f)
    }.let { if (it < 0f) it + 360f else it }
    val l2 = minOf(l, MAX_LIGHTNESS)
    val s2 = if (s < 0.05f) s else maxOf(s, 0.55f)
    val c = (1f - kotlin.math.abs(2f * l2 - 1f)) * s2
    val x = c * (1f - kotlin.math.abs((h / 60f) % 2f - 1f))
    val m = l2 - c / 2f
    val (rp, gp, bp) = when {
        h < 60f -> Triple(c, x, 0f)
        h < 120f -> Triple(x, c, 0f)
        h < 180f -> Triple(0f, c, x)
        h < 240f -> Triple(0f, x, c)
        h < 300f -> Triple(x, 0f, c)
        else -> Triple(c, 0f, x)
    }
    fun ch(v: Float) = (((v + m) * 255f).toInt()).coerceIn(0, 255)
    return (a shl 24) or (ch(rp) shl 16) or (ch(gp) shl 8) or ch(bp)
}

private const val MAX_LIGHTNESS = 0.36f

fun Color.asDayInk(): Color = Color(dayInkArgb(toArgb()))

/** Darkens the ink only while the pastel light theme is active; identity otherwise. */
fun Color.dayIf(): Color = if (DayInk.light) asDayInk() else this

/**
 * Identity in dark mode. Night mode maps to the red ramp; in the pastel light theme the ink
 * is darkened so it keeps contrast on a light background.
 */
fun Color.nightIf(night: Boolean): Color = when {
    night -> asNightForeground()
    DayInk.light -> asDayInk()
    else -> this
}

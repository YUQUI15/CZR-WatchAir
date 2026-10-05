package app.czrwatchair.ui.component

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.RowScope
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.surfaceColorAtElevation
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.unit.dp
import app.czrwatchair.ui.theme.LocalNightMode
import app.czrwatchair.ui.theme.PastelActive
import app.czrwatchair.ui.theme.PastelBlue
import app.czrwatchair.ui.theme.PastelTeal
import app.czrwatchair.ui.theme.PhosphorActive
import app.czrwatchair.ui.theme.nightIf

/** Section-tile green (surface at 1.dp). */
@Composable
internal fun spectreSectionFill(): Color {
    if (isLightScheme()) return lerp(Color.White, PastelTeal, 0.22f)
    return MaterialTheme.colorScheme.surfaceColorAtElevation(1.dp)
}

/** True while the pastel light scheme is active (surface is light). */
@Composable
internal fun isLightScheme(): Boolean = MaterialTheme.colorScheme.surface.luminance() > 0.5f

/** Active accent for switches, sliders and selected chips: phosphor in dark, deep pastel purple in light. */
@Composable
internal fun spectreActive(): Color {
    if (isLightScheme()) return PastelActive
    return PhosphorActive.nightIf(LocalNightMode.current)
}

/** Section-tile green, darkened. Shared by action buttons and switch tracks. */
@Composable
internal fun spectreTileFill(): Color {
    if (isLightScheme()) return lerp(Color.White, PastelBlue, 0.30f)
    return lerp(Color.Black, spectreSectionFill(), 0.78f)
}

/** Gray outline shared by action buttons and switches. */
@Composable
internal fun spectreTileEdge(): Color {
    val scheme = MaterialTheme.colorScheme
    return lerp(scheme.outline, scheme.onSurfaceVariant, 0.32f)
}

/** Action button: section-tile green, darkened; gray outline, off-white label. */
@Composable
fun FieldwatchActionButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable RowScope.() -> Unit,
) {
    val scheme = MaterialTheme.colorScheme
    val light = isLightScheme()
    val fill = if (light) scheme.primary else spectreTileFill()
    val ink = if (light) scheme.onPrimary else scheme.onSurface
    val edge = if (light) lerp(PastelBlue, Color.Black, 0.28f) else spectreTileEdge()
    OutlinedButton(
        onClick = onClick,
        modifier = modifier,
        enabled = enabled,
        contentPadding = contentPadding,
        colors = ButtonDefaults.outlinedButtonColors(
            containerColor = fill,
            contentColor = ink,
            disabledContainerColor = fill.copy(alpha = 0.4f),
            disabledContentColor = ink.copy(alpha = 0.38f),
        ),
        border = BorderStroke(1.dp, if (enabled) edge else edge.copy(alpha = 0.4f)),
        content = content,
    )
}

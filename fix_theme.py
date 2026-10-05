import os
import re

path = "app/src/main/java/app/czrwatchair/ui/theme/Theme.kt"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'private val LightColors = lightColorScheme\(.*?\n\)', '''private val LightColors = lightColorScheme(
    primary = Color(0xFF6FCFEB),
    onPrimary = Color.Black,
    primaryContainer = Color(0xFF99E6D8),
    onPrimaryContainer = Color.Black,
    secondary = Color(0xFFF3EFA1),
    onSecondary = Color.Black,
    tertiary = Color(0xFFC19ADE),
    background = Color(0xFFF9FAFB),
    onBackground = Color(0xFF12171C),
    surface = Color.White,
    onSurface = Color(0xFF12171C),
    surfaceVariant = Color(0xFFF3B2DB),
    onSurfaceVariant = Color.Black,
    outline = Color(0xFFC5CDD4),
    error = Color(0xFFFEAEBB),
)''', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

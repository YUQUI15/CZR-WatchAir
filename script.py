import os
import re

def process_theme():
    path = "app/src/main/java/app/czrwatchair/ui/theme/Theme.kt"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    light_colors = """private val LightColors = lightColorScheme(
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
)"""
    
    # Replace the existing LightColors block
    content = re.sub(r'private val LightColors = lightColorScheme\([^)]+\)', light_colors, content, flags=re.MULTILINE | re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_enjambre_ui():
    path = "app/src/main/java/app/czrwatchair/ui/screen/HuntScreen.kt"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's inject a button into the bottom of HuntScreen or top app bar.
    # We can inject it before the last closing brace of Scaffold.
    button_code = """
            Spacer(modifier = Modifier.height(16.dp))
            CZRWatchAirActionButton(
                onClick = { /* TODO: Hook TrilaterationEngine */ },
                text = "Modo Enjambre (Trilateración Mesh)",
                color = MaterialTheme.colorScheme.tertiary
            )
"""
    # Replace "Settings" in HuntScreen
    content = content.replace('"Hunt"', '"Rastrear"')
    
    # Add the button below the Rssi display
    if "Spacer(modifier = Modifier.weight(1f))" in content:
        content = content.replace("Spacer(modifier = Modifier.weight(1f))", button_code + "\n            Spacer(modifier = Modifier.weight(1f))", 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def translate_app():
    translations = {
        '"Settings"': '"Ajustes"',
        '"Settings "': '"Ajustes "',
        '"Live"': '"En vivo"',
        '"Candidates"': '"Candidatos"',
        '"Fleets"': '"Flotas"',
        '"Signatures"': '"Firmas"',
        '"Export"': '"Exportar"',
        '"Clear"': '"Limpiar"',
        '"Stop"': '"Detener"',
        '"Paused"': '"Pausado"',
        '"Scanning"': '"Escaneando"',
        '"Hunt"': '"Rastrear"',
        '"Radar"': '"Radar"',
        '"Devices"': '"Dispositivos"',
        '"Reports"': '"Reportes"',
        '"Background"': '"En segundo plano"',
        '"Foreground"': '"Primer plano"',
        '"Network"': '"Red"',
        '"Unknown"': '"Desconocido"',
        '"Distance"': '"Distancia"',
        '"Signal"': '"Señal"',
        '"Map"': '"Mapa"',
        '"Start"': '"Iniciar"',
        '"Details"': '"Detalles"',
        '"Location"': '"Ubicación"',
        '"History"': '"Historial"'
    }
    
    for root, dirs, files in os.walk("app/src/main/java/app/czrwatchair/ui"):
        for f in files:
            if not f.endswith(".kt"): continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig = content
            for eng, spa in translations.items():
                content = content.replace(eng, spa)
            
            if orig != content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)

process_theme()
add_enjambre_ui()
translate_app()

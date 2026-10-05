package app.czrwatchair.ui

/** Punto de medicion de la trilateracion: posicion GPS y RSSI mediano (dBm) en ese lugar. */
data class TriPoint(val lat: Double, val lon: Double, val rssi: Double)

/** Posicion estimada del emisor y su calidad. [residualM] bajo = lecturas coherentes entre si. */
data class TriResult(
    val lat: Double,
    val lon: Double,
    val distanceM: Double,
    val bearingDeg: Double,
    val residualM: Double,
)

data class TriUi(
    val points: List<TriPoint> = emptyList(),
    val result: TriResult? = null,
    val message: String? = null,
)

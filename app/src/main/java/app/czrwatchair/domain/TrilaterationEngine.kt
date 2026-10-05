package app.czrwatchair.domain

import kotlin.math.PI
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.hypot
import kotlin.math.pow
import kotlin.math.sqrt

/**
 * CZR WatchAir - Trilateracion por RSSI.
 *
 * Estima donde esta un emisor (balizas BLE, AirTag, camaras...) a partir de las lecturas de
 * senal tomadas en 3 o mas puntos distintos. Usa el modelo de perdida logaritmica para
 * convertir dBm en metros y resuelve la posicion por minimos cuadrados lineales, de modo que
 * con mas de 3 puntos el error se promedia en vez de acumularse.
 *
 * El RSSI NO es una medida de distancia exacta: paredes, cuerpo y antena lo alteran. El
 * resultado es una orientacion aproximada (decenas de metros en exteriores, peor en interiores).
 */
object TrilaterationEngine {

    /** Potencia medida a 1 m habitual de un anunciante BLE. */
    const val DEFAULT_TX_POWER = -59

    /** Exponente de perdida de camino: 2.0 espacio libre, 2.5-3.5 con obstaculos. */
    const val DEFAULT_PATH_LOSS = 2.5

    /** Los puntos deben estar al menos a esta distancia entre si para dar geometria util. */
    const val MIN_SEPARATION_M = 5.0

    /** Lectura de senal en un punto. [x], [y] en metros dentro de un plano local. */
    data class NodeReading(
        val x: Double,
        val y: Double,
        val rssi: Double,
        val txPower: Int = DEFAULT_TX_POWER,
    )

    data class Coordinate(val x: Double, val y: Double)

    /**
     * Resultado: [position] estimada y [residualM], el error cuadratico medio entre las
     * distancias medidas y las que implica la posicion (menor = lecturas mas coherentes).
     */
    data class Estimate(val position: Coordinate, val residualM: Double)

    /** Distancia estimada en metros con el modelo de perdida logaritmica. */
    fun calculateDistance(
        rssi: Double,
        txPower: Int = DEFAULT_TX_POWER,
        pathLoss: Double = DEFAULT_PATH_LOSS,
    ): Double = 10.0.pow((txPower - rssi) / (10.0 * pathLoss))

    /**
     * Posicion estimada del emisor, o null si hay menos de 3 lecturas o los puntos estan
     * (casi) alineados y no definen una unica solucion.
     */
    fun locate(
        readings: List<NodeReading>,
        pathLoss: Double = DEFAULT_PATH_LOSS,
    ): Estimate? {
        if (readings.size < 3) return null
        val origin = readings[0]
        val d = readings.map { calculateDistance(it.rssi, it.txPower, pathLoss) }
        val d0sq = d[0] * d[0]

        // Sistema lineal  A p = b  respecto al primer punto (origen local en 0,0).
        var a11 = 0.0
        var a12 = 0.0
        var a22 = 0.0
        var c1 = 0.0
        var c2 = 0.0
        for (i in 1 until readings.size) {
            val xi = readings[i].x - origin.x
            val yi = readings[i].y - origin.y
            val ax = 2.0 * xi
            val ay = 2.0 * yi
            val b = d0sq - d[i] * d[i] + xi * xi + yi * yi
            a11 += ax * ax
            a12 += ax * ay
            a22 += ay * ay
            c1 += ax * b
            c2 += ay * b
        }
        val det = a11 * a22 - a12 * a12
        val scale = (a11 + a22).let { it * it }
        if (scale <= 0.0 || det / scale < COLLINEAR_EPS) return null

        val px = (c1 * a22 - c2 * a12) / det
        val py = (a11 * c2 - a12 * c1) / det
        val position = Coordinate(origin.x + px, origin.y + py)

        var sq = 0.0
        readings.forEachIndexed { i, r ->
            val err = hypot(position.x - r.x, position.y - r.y) - d[i]
            sq += err * err
        }
        return Estimate(position, sqrt(sq / readings.size))
    }

    private const val COLLINEAR_EPS = 1e-3
    private const val EARTH_R_M = 6_371_000.0

    /** Pasa lat/lon a metros (este, norte) respecto a un origen; valido para unos km. */
    fun toLocalMeters(originLat: Double, originLon: Double, lat: Double, lon: Double): Coordinate {
        val x = Math.toRadians(lon - originLon) * EARTH_R_M * cos(Math.toRadians(originLat))
        val y = Math.toRadians(lat - originLat) * EARTH_R_M
        return Coordinate(x, y)
    }

    /** Inversa de [toLocalMeters]: devuelve (lat, lon). */
    fun toLatLon(originLat: Double, originLon: Double, point: Coordinate): Pair<Double, Double> {
        val lat = originLat + Math.toDegrees(point.y / EARTH_R_M)
        val lon = originLon + Math.toDegrees(point.x / (EARTH_R_M * cos(Math.toRadians(originLat))))
        return lat to lon
    }

    /** Rumbo en grados 0..360 (0 = norte, 90 = este) de [from] hacia [to] en el plano local. */
    fun bearingDegrees(from: Coordinate, to: Coordinate): Double {
        val deg = atan2(to.x - from.x, to.y - from.y) * 180.0 / PI
        return (deg + 360.0) % 360.0
    }

    /** Punto cardinal en espanol para un rumbo (N, NE, E, SE, S, SO, O, NO). */
    fun cardinal(bearing: Double): String {
        val names = listOf("N", "NE", "E", "SE", "S", "SO", "O", "NO")
        return names[(((bearing % 360.0) + 360.0) % 360.0 / 45.0 + 0.5).toInt() % 8]
    }
}

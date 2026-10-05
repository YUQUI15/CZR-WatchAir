package app.czrwatchair.domain

import kotlin.math.abs
import kotlin.math.hypot
import kotlin.math.log10
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class TrilaterationEngineTest {

    private fun rssiAt(distanceM: Double, txPower: Int = -59, n: Double = 2.5): Double =
        txPower - 10.0 * n * log10(distanceM)

    private fun reading(x: Double, y: Double, target: TrilaterationEngine.Coordinate) =
        TrilaterationEngine.NodeReading(x, y, rssiAt(hypot(target.x - x, target.y - y)))

    @Test
    fun distanceAndRssiAreInverse() {
        val d = TrilaterationEngine.calculateDistance(rssiAt(12.0))
        assertEquals(12.0, d, 1e-6)
    }

    @Test
    fun threePointsLocateTarget() {
        val target = TrilaterationEngine.Coordinate(7.0, 11.0)
        val est = TrilaterationEngine.locate(
            listOf(reading(0.0, 0.0, target), reading(20.0, 0.0, target), reading(0.0, 20.0, target)),
        )
        assertNotNull(est)
        assertEquals(7.0, est!!.position.x, 0.01)
        assertEquals(11.0, est.position.y, 0.01)
        assertTrue(est.residualM < 0.01)
    }

    @Test
    fun morePointsStillConverge() {
        val target = TrilaterationEngine.Coordinate(-6.0, 4.0)
        val est = TrilaterationEngine.locate(
            listOf(
                reading(0.0, 0.0, target),
                reading(15.0, 3.0, target),
                reading(2.0, 18.0, target),
                reading(-14.0, -9.0, target),
            ),
        )
        assertNotNull(est)
        assertEquals(-6.0, est!!.position.x, 0.01)
        assertEquals(4.0, est.position.y, 0.01)
    }

    @Test
    fun collinearPointsAreRejected() {
        val target = TrilaterationEngine.Coordinate(5.0, 5.0)
        val est = TrilaterationEngine.locate(
            listOf(reading(0.0, 0.0, target), reading(10.0, 0.0, target), reading(20.0, 0.0, target)),
        )
        assertNull(est)
    }

    @Test
    fun fewerThanThreePointsIsNull() {
        val target = TrilaterationEngine.Coordinate(5.0, 5.0)
        assertNull(TrilaterationEngine.locate(listOf(reading(0.0, 0.0, target), reading(9.0, 1.0, target))))
    }

    @Test
    fun noisyReadingsStayNearTarget() {
        val target = TrilaterationEngine.Coordinate(10.0, 10.0)
        val noise = listOf(2.0, -3.0, 1.5)
        val pts = listOf(0.0 to 0.0, 25.0 to 0.0, 0.0 to 25.0)
        val readings = pts.mapIndexed { i, (x, y) ->
            TrilaterationEngine.NodeReading(x, y, rssiAt(hypot(target.x - x, target.y - y)) + noise[i])
        }
        val est = TrilaterationEngine.locate(readings)!!
        val err = hypot(est.position.x - target.x, est.position.y - target.y)
        assertTrue("error $err m", err < 8.0)
    }

    @Test
    fun gpsRoundTripAndBearing() {
        val lat = 4.6097
        val lon = -74.0817
        val p = TrilaterationEngine.toLocalMeters(lat, lon, lat + 0.0009, lon)
        assertEquals(0.0, p.x, 0.5)
        assertEquals(100.0, p.y, 1.0)
        val (la, lo) = TrilaterationEngine.toLatLon(lat, lon, p)
        assertEquals(lat + 0.0009, la, 1e-7)
        assertEquals(lon, lo, 1e-7)
        val origin = TrilaterationEngine.Coordinate(0.0, 0.0)
        assertEquals(0.0, TrilaterationEngine.bearingDegrees(origin, TrilaterationEngine.Coordinate(0.0, 10.0)), 1e-6)
        assertEquals(90.0, TrilaterationEngine.bearingDegrees(origin, TrilaterationEngine.Coordinate(10.0, 0.0)), 1e-6)
        assertEquals(225.0, TrilaterationEngine.bearingDegrees(origin, TrilaterationEngine.Coordinate(-5.0, -5.0)), 1e-6)
        assertEquals("N", TrilaterationEngine.cardinal(359.0))
        assertEquals("SO", TrilaterationEngine.cardinal(225.0))
        assertTrue(abs(TrilaterationEngine.bearingDegrees(origin, origin)) < 360.0)
    }
}

package app.fieldwatch.domain

import kotlin.math.pow

/**
 * CZR WatchAir - Collaborative Mesh Trilateration Engine
 * 
 * Calculates the exact X,Y coordinates of a radio source (like a hidden camera or AirTag)
 * based on the RSSI readings from 3 or more CZR WatchAir devices in the same room.
 */
object TrilaterationEngine {

    data class NodeReading(
        val x: Double,
        val y: Double,
        val rssi: Int,
        val txPower: Int = -59 // Default BLE Tx Power at 1 meter
    )

    data class Coordinate(val x: Double, val y: Double)

    /**
     * Converts RSSI to estimated distance in meters using the Log-Distance Path Loss Model.
     */
    fun calculateDistance(rssi: Int, txPower: Int, environmentalFactor: Double = 2.5): Double {
        return 10.0.pow((txPower - rssi) / (10.0 * environmentalFactor))
    }

    /**
     * Performs 2D Trilateration using the geometric intersection of 3 circles.
     * @param nodeA Reading from WatchAir device 1
     * @param nodeB Reading from WatchAir device 2
     * @param nodeC Reading from WatchAir device 3
     * @return Estimated X,Y coordinates of the hidden target
     */
    fun locateTarget(nodeA: NodeReading, nodeB: NodeReading, nodeC: NodeReading): Coordinate? {
        val dA = calculateDistance(nodeA.rssi, nodeA.txPower)
        val dB = calculateDistance(nodeB.rssi, nodeB.txPower)
        val dC = calculateDistance(nodeC.rssi, nodeC.txPower)

        // Using standard trilateration algebraic resolution
        val p2p1Distance = Math.hypot(nodeB.x - nodeA.x, nodeB.y - nodeA.y)
        
        // Ensure nodes are not in the exact same spot to avoid division by zero
        if (p2p1Distance == 0.0) return null

        val exX = (nodeB.x - nodeA.x) / p2p1Distance
        val exY = (nodeB.y - nodeA.y) / p2p1Distance

        val i = exX * (nodeC.x - nodeA.x) + exY * (nodeC.y - nodeA.y)

        val eyX = (nodeC.x - nodeA.x - i * exX)
        val eyY = (nodeC.y - nodeA.y - i * exY)
        val eyMag = Math.hypot(eyX, eyY)
        
        if (eyMag == 0.0) return null

        val eyXNorm = eyX / eyMag
        val eyYNorm = eyY / eyMag

        val d = p2p1Distance
        val j = eyXNorm * (nodeC.x - nodeA.x) + eyYNorm * (nodeC.y - nodeA.y)

        val x = (Math.pow(dA, 2.0) - Math.pow(dB, 2.0) + Math.pow(d, 2.0)) / (2 * d)
        val y = ((Math.pow(dA, 2.0) - Math.pow(dC, 2.0) + Math.pow(i, 2.0) + Math.pow(j, 2.0)) / (2 * j)) - ((i / j) * x)

        val targetX = nodeA.x + x * exX + y * eyXNorm
        val targetY = nodeA.y + x * exY + y * eyYNorm

        return Coordinate(targetX, targetY)
    }
}

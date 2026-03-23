public class ParticleLeader extends Particle {
    private static final double CENTER_X = 1.0;
    private static final double CENTER_Y = 1.0;
    private static final double ORBIT_RADIUS = 5.0;
    private static final double ORBIT_SPEED = 0.006; // radians per step

    private double orbitAngle = 0.0;

    public ParticleLeader(int id, double x, double y, double theta, double radius, double property, boolean isLeader) {
        super(id, x, y, theta, radius, property, isLeader);
    }

    @Override
    public void calculateNextTheta(double eta, java.util.Random rand) {
        // The leader ignores neighbors and maintains its absolute orbit.
    }

    @Override
    public void updatePosition(double L, boolean periodic) {
        orbitAngle += ORBIT_SPEED;

        double newX = CENTER_X + ORBIT_RADIUS * Math.cos(orbitAngle);
        double newY = CENTER_Y + ORBIT_RADIUS * Math.sin(orbitAngle);

        // Update the velocity vector direction for exportFrame (tangent to orbit)
        setTheta(orbitAngle + Math.PI / 2);

        if (periodic) {
            newX = ((newX % L) + L) % L;
            newY = ((newY % L) + L) % L;
        }

        setX(newX);
        setY(newY);
    }
}

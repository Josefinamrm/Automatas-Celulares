import java.util.HashSet;
import java.util.Set;

public class Particle {
    static final double VELOCITY = 0.03;
    private int id;
    private double x;
    private double y;
    private double theta;
    private double radius;
    private double property;
    private Set<Particle> neighbours;
    private double nextTheta;

    public Particle(int id, double x, double y, double theta, double radius, double property) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.theta = theta;
        this.radius = radius;
        this.property = property;
        this.neighbours = new HashSet<>();
        this.nextTheta = theta;
    }

    public void updatePosition(double L, boolean periodic){
        this.x += VELOCITY * Math.cos(this.theta);
        this.y += VELOCITY * Math.sin(this.theta);
        
        if (periodic) {
            this.x = (this.x % L + L) % L;
            this.y = (this.y % L + L) % L;
        }
    }

    public void calculateNextTheta(double eta, java.util.Random rand) {
        double sinSum = Math.sin(this.theta);
        double cosSum = Math.cos(this.theta);

        for (Particle p : neighbours) {
            sinSum += Math.sin(p.getTheta());
            cosSum += Math.cos(p.getTheta());
        }

        double avgTheta = Math.atan2(sinSum, cosSum);
        double noise = (rand.nextDouble() - 0.5) * eta;
        this.nextTheta = avgTheta + noise;
    }

    public void updateTheta() {
        this.theta = this.nextTheta;
    }

    public int getId() {
        return id;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getTheta() {
        return theta;
    }

    public double getRadius() {
        return radius;
    }

    public double getProperty() {
        return property;
    }

    public Set<Particle> getNeighbours() {
        return neighbours;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public void setTheta(double theta) {
        this.theta = theta;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }

    public void setProperty(double property) {
        this.property = property;
    }

    public void addNeighbour(Particle neighbour) {
        this.neighbours.add(neighbour);
    }

    public void clearNeighbours() {
        this.neighbours.clear();
    }
}
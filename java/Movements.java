public class Movements {
    private Particle[] particles;

    public Movements(Particle[] particles){
        this.particles = particles;
    }

    public void update(double dt, double L, boolean periodic){
        for (Particle p : particles) {
            p.updatePosition(L, periodic);
        }
    }

    public void updateTheta(double theta){
        for (Particle p : particles) {
            p.setTheta(theta);
        }
    }

    
}

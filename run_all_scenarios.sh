#!/bin/bash
# run_all_scenarios.sh
# Ubicar en /root (misma altura que /java, visualize.py, plot_va.py, etc.)
#
# USO:
#   chmod +x run_all_scenarios.sh
#   ./run_all_scenarios.sh
#
# Genera:
#   results/no_leader/eta_X.X/run_Y/particles_frames.txt
#   results/fixed_leader/eta_X.X/run_Y/particles_frames.txt
#   results/circle_leader/eta_X.X/run_Y/particles_frames.txt

# ─────────────────── PARÁMETROS ──────────────────────────────────────────── #
N=400           # rho=4, L=10 → N = 4 * 10^2 = 400
L=10
M=5
RC=1.0
PERIODIC=true
ITERATIONS=500  # aumentar si el transitorio es largo
N_RUNS=3        # repeticiones por eta para barras de error

LEADER_ID=0

ETA_VALUES=(0.0 0.1 0.2 0.3 0.5 0.7 0.8 0.9 1.0 1.5 2.0 2.5 3.0 4.0 5.0)
# ─────────────────────────────────────────────────────────────────────────── #

ROOT_DIR="$(pwd)"          # /root
JAVA_DIR="$ROOT_DIR/java"
RESULTS_DIR="$ROOT_DIR/results"

echo "Compilando Java..."
cd "$JAVA_DIR"
javac *.java
if [ $? -ne 0 ]; then
    echo "Error de compilación. Abortando."
    exit 1
fi
echo "OK."
cd "$ROOT_DIR"

run_scenario() {
    local SCENARIO_NAME=$1   # no_leader | fixed_leader | circle_leader
    local HAS_LEADER=$2      # true | false
    local CIRCLE_LEADER=$3   # true | false

    echo ""
    echo "=============================="
    echo "  Escenario: $SCENARIO_NAME"
    echo "=============================="

    for ETA in "${ETA_VALUES[@]}"; do
        for RUN in $(seq 1 $N_RUNS); do

            OUT_DIR="$RESULTS_DIR/$SCENARIO_NAME/eta_$ETA/run_$RUN"
            mkdir -p "$OUT_DIR"

            # App escribe particles_frames.txt en ../ relativo a donde se ejecuta
            # → ejecutamos desde /java para que quede en /root/particles_frames.txt
            rm -f "$ROOT_DIR/particles_frames.txt"

            echo -n "  eta=$ETA  run=$RUN ... "
            cd "$JAVA_DIR"
            java App \
                $N $L $M $RC $PERIODIC \
                $ITERATIONS $ETA \
                $HAS_LEADER $LEADER_ID $CIRCLE_LEADER \
                > /dev/null 2>&1
            cd "$ROOT_DIR"

            if [ -f "particles_frames.txt" ]; then
                mv "particles_frames.txt" "$OUT_DIR/particles_frames.txt"
                echo "OK → $OUT_DIR"
            else
                echo "FALLA (no se generó particles_frames.txt)"
            fi

        done
    done
}

mkdir -p "$RESULTS_DIR"

# Escenario A: Sin líder
run_scenario "no_leader"     false false

# Escenario B: Líder dirección fija
run_scenario "fixed_leader"  true  false

# Escenario C: Líder circular
run_scenario "circle_leader" true  true

echo ""
echo "Todos los escenarios finalizados."
echo "Ahora corré:  python3 benchmark_comparison.py"

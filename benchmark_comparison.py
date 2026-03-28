"""
benchmark_comparison.py
========================
Ubicar en /root (misma altura que /java, visualize.py, plot_va.py, etc.)

Lee los resultados generados por run_all_scenarios.sh y produce:
  - va_vs_eta_comparison.png  → curva comparativa de los 3 escenarios (ítem c/d)

Estructura esperada de resultados:
  results/
    no_leader/eta_0.0/run_1/particles_frames.txt
    fixed_leader/eta_0.5/run_1/particles_frames.txt
    circle_leader/eta_1.0/run_1/particles_frames.txt
    ...
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import math

# ─────────────────────────── CONFIGURACIÓN ────────────────────────────────── #

ETA_VALUES  = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
N_RUNS      = 3
TRANSIENT   = 200

RESULTS_DIR = "results"

SCENARIOS = {
    "Sin líder":      "no_leader",
    "Líder fijo":     "fixed_leader",
    "Líder circular": "circle_leader",
}

STYLES = {
    "Sin líder":      {"color": "steelblue",  "marker": "o", "ls": "-"},
    "Líder fijo":     {"color": "darkorange", "marker": "s", "ls": "--"},
    "Líder circular": {"color": "seagreen",   "marker": "^", "ls": "-."},
}

# ──────────────────────────── FUNCIONES ───────────────────────────────────── #

def compute_va_series(filepath):
    va_list = []
    try:
        with open(filepath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    N = int(line)
                except ValueError:
                    continue

                f.readline()  # "Frame X"

                sum_vx, sum_vy = 0.0, 0.0
                v0 = None

                for _ in range(N):
                    parts = f.readline().strip().split()
                    if len(parts) < 5:
                        continue
                    vx, vy = float(parts[3]), float(parts[4])
                    sum_vx += vx
                    sum_vy += vy
                    if v0 is None:
                        s = math.sqrt(vx**2 + vy**2)
                        if s > 0:
                            v0 = s

                if N > 0 and v0:
                    va = math.sqrt(sum_vx**2 + sum_vy**2) / (N * v0)
                    va_list.append(va)

    except FileNotFoundError:
        pass
    return va_list


def steady_state(va_series, transient):
    ss = np.array(va_series[transient:])
    if ss.size == 0:
        return float('nan'), float('nan')
    return float(np.mean(ss)), float(np.std(ss))


def collect_scenario(folder, eta_values, n_runs, transient):
    etas, means, stds = [], [], []

    for eta in eta_values:
        print(f"    leyendo eta={eta}...", flush=True)
        run_means = []
        last_series = []

        for run in range(1, n_runs + 1):
            path = os.path.join(RESULTS_DIR, folder,
                                f"eta_{eta}", f"run_{run}",
                                "particles_frames.txt")
            series = compute_va_series(path)
            if not series:
                continue
            m, _ = steady_state(series, transient)
            if not math.isnan(m):
                run_means.append(m)
                last_series = series

        if not run_means:
            continue

        etas.append(eta)
        if len(run_means) == 1:
            _, s = steady_state(last_series, transient)
            means.append(run_means[0])
            stds.append(s)
        else:
            means.append(float(np.mean(run_means)))
            stds.append(float(np.std(run_means)))

    return np.array(etas), np.array(means), np.array(stds)


def plot_comparison(results, outfile="va_vs_eta_comparison.png"):
    fig, ax = plt.subplots(figsize=(10, 6))

    for label, (etas, means, stds) in results.items():
        if len(etas) == 0:
            print(f"  [WARN] Sin datos para '{label}'")
            continue
        st = STYLES[label]
        ax.errorbar(etas, means, yerr=stds*10,
                    label=label,
                    color=st["color"], marker=st["marker"], linestyle=st["ls"],
                    capsize=5, linewidth=1.8, markersize=6)

    ax.set_xlabel(r"$\eta$ (ruido)", fontsize=13)
    ax.set_ylabel(r"$v_a$ (polarización)", fontsize=13)
    ax.set_title(r"Parámetro de orden $v_a$ vs $\eta$ — Comparación de escenarios", fontsize=13)
    ax.set_xlim(-0.1, max(ETA_VALUES) + 0.2)
    ax.set_ylim(0.0, 1.05)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    fig.savefig(outfile, dpi=150)
    plt.close(fig)
    print(f"Gráfico guardado: {outfile}")


# ──────────────────────────────── MAIN ───────────────────────────────────────

def main():
    print("=" * 60)
    print("  BENCHMARK: Comparación va vs eta — 3 escenarios")
    print("=" * 60)

    results = {}

    for label, folder in SCENARIOS.items():
        print(f"\n[{label}]  carpeta: {folder}")
        etas, means, stds = collect_scenario(folder, ETA_VALUES, N_RUNS, TRANSIENT)
        results[label] = (etas, means, stds)
        for e, m, s in zip(etas, means, stds):
            print(f"  eta={e:.1f}  va={m:.4f} ± {s:.4f}")

    print("\nGenerando gráfico...")
    plot_comparison(results)
    print("Listo.")


if __name__ == "__main__":
    main()

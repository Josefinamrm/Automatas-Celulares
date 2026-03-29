import numpy as np
import matplotlib.pyplot as plt
import sys
import math

def read_frames(filepath):
    va_list = []
    try:
        with open(filepath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                try:
                    N = int(line.strip())
                except ValueError:
                    continue
                
                frame_label = f.readline().strip()
                
                sum_vx = 0.0
                sum_vy = 0.0
                v0 = 0.0
                
                for _ in range(N):
                    parts = f.readline().strip().split()
                    if len(parts) >= 6:
                        vx = float(parts[3])
                        vy = float(parts[4])
                        sum_vx += vx
                        sum_vy += vy
                        if v0 == 0.0:
                            v0 = math.sqrt(vx*vx + vy*vy)
                
                if N > 0 and v0 > 0:
                    va = math.sqrt(sum_vx**2 + sum_vy**2) / (N * v0)
                    va_list.append(va)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        sys.exit(1)
    return va_list

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <stationary_start_index>")
        sys.exit(1)

    stationary_start = int(sys.argv[1])

    filepath = 'particles_frames.txt'
    va_list = read_frames(filepath)

    if not va_list:
        print("No data.")
        sys.exit(1)

    if stationary_start >= len(va_list):
        print("Error: stationary index out of range.")
        sys.exit(1)

    # Promedio desde estacionario
    va_stationary = va_list[stationary_start:]
    mean_va = np.mean(va_stationary)

    print(f"Stationary starts at iteration: {stationary_start}")
    print(f"Mean v_a (stationary): {mean_va:.4f}")

    plt.figure(figsize=(10, 6))

    # Serie principal (adelante)
    plt.plot(range(len(va_list)), va_list, label='v_a', linewidth=1, zorder=2)

    # Línea vertical (opcional adelante también)
    plt.axvline(x=stationary_start, color='red', linestyle='--',
                label=f'Estacionario en t={stationary_start}', zorder=3)

    # Promedio (atrás)
    plt.axhline(mean_va, linestyle='--', linewidth=2,
                color='lightgreen',
                label=f'v_a promedio = {mean_va:.3f}',
                zorder=1)
    

    plt.xlabel('Tiempo')
    plt.ylabel('Polarización (v_a)')
    plt.title('Order Parameter vs Time')
    plt.grid(True)

    plt.ylim(0, 1)

    # Leyenda afuera del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar layout para que no se corte la leyenda
    plt.tight_layout()

    plt.savefig('va_vs_time.png', dpi=300, bbox_inches='tight')
    print("Saved plot to va_vs_time.png")

    plt.show()

if __name__ == "__main__":
    main()
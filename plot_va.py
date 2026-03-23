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
    filepath = 'particles_frames.txt'
    va_list = read_frames(filepath)

    if not va_list:
        print("No data.")
        sys.exit(1)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(va_list)), va_list, label='v_a', linewidth=1)
    plt.xlabel('Iterations')
    plt.ylabel('Order Parameter (v_a)')
    plt.title('Order Parameter vs Time')
    plt.grid(True)

    # Simple moving average to find when it stops growing/decreasing
    window_size = 50
    if len(va_list) > window_size:
        va_array = np.array(va_list)
        moving_avg = np.convolve(va_array, np.ones(window_size)/window_size, mode='valid')
        
        # Look at the derivative of the moving average
        deriv = np.diff(moving_avg)
        
        # Find when derivative magnitude becomes consistently small
        stab_idx = -1
        threshold = 0.001
        
        for i in range(len(deriv)):
            # Check if all subsequent derivatives are small
            if np.all(np.abs(deriv[i:i+100]) < threshold):
                stab_idx = i + window_size // 2
                break
                
        if stab_idx != -1:
            plt.axvline(x=stab_idx, color='r', linestyle='--', label=f'Stabilization ~ {stab_idx}')
            print(f"Stabilization detected at iteration {stab_idx}")
        else:
            print("Stabilization point not clearly found based on derivative.")
            
        # Plot moving average as well
        plt.plot(range(window_size-1, len(va_list)), moving_avg, color='orange', label='Moving Avg', linewidth=2)

    plt.legend()
    plt.savefig('va_vs_time.png', dpi=300)
    print("Saved plot to va_vs_time.png")

if __name__ == "__main__":
    main()

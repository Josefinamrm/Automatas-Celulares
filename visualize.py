import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

def read_frames(filepath):
    frames = []
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
                
                frame_data = []
                for _ in range(N):
                    parts = f.readline().strip().split()
                    if len(parts) >= 6:
                        pid = int(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        vx = float(parts[3])
                        vy = float(parts[4])
                        radius = float(parts[5])
                        is_leader = False
                        if len(parts) >= 7:
                            is_leader = bool(int(parts[6]))
                        frame_data.append([x, y, vx, vy, radius, 1 if is_leader else 0])
                if frame_data:
                    frames.append(np.array(frame_data))
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        sys.exit(1)
    return frames

filepath = 'particles_frames.txt'
frames = read_frames(filepath)
if not frames:
    print("No frames data found in", filepath)
    sys.exit(1)

fig, ax = plt.subplots(figsize=(8, 8))

# Estimate L from the data
max_x = max(np.max(f[:, 0]) for f in frames) if frames else 10
max_y = max(np.max(f[:, 1]) for f in frames) if frames else 10
L = max(max_x, max_y)
# Since positions can wrap around, L might be slightly larger than max_x, max_y. 
# We'll just add a little margin or round up to nearest 10 for safety if it's close.
# But 10 was the parameter used.
L = 10.0 

ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_aspect('equal')
ax.set_title("Off-Lattice Automata")

# Initialize with first frame to avoid length mismatch issues in matplotlib Quirver
init_data = frames[0]

colors = ['blue' if c == 1 else 'red' for c in init_data[:, 5]]
scatter = ax.scatter(init_data[:, 0], init_data[:, 1], s=30, color=colors, zorder=2)
quiver = ax.quiver(init_data[:, 0], init_data[:, 1], init_data[:, 2]*10, init_data[:, 3]*10, color='black', scale=1.0, scale_units='xy', angles='xy', headwidth=3, headlength=4, zorder=1)

def init():
    return scatter, quiver

def update(frame_idx):
    data = frames[frame_idx]
    x = data[:, 0]
    y = data[:, 1]
    vx = data[:, 2]
    vy = data[:, 3]
    is_leader = data[:, 5]
    
    offsets = np.c_[x, y]
    scatter.set_offsets(offsets)
    scatter.set_color(['blue' if c == 1 else 'red' for c in is_leader])
    quiver.set_offsets(offsets)
    # The arrow should have length proportional to velocity.
    # We multiply by a large factor just to make the arrows visible if velocity is small (0.03).
    quiver.set_UVC(vx*10, vy*10)
    
    ax.set_title(f"Time Step {frame_idx} (N={len(x)})")
    return scatter, quiver

ani = animation.FuncAnimation(fig, update, frames=len(frames), init_func=init, blit=True, interval=100)
plt.show()

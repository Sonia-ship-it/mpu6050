import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

PORT = 'COM11'
BAUD = 115200
ser = serial.Serial(PORT, BAUD, timeout=1)

WINDOW = 200
pitch_buf = deque(maxlen=WINDOW)
x_idx = deque(maxlen=WINDOW)

fig, ax = plt.subplots(figsize=(8, 4))
(line_pitch,) = ax.plot([], [], color='tab:blue', label='Pitch (°)')

ax.set_xlim(0, WINDOW)
ax.set_ylim(-90, 90)
ax.set_xlabel("Samples")
ax.set_ylabel("Pitch (°)")
ax.set_title("MPU6050 Real-Time Pitch Visualization")
ax.legend(loc='upper right')

def parse_line(line):
    try:
        pitch, roll, yaw = map(float, line.strip().split(','))
        return pitch
    except:
        return None

def init():
    line_pitch.set_data([], [])
    return (line_pitch,)

def update(frame):
    raw = ser.readline().decode(errors='ignore')
    pitch = parse_line(raw)
    if pitch is not None:
        pitch_buf.append(pitch)
        x_idx.append(len(x_idx) + 1 if x_idx else 1)
        ax.set_xlim(max(0, len(x_idx) - WINDOW), len(x_idx))
    line_pitch.set_data(range(len(pitch_buf)), list(pitch_buf))
    return (line_pitch,)

ani = animation.FuncAnimation(fig, update, init_func=init, interval=30, blit=True)
plt.tight_layout()
plt.show()

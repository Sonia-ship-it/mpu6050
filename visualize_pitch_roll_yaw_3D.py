import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

PORT = 'COM11'
BAUD = 115200
ser = serial.Serial(PORT, BAUD, timeout=1)

fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')

def rotation_matrix(pitch, roll, yaw):
    p, r, y = np.radians([pitch, roll, yaw])
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(p), -np.sin(p)],
                   [0, np.sin(p), np.cos(p)]])
    Ry = np.array([[np.cos(r), 0, np.sin(r)],
                   [0, 1, 0],
                   [-np.sin(r), 0, np.cos(r)]])
    Rz = np.array([[np.cos(y), -np.sin(y), 0],
                   [np.sin(y), np.cos(y), 0],
                   [0, 0, 1]])
    return Rz @ Ry @ Rx

verts = np.array([[-0.5, -0.5, 0],
                  [ 0.5, -0.5, 0],
                  [ 0.5,  0.5, 0],
                  [-0.5,  0.5, 0]])

def parse_line(line):
    try:
        return map(float, line.strip().split(','))
    except:
        return None, None, None

def update(frame):
    raw = ser.readline().decode(errors='ignore')
    pitch, roll, yaw = parse_line(raw)
    if pitch is None: return []

    R = rotation_matrix(pitch, roll, yaw)
    rotated = (R @ verts.T).T
    poly = [list(rotated)]

    ax.clear()
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.add_collection3d(Poly3DCollection(poly, color='lightgreen', alpha=0.8))
    ax.set_title(f"Pitch: {pitch:.1f}°, Roll: {roll:.1f}°, Yaw: {yaw:.1f}°")
    return []

ani = animation.FuncAnimation(fig, update, interval=50, blit=False)
plt.show()

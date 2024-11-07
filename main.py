from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors

# delta t and timestep 
dt = 0.01
n_steps = 3000

# arrays to store data traces
xs = np.empty(n_steps + 1, dtype="float64")
ys = np.empty(n_steps + 1, dtype="float64")
zs = np.empty(n_steps + 1, dtype="float64")

# initial condition
xs[0], ys[0], zs[0] = (0., 1., 1.05)

# calculate lorenz equation
def lorenz(x, y, z, s=10, r=28, b=8/3):
    dot_x = s * (y - x)
    dot_y = r * x - y - x * z
    dot_z = x * y - b * z
    return dot_x, dot_y, dot_z

# main loop
for i in range(n_steps):
    dot_x, dot_y, dot_z = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + (dot_x * dt)
    ys[i + 1] = ys[i] + (dot_y * dt)
    zs[i + 1] = zs[i] + (dot_z * dt)

# set color map
cmap = plt.cm.viridis
norm = colors.Normalize(0, n_steps)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# set axis limits
ax.set_xlim([-20, 20])
ax.set_ylim([-30, 30])
ax.set_zlim([0, 60])

# Add axis labels and title
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('Lorenz System')

#!ignore! plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0) 

# initialize animation
lines = [ax.plot([], [], [], color=cmap(norm(i)), lw=0.5)[0] for i in range(n_steps)]
point = ax.scatter([], [], [], color='green', s=10)  
time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

def init():
    for line in lines:
        line.set_data([], [])
        line.set_3d_properties([])
    point._offsets3d = ([], [], [])  # initialize
    time_text.set_text('')
    return lines + [time_text, point]

def animate(i):
    # update each segment
    lines[i].set_data(xs[i:i+2], ys[i:i+2])
    lines[i].set_3d_properties(zs[i:i+2])
    
    # Update coordinate values of the moving point
    point._offsets3d = (xs[i:i+1], ys[i:i+1], zs[i:i+1])
    
    # show time and coordinate values
    time_text.set_position((0.85, 0.85))
    time_text.set_text(f't: {i * dt:.2f}\n\n'
                        f'x: {xs[i]:.2f}\n'
                        f'y: {ys[i]:.2f}\n'
                        f'z: {zs[i]:.2f}')
    
    return lines + [time_text, point]

ani = FuncAnimation(fig, animate, frames=n_steps, init_func=init, interval=10, blit=True)

# save animation
ani.save('lorenz_solutions.gif', writer="imagemagick", dpi=100, fps=30)

plt.show()
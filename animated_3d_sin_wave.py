'''
Plots a 3D sin wave with a uniform colormap applied to z-axis values.
The plot is rotated over time and the view elevation oscillates in a
smooth sine wave. Default settings are mostly for aesthetic reasons.
This will most likely run too slowly to view well without saving or
increasing the mesh_granularity.
'''

########### SETTINGS ###########
lim = -1 # Frame limit, -1 = unlimited
location = "./rotating_sin_wave.mp4"
save = False
x_min,x_max=-99,100 # range of graph axes, having 2 center points in each x/y plane ensures center appears smooth vs comes to a single point
y_min,y_max=-99,100
z_min,z_max=-2.0,2.0 # For A E S T H E T I C S
mesh_granularity = 1 # Step size over range
graph_granularity = 1 # Step size over *elements* of x,y grid arrays
legend = False # Display a colorbar corresponding to the color mapping in the z-axis
axes = False # Show axes in animation
resolution = 1080 # set as height dimension for 16:9 w:h aspect ratio, e.g. 360=360p=640x360, 720=720p=1280x720, 1080=1080p=1920x1080... etc
fps = 60.0 # Frames per second when saving as video
################################

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.animation as animation

if(lim == -1): # Videos need limited size...
    save = False

# Figure/plot handles
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.set_dpi(resolution/fig.get_figheight())
fig.set_figwidth((16/9)*fig.get_figheight())

# Data points
X = np.arange(x_min, x_max, mesh_granularity)
Y = np.arange(y_min, y_max, mesh_granularity)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot initializing and settings
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, rstride=graph_granularity, cstride=graph_granularity,
                       linewidth=0, antialiased=save)

# Add a color bar which maps values to colors.
if(legend == True):
    fig.colorbar(surf, shrink=0.5, aspect=5)

# Axes/3D settings
ax.set_zlim(z_min, z_max)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
if(not axes): # Hiding axes is more aesthetic
    ax.set_axis_off()
plt.subplots_adjust(left=0, bottom=0, right=1, top=1,
                    wspace=0, hspace=0)
init_elev = 45 # Degrees; initial view elevation in 3D space; this value is used to adjust elevation throughout the animation
ax.view_init(elev=init_elev, azim=0) # Set inital view elevation; this is animated

def data_gen(t=0):# Make data.
    while (lim == -1 or t<lim):
        t+=1
        if(save and t%np.floor((lim/20))==0):
            print(str(int(100*t/lim))+"%... t="+str(t))
        yield np.divide(np.sin(R/(3*np.pi)+((360-t%360)/180)*np.pi-1), 5),(t%360)

def run(data):
    # Plot the surface.
    Z,angle = data
    for c in ax.collections:
        c.remove()
        del c
    del ax.collections[:]
    surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, rstride=graph_granularity, cstride=graph_granularity,
                           linewidth=0, antialiased=save)
    ax.view_init(elev=init_elev+10*np.sin(angle*np.pi/180), azim=angle/2)

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=1, repeat=(not save))

if(save): # Save video
    Writer = animation.writers['ffmpeg']
    b,h=fig.get_size_inches()
    dpi=(resolution/h)
    writer = Writer(fps=fps)
    ani.save_count = lim # Override limit on saved frames
    ani.save(location, dpi=dpi, writer=writer)
    exit()
else: # Show plot
    plt.show()

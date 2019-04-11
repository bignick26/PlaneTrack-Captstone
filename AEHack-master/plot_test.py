import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig=plt.figure()
ax=fig.add_axes([.1,.1,.8,.8],polar=True) # This is the background axis

# variables for the background plot. I use some random numbers just for
# illustration purposes
N = 150
r = (1 - 0.8) * np.random.random_sample(N) +0.8
theta = 2*np.pi*np.random.random(N)
area = 200*r**2*np.random.random(N)

ax.scatter(theta, r, c=theta, s=area, cmap='hsv')

plt.setp(ax.get_xticklabels(),visible=False)
plt.setp(ax.get_yticklabels(),visible=False)
ax.patch.set_visible(False)
ax.grid(False)
ax.axis('off')

ax2=fig.add_axes([.3,.3,.4,.4])
m = Basemap(projection='ortho',lon_0=-105,lat_0=-25,resolution='l',ax=ax2)
m.bluemarble(scale=.1) # scale=.1 for low resolution

input("Press Enter to continue...")
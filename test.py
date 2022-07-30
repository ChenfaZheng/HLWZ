import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
mpl.use('TkAgg')


x = np.linspace(0, 100, 100)
y = np.sin(x)

rainbow = cm.get_cmap('rainbow')

colors = rainbow(x)

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.vlines(x, ymin=0, ymax=1, colors=colors, cmap=rainbow)
fig.colorbar(cax)

plt.show()
plt.close()
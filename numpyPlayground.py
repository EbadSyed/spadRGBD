import numpy as np

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)

tanTheta = 0.4434

a = 20
a1 = np.full((50, 50),113)

area = int(a * tanTheta)

if area%2 != 0:
    area = area + 1

diff = int((50 - area)/2)

print(area)

for x in range(area):
    for y in range(area):
        a1[x+diff,y+diff] = a



plt.imshow(a1)
plt.colorbar(fraction=0.1, pad=0.04)
plt.show()

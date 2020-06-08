import matplotlib.pyplot as plt
import numpy as np
from math import degrees, atan

x = np.array(range(-10, 10))
m1 = 0
m2 = 1
y1 = m1*x
y2 = m2*x

angle = degrees(atan((m2-m1)/(1+m1*m2)))

print(angle)

plt.plot(x, y1, label='long')
plt.plot(x, y2, label='short')

plt.show()
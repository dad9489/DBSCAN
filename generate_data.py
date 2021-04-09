import matplotlib.pyplot as plt
import numpy as np

t = np.arange(10)

# plt.plot(t, np.sin(t))

plt.title('matplotlib.pyplot.ginput()\
 function Example', fontweight="bold")

n = 9
print(f"After {n} clicks :")
x = plt.ginput(n)
x = [list(x) for x in x]
print(x)

plt.show()
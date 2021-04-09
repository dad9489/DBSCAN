import matplotlib.pyplot as plt
import numpy as np

t = np.arange(10)

n = 100
plt.title(f'Creating distribution with n={n} points. Click to place a point.', fontweight="bold")

print(f"After {n} clicks :")
x = plt.ginput(n)
x = [list(x) for x in x]
print(x)

plt.show()

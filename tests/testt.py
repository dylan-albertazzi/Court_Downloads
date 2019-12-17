import numpy as np

a = np.arange(20).reshape(20, 1)
#print(a)

for i in range(np.size(a, 0)):
    print(a[0, :])
    print("\n")
    a = np.delete(a,0, 0)

print(a)
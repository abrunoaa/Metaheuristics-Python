import sys
import matplotlib.pyplot as plt
plt.xlabel("Iteração")
plt.ylabel("Solução")
plt.plot()
plt.grid()
plt.savefig(sys.stdout.buffer)

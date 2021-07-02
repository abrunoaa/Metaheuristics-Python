import matplotlib.pyplot as plt

from perf import perf


sa = [784, 661, 742, 778, 800.6, 669, 949, 730, 823.05, 832.7]
sa_2opt = [784, 661, 742, 778, 802.8, 669, 949, 730, 822.8, 832.5]
ga = [784, 661, 742.9, 778.1, 809.5, 669, 949.1, 730, 823.7, 834.7]
ga_2opt = [784, 661, 742.6, 778, 806.2, 669, 949.4, 730, 822.3, 833.1]

t = [list(p) for p in zip(sa, sa_2opt, ga, ga_2opt)]

plt.figure()
perf(t, s_label=['SA', 'SA + 2-opt', 'GA', 'GA + 2-opt'])

plt.yticks([x / 10 for x in range(11)])
plt.title('Performance profile')
plt.xlabel('\u03C4')
plt.ylabel('P(r(p, s))')
plt.legend()
plt.grid()
plt.show()

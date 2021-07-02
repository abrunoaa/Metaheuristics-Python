import matplotlib.pyplot as plt
from math import isnan


def stairs(x, y):
  assert len(x) == len(y)
  xs, ys = [], []
  for i in range(len(x)):
    xs += [x[i], x[i]]
    ys += [y[i], y[i]]
  return xs[1:], ys[:-1]


# Adapted from:
#   Benchmarking optimization software with performance profiles,
#   E.D. Dolan and J.J. More',
#   Mathematical Programming, 91 (2002), 201--213.
# See: https://www.mcs.anl.gov/~more/cops/
def perf(t, s_label=None):
  if not t:
    return

  colors  = ['m', 'b', 'r', 'g', 'c', 'k', 'y']
  lines   = [':', '-', '-.', '--']
  markers = ['x', '*', 's', 'd', 'v', '^', 'o']

  np, ns = len(t), len(t[0])
  assert all(len(row) == ns for row in t), 'It is expected a square matrix'

  # ratios
  r = []
  for row in t:
    r.append([x / min(row) for x in row])
  max_ratio = max(map(max, r))

  for i in range(np):
    r[i] = [2 * max_ratio if isnan(x) else x for x in r[i]]

  # sort columns
  r = [list(x) for x in [*zip(*r)]]  # transpose r
  for row in r:
    row.sort()

  for s in range(ns):
    xs, ys = stairs(r[s], [x / np for x in range(1, np + 1)])
    xs = xs + [2 * max_ratio]
    ys = ys + [1]
    lb = None if s_label is None else s_label[s]
    plt.plot(xs, ys, color=colors[s], marker=markers[s], markersize=5, linestyle=lines[s], label=lb)

  plt.axis((1, max_ratio, 0, 1))

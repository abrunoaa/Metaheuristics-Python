import cython
from libc.stdlib cimport malloc, free

from logging import info


cdef long c_two_opt(unsigned n, unsigned* tour, distance):
  # declarations
  cdef unsigned* dist = <unsigned*>malloc(n * cython.sizeof(int))

  cdef long improve = 0
  cdef long best, reduce
  cdef unsigned left = 0, right = 0
  cdef unsigned a, b, c, d, tmp

  # execution
  while True:
    for i in range(n):
      dist[i] = distance(tour[i - 1], tour[i])
    best = 0
    for i in range(-1, n - 3):
      a = tour[i]
      b = tour[i + 1]
      for j in range(i + 2, n - 1):
        c = tour[j]
        d = tour[j + 1]
        reduce = dist[i + 1] + dist[j + 1] - distance(a, c) - distance(b, d)
        if reduce > best:
          best = reduce
          left = i + 1
          right = j

    if best == 0:
      free(dist)
      return improve

    assert left < right
    improve += best
    while left < right:
      tmp = tour[left]
      tour[left] = tour[right]
      tour[right] = tmp
      left += 1
      right -= 1

    assert tour[-1] == 0

cpdef two_opt(tour, distance):
  info("Running 2-opt in C")

  # validations
  assert isinstance(tour, list), "'tour' must be a list"
  assert callable(distance), "'distance' must be a function"
  if tour is None or len(tour) <= 2:
    return 0, tour
  assert len(set(tour)) == len(tour), "Duplicates found in tour"
  assert tour[-1] == 0, "Expected depot at end of tour, found {}".format(tour[-1])

  cdef unsigned n = len(tour)
  cdef unsigned* c_tour = <unsigned*>malloc(n * cython.sizeof(int))
  for i in range(n):
    c_tour[i] = tour[i]

  improve = c_two_opt(n, c_tour, distance)

  for i in range(n):
    tour[i] = c_tour[i]

  free(c_tour)
  return improve, tour

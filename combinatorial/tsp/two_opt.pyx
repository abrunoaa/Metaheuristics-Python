import cython
from libc.stdlib cimport malloc, free

from logging import info


cpdef two_opt(tour, distance):
  info("Running 2-opt in C")

  # validations
  assert isinstance(tour, list), "'tour' must be a list"
  assert callable(distance), "'distance' must be a function"
  if tour is None or len(tour) < 2:
    return 0, [0]
  assert len(set(tour)) == len(tour), "Duplicates found in tour"
  assert tour[-1] == 0, "Expected depot at end of tour, found {}".format(tour[-1])

  # declarations
  cdef int n = len(tour)
  cdef unsigned* c_tour = <unsigned*>malloc(len(tour) * cython.sizeof(int))

  cdef long improve = 0
  cdef long best, reduce
  cdef unsigned left = 0, right = 0
  cdef unsigned a, b, c, d, tmp

  # convert to C
  for i in range(n):
    c_tour[i] = tour[i]

  # remaining code
  while True:
    best = 0
    for i in range(-1, n - 3):
      a = c_tour[i]
      b = c_tour[i + 1]
      for j in range(i + 2, n - 1):
        c = c_tour[j]
        d = c_tour[j + 1]
        reduce = distance(a, b) + distance(c, d) - distance(a, c) - distance(b, d)
        if reduce > best:
          best = reduce
          left = i + 1
          right = j

    if best == 0:
      assert set(tour) == set([u for u in c_tour[: n]])
      tour = [u for u in c_tour[: n]]
      free(c_tour)
      return int(improve), tour

    assert left < right
    improve += best
    while left < right:
      tmp = c_tour[left]
      c_tour[left] = c_tour[right]
      c_tour[right] = tmp
      left += 1
      right -= 1

    assert c_tour[-1] == 0
    assert len(set([u for u in c_tour[: n]])) == n

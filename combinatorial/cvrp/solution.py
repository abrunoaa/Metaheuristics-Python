from logging import info
from random import randrange, shuffle

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.solution import Solution as Base
from combinatorial.tsp.two_opt import two_opt as tsp_two_opt
from container.min_queue import MinQueue


class Solution(Base):
  def __init__(self, cvrp: Cvrp, tour = None):
    info("Initializing solution: {} tour".format("Generating" if tour is None else "Received"))
    if tour is None:
      tour = [i for i in range(1, cvrp.number_of_clients + 1)]
      shuffle(tour)
    assert cvrp is not None, "Invalid cvrp instance 'None'"
    assert isinstance(cvrp, Cvrp), "Invalid cvrp instance of '{}'".format(type(cvrp).__name__)
    assert min(tour) >= 1, "Invalid node: '{}' < 1".format(min(tour))
    assert max(tour) <= cvrp.number_of_clients, "Invalid node: '{}' > {}".format(max(tour), cvrp.number_of_clients)
    assert len(set(tour)) == cvrp.number_of_clients, "Duplicates found in tour"
    self.cvrp = cvrp
    self.tour = tour
    self.fitness = None
    self.truck = None
    self.optimal_split()

  def get_fitness(self):
    return self.fitness

  def get_tour(self):
    return [self.tour[i: j + 1] for i, j in self.truck_ranges()]

  def neighbor(self):
    i = randrange(0, self.cvrp.number_of_clients - 1)
    j = randrange(i + 2, self.cvrp.number_of_clients + 1)
    return Solution(self.cvrp, self.tour[:i] + self.tour[i: j][::-1] + self.tour[j:])

  def local_search(self):
    self.two_opt()
    self.validate()

  def optimal_split(self):
    """
    Given a TSP-like solution, calculates the optimal positions for splitting into trucks.
    Used for building fitness and truck list of current solution, given a valid tour.
    :return: None
    """
    info("Starting optimal split calculation")
    cvrp = self.cvrp
    tour = self.tour
    dist = cvrp.distance
    n = cvrp.number_of_clients

    distances = [dist(tour[i], tour[i + 1]) for i in range(n - 1)]
    split = [dist(tour[i], 0) + dist(0, tour[i + 1]) - distances[i] for i in range(n - 1)]
    path = [None] * n
    used = 0
    best = None
    i = 0
    queue = MinQueue()
    queue.push((0, -1))
    for j in range(n):
      used += cvrp.demand[tour[j]]
      while used > cvrp.capacity:
        used -= cvrp.demand[tour[i]]
        i += 1
        queue.pop()

      assert i <= j
      best, path[j] = queue.min()
      if j < n - 1:
        queue.push((split[j] + best, j))

    self.fitness = best + dist(0, tour[0]) + sum(distances) + dist(tour[-1], 0)
    self.truck = []
    v = n - 1
    while v != -1:
      self.truck.append(v)
      v = path[v]
    self.truck = self.truck[::-1]
    self.validate()

  def calculate_fitness(self):
    """
    Calculate the expected value of fitness of current tour. Used just for checking.
    :return: Total length of tour.
    """
    tour = self.tour
    dist = self.cvrp.distance
    return sum(dist(0, tour[i]) + sum(dist(tour[k], tour[k + 1]) for k in range(i, j)) + dist(tour[j], 0)
               for i, j in self.truck_ranges())

  def truck_ranges(self):
    """
    Build truck ranges for easy manipulation.
    :return: A zip with starting and ending nodes position for each truck.
    """
    return zip([0] + [x + 1 for x in self.truck[: -1]], [x for x in self.truck])

  def two_opt(self):
    """
    Run 2-opt adaptation from TSP to CVRP.
    It's guaranteed that there is no pair which exchange will improve fitness cost.
    :return: None.
    """
    cvrp = self.cvrp
    tour = self.tour
    truck = self.truck
    distance = cvrp.distance

    # split tour to small TSP and optimize
    split_tour = [tour[i: j + 1] + [0] for i, j in self.truck_ranges()]
    for i in range(len(split_tour)):
      improve, split_tour[i] = tsp_two_opt(split_tour[i], distance)
      self.fitness -= improve

    # exchange routes to be 2-opt
    while True:
      load = [sum(cvrp.demand[u] for u in st) for st in split_tour]
      ntour = len(split_tour)
      best = 0
      t1 = t2 = p1 = p2 = op_type = None

      # search for best point
      for p in range(ntour):
        used_p = 0
        for i in range(len(split_tour[p])):
          a = split_tour[p][i - 1]
          b = split_tour[p][i]

          for q in range(p + 1, ntour):
            # combine first half with first half
            used_q = 0
            for j in range(len(split_tour[q])):
              if (load[p] - used_p) + (load[q] - used_q) <= cvrp.capacity:
                c = split_tour[q][j - 1]
                d = split_tour[q][j]
                reduce = distance(a, b) + distance(c, d) - distance(a, c) - distance(d, b)
                if reduce > best:
                  best = reduce
                  t1, t2 = p, q
                  p1, p2 = i, j
                  op_type = 1
              used_q += cvrp.demand[split_tour[q][j]]
              if used_p + used_q > cvrp.capacity:
                break

            # combine first half with second half
            used_q = 0
            for j in range(len(split_tour[q])):
              if used_p + (load[q] - used_q) <= cvrp.capacity:
                c = split_tour[q][j - 1]
                d = split_tour[q][j]
                reduce = distance(a, b) + distance(c, d) - distance(a, d) - distance(c, b)
                if reduce > best:
                  best = reduce
                  t1, t2 = p, q
                  p1, p2 = i, j
                  op_type = 2
              used_q += cvrp.demand[split_tour[q][j]]
              if (load[p] - used_p) + used_q > cvrp.capacity:
                break

          used_p += cvrp.demand[b]

      if best == 0:
        break
      info("Found optimization of type {}".format(op_type))
      self.fitness -= best
      r1 = split_tour[t1]
      r2 = split_tour[t2]
      st = r1 + r2
      if op_type == 1:
        split_tour[t1], split_tour[t2] = r1[: p1] + r2[: p2][::-1] + [0], r1[p1: -1][::-1] + r2[p2:]
      else:
        split_tour[t1], split_tour[t2] = r1[: p1] + r2[p2:], r2[: p2] + r1[p1:]
      assert split_tour[t1][-1] == 0
      assert split_tour[t2][-1] == 0
      assert sorted(st) == sorted(split_tour[t1] + split_tour[t2])

      improve, split_tour[t1] = tsp_two_opt(split_tour[t1], distance)
      self.fitness -= improve
      improve, split_tour[t2] = tsp_two_opt(split_tour[t2], distance)
      self.fitness -= improve

    tour.clear()
    truck.clear()
    for t in split_tour:
      if len(t) != 1:
        tour += t[: -1]
        truck.append(len(tour) - 1)

  # noinspection PyUnreachableCode
  def validate(self):
    """
    Checks if current state of solution is valid.
    :return: None
    """
    if __debug__:
      info("Validating current solution")
      cvrp = self.cvrp
      tour = self.tour
      truck = self.truck

      assert cvrp is not None
      assert self.fitness is not None
      assert tour is not None
      assert truck is not None
      assert len(set(tour)) == cvrp.number_of_clients, "Duplicates found in tour"
      assert truck[-1] == cvrp.number_of_clients - 1, "Last truck must be the last node on tour"
      assert self.fitness == self.calculate_fitness(), "Invalid fitness for current tour"

      heaviest = max(sum(cvrp.demand[u] for u in tour[i: j + 1]) for i, j in self.truck_ranges())
      assert heaviest <= cvrp.capacity, "Truck has load = {}, while capacity = {}".format(heaviest, cvrp.capacity)

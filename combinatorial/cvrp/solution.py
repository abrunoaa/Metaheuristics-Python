#  solution.py
#
#  Copyright (c) 2020 Bruno Almeda de Oliveira <abrunoaa@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

from logging import info
from random import randrange, shuffle

from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.solution import Solution as Base
from combinatorial.cvrp.two_opt import two_opt
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
    improve, self.tour, self.truck = two_opt(self.tour, self.truck, self.cvrp.demand, self.cvrp.capacity, self.cvrp.distance)
    self.fitness -= improve
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

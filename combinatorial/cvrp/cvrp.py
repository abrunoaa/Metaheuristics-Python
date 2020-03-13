from logging import info
from math import sqrt


class Cvrp:
  def __init__(self, number_of_clients, capacity, demand, locations):
    assert number_of_clients >= 2, "number of clients = {} < 2".format(number_of_clients)
    assert len(locations) == number_of_clients + 1, "Missing node location"
    assert len(demand) == number_of_clients + 1, "Missing demand"
    assert min(demand[1:]) > 0, "Client has demand = {}!".format(min(demand))
    assert max(demand) <= capacity, "Found demand ({}) > capacity ({})".format(max(demand), capacity)
    assert demand[0] == 0, "Depot must have demand = 0, but was {}".format(demand[0])
    self.number_of_clients = number_of_clients
    self.capacity = capacity
    self.demand = demand
    self.locations = locations

  def distance(self, u, v):
    diff = lambda i: self.locations[u][i] - self.locations[v][i]
    a = diff(0)
    b = diff(1)
    return int(sqrt(a * a + b * b) + 0.5)

  @staticmethod
  def read(filename):
    info("Started to read instance {}".format(filename))
    with open(filename) as file:
      content = [x.strip().split() for x in file.readlines()]

    c = content.index(["NODE_COORD_SECTION"])
    d = content.index(["DEMAND_SECTION"])

    number_of_clients = next(int(x[2]) - 1 for x in content if x[0] == "DIMENSION")
    capacity = next(int(x[2]) for x in content if x[0] == "CAPACITY")
    demand = [int(x[1]) for x in content[d + 1: d + number_of_clients + 2]]
    locations = [(int(x[1]), int(x[2])) for x in content[c + 1: c + number_of_clients + 2]]

    return Cvrp(number_of_clients, capacity, demand, locations)

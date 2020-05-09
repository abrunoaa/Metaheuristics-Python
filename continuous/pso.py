#  pso.py
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

from copy import copy
from random import uniform, random


class Particle:
  def __init__(self, f, interval):
    dimensions = len(interval)
    self.v = [uniform(interval[i][0], interval[i][1]) for i in range(dimensions)]
    self.x = [uniform(interval[i][0], interval[i][1]) for i in range(dimensions)]
    self.fitness = f(self.x)
    self.best = copy(self.x)
    self.best_fitness = self.fitness

  def move(self, w, c1, c2, gbest, f):
    assert 0 <= w < 1
    for i in range(len(self.v)):
      self.v[i] = w * self.v[i] + c1 * random() * (self.best[i] - self.x[i]) + c2 * random() * (gbest[i] - self.x[i])
      self.x[i] += self.v[i]
    self.fitness = f(self.x)

    if self.fitness < self.best_fitness:
      self.best_fitness = self.fitness
      self.best = copy(self.x)
      return True
    return False


def pso(f, interval, w, c1, c2, n_particles, iterations):
  particle = [Particle(f, interval) for _ in range(n_particles)]
  gbest = particle[0].best
  gbest_fitness = particle[0].best_fitness
  for i in range(1, n_particles):
    if particle[i].best_fitness < gbest_fitness:
      gbest = particle[i].best
      gbest_fitness = particle[i].fitness

  for _ in range(iterations):
    for i in range(n_particles):
      if particle[i].move(w, c1, c2, gbest, f):
        if particle[i].best_fitness < gbest_fitness:
          gbest = particle[i].best
          gbest_fitness = particle[i].best_fitness

  return gbest_fitness, gbest

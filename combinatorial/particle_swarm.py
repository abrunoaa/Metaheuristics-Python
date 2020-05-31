#  particle_swarm.py
#
#  Copyright (c) 2020 Bruno Almêda de Oliveira <abrunoaa@gmail.com>
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
#
from copy import deepcopy

from combinatorial.metaheuristic import MetaheuristicPopulationBased


# TODO: add type hint
# TODO: add docs
class ParticleSwarm(MetaheuristicPopulationBased):

  @staticmethod
  def build(w, c1, c2, stopping_condition):
    return ParticleSwarm((w, c1, c2, stopping_condition))

  def __init__(self, args):
    self.__w = args[0]
    self.__c1 = args[1]
    self.__c2 = args[2]
    self.__stopping_condition = args[-1]

  def execute(self, particles):
    gbest = min(particles, key=lambda particle: particle.get_fitness())

    self.__stopping_condition.start()
    while not self.__stopping_condition:
      improved = False
      for p in particles:
        p.move(gbest, self.__w, self.__c1, self.__c2)
        p.local_search()
        if p.get_fitness() < gbest.get_fitness():
          gbest = deepcopy(p)
          improved = True

      self.__stopping_condition.update(improved)

    return gbest

#  run.py
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
import sys
from argparse import ArgumentParser, FileType, ArgumentTypeError
from copy import deepcopy
from time import process_time as time
from typing import Callable

from combinatorial.ant_colony import AntColonyOptimization
from combinatorial.crp.crp import Crp
from combinatorial.crp.crp_solution import CrpSolution
from combinatorial.cvrp.cvrp import Cvrp
from combinatorial.cvrp.cvrp_ant import CvrpAnt
from combinatorial.cvrp.cvrp_chromosome import CvrpChromosome
from combinatorial.cvrp.cvrp_particle import CvrpParticle
from combinatorial.cvrp.cvrp_solution import CvrpSolution
from combinatorial.genetic_algorithm import GeneticAlgorithm
from combinatorial.instance import Instance
from combinatorial.metaheuristic import Metaheuristic
from combinatorial.particle_swarm import ParticleSwarm
from combinatorial.simulated_annealing import SimulatedAnnealing
from combinatorial.tsp.tsp import Tsp
from combinatorial.tsp.tsp_ant import TspAnt
from combinatorial.tsp.tsp_chromosome import TspChromosome
from combinatorial.tsp.tsp_solution import TspSolution
from stopping.max_no_improve import MaxNoImprove
from stopping.time_limit import TimeLimit

INSTANCE_TYPES = {'CRP': Crp, 'CVRP': Cvrp, 'TSP': Tsp}

SINGLE_SOLUTION = {'SA'}

SOLUTION_TYPES = {
  ('ACO', 'CRP'): None, ('ACO', 'CVRP'): CvrpAnt, ('ACO', 'TSP'): TspAnt,
  ('SA', 'CRP'): CrpSolution, ('SA', 'CVRP'): CvrpSolution, ('SA', 'TSP'): TspSolution,
  ('GA', 'CRP'): None, ('GA', 'CVRP'): CvrpChromosome, ('GA', 'TSP'): TspChromosome,
  ('PSO', 'CRP'): None, ('PSO', 'CVRP'): CvrpParticle, ('PSO', 'TSP'): None,
}


def extract_param(params):
  parameters = {}
  for var in params.split(','):
    p = var.split('=')
    if len(p) != 2:
      raise ArgumentTypeError("expected exactly two values per variable: {}".format(var))
    try:
      exec('{} = {}'.format(p[0], float(p[1])), {}, parameters)
    except ValueError:
      raise ArgumentTypeError("invalid number: {}".format(var))
    except SyntaxError:
      raise ArgumentTypeError("invalid variable: {}".format(var))

  return parameters


def read_instance(io, problem):
  return INSTANCE_TYPES[problem].read(io)


def build_algorithm(algorithm, n):
  if algorithm == 'ACO':
    pheromone = AntColonyOptimization.default_pheromone(n)
    return AntColonyOptimization.build(pheromone, alpha=1, beta=10, rho=0.5, stopping_condition=MaxNoImprove(10))

  if algorithm == 'GA':
    return GeneticAlgorithm.build(crossover=.9, elitism=.9, mutation=.9, stopping_condition=MaxNoImprove(100))

  if algorithm == 'SA':
    return SimulatedAnnealing.build(1000000, 1, .999, TimeLimit(120))

  if algorithm == 'PSO':
    return ParticleSwarm.build(w=.5, c1=.2, c2=.3, stopping_condition=MaxNoImprove(10))

  raise ArgumentTypeError("invalid algorithm: {}".format(algorithm))


def build_solution_builder(algorithm, problem):
  if SOLUTION_TYPES[algorithm, problem] is None:
    raise NotImplementedError("{} wasn't implemented with {}".format(problem, algorithm))

  if algorithm in SINGLE_SOLUTION:
    return SOLUTION_TYPES[algorithm, problem]

  # FIXME: currently doesn't read pop_size from command line
  pop_size = 20
  return lambda inst: [SOLUTION_TYPES[algorithm, problem](inst) for _ in range(pop_size)]


def parse_args():
  parser = ArgumentParser()
  parser.add_argument("problem", type=str.upper, help="problem to solve", choices=['CRP', 'CVRP', 'TSP'])
  parser.add_argument("algorithm", type=str.upper, help="algorithm to use", choices=['ACO', 'GA', 'PSO', 'SA'])
  # FIXME: the parameters are ignored
  parser.add_argument("-p", "--params", type=extract_param, help="parameters for the algorithm (ignored!)")
  # FIXME: the algorithms currently reads from stdin
  parser.add_argument("-i", "--input", type=FileType('r'), default=sys.stdin, help="file to read instance")
  # FIXME: the output file is ignored
  parser.add_argument("-o", "--output", type=FileType('w'), default=sys.stdout, help="file to write results")
  parser.add_argument("-r", "--repeat", type=int, help="number of times to execute")

  args = parser.parse_args()

  if args.repeat is None:
    args.repeat = 1

  instance = read_instance(args.input, args.problem)
  n = instance.get_n() + 1 if args.problem == 'CVRP' else instance.get_n()

  mh = build_algorithm(args.algorithm, n)
  solution_builder = build_solution_builder(args.algorithm, args.problem)

  return instance, mh, solution_builder, args.repeat


def run(instance: Instance, metaheuristic: Metaheuristic, solution_builder: Callable, number_of_tests: int):
  """
  Run several tests on an instance with a specific metaheuristic.

  :param instance: Instance to test.
  :param metaheuristic: Metaheuristic to execute.
  :param solution_builder: Creates a new solution. This must be callable and receive the instance as argument.
  :param number_of_tests: Number of times to repeat the test.
  :return: A tuple with the results with the time they spent.
  """
  if number_of_tests < 1:
    raise ValueError("Invalid number of tests: {}".format(number_of_tests))

  for mh in (deepcopy(metaheuristic) for _ in range(number_of_tests)):
    start = time()
    ans = mh.execute(solution_builder(instance))
    end = time()
    elapsed = end - start
    yield ans, elapsed


def run_and_print(instance: Instance, metaheuristic: Metaheuristic, solution_builder: Callable, number_of_tests: int):
  avg_answer = 0
  avg_time = 0
  best, worst = float("inf"), float("-inf")

  print('elapsed;fitness;solution')
  for ans, elapsed in run(instance, metaheuristic, solution_builder, number_of_tests):
    if isinstance(ans.get_fitness(), int):
      print('{:.2f}s;{};{}'.format(elapsed, ans.get_fitness(), ans.get_solution()), flush=True)
    else:
      print('{:.2f}s;{:.2f};{}'.format(elapsed, ans.get_fitness(), ans.get_solution()), flush=True)

    best = min(best, ans.get_fitness())
    worst = max(worst, ans.get_fitness())
    avg_answer += ans.get_fitness()
    avg_time += elapsed
  avg_time /= number_of_tests
  avg_answer /= number_of_tests

  print('')
  print('avg_time;avg_ans;best;worst')
  if isinstance(best, int):
    print('{:.2f}s;{:.2f};{};{}'.format(avg_time, avg_answer, best, worst), flush=True)
  else:
    print('{:.2f}s;{:.2f};{:.2f};{:.2f}'.format(avg_time, avg_answer, best, worst), flush=True)


if __name__ == '__main__':
  run_and_print(*parse_args())

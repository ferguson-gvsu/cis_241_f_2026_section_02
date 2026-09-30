import copy
import random
import string

class StringSolver:
  def __init__(self, target, pop_size, mut_rate, num_elites = 0):
    self.target = target
    self.all_characters = string.ascii_letters + ' !.?@#$%^&*()0123456789-_=+;:,'
    self.pop_size = pop_size
    self.mut_rate = mut_rate
    self.num_elites = num_elites
    self.pop = []
    self.generate_population()

  def generate_solution(self):
    s = ''
    for i in range(len(self.target)):
      s += random.choice(self.all_characters)
    return s

  def generate_population(self):
    self.pop = []
    for idx in range(self.pop_size):
      self.pop.append(self.generate_solution())

  def boolean_list_to_string(self, L):
    s = '['
    for b in L:
      if b:
        s += '1'
      else:
        s += '0'
    s += ']'
    return s

  def print_solution(self, sol, verbose = False):
    fitness_str = str(round(self.get_solution_fitness(sol), 2))
    print(f'{sol} = {fitness_str}')

  def print_population(self, pop = None, verbose = False):
    if pop is None:
      pop = self.pop
    for x in pop:
      self.print_solution(x, verbose)

  def get_solution_fitness(self, sol):
    letters_correct = 0
    letters_total = len(sol)
    for letter_idx in range(len(sol)):
      if sol[letter_idx] == self.target[letter_idx]:
        letters_correct += 1

    frac = letters_correct / letters_total
    return round(frac * 1000, 2) # This calculates fitness!

  def select(self, num_orgs):
    total_fitness = 0
    cumulative_fitnesses = []
    max_fitness = None
    max_fitness_orgs = []
    for org in self.pop:
      org_fitness = self.get_solution_fitness(org)
      total_fitness += org_fitness
      cumulative_fitnesses.append(total_fitness)
      if max_fitness is None or org_fitness > max_fitness:
        max_fitness = org_fitness
        max_fitness_orgs = [org]
      elif org_fitness == max_fitness:
        max_fitness_orgs.append(org)
    selected_orgs = []
    if self.num_elites > 0:
      selected_orgs += random.choices(max_fitness_orgs, k = self.num_elites)
    #print('Elite orgs:')
    #self.print_population(selected_orgs, True)
    for i in range(num_orgs - self.num_elites):
      random_val = random.uniform(0, total_fitness)
      for org_idx, org in enumerate(self.pop):
        if random_val < cumulative_fitnesses[org_idx]:
          selected_orgs.append(copy.deepcopy(org))
          break
    return selected_orgs

  def mutate(self, sol):
    offspring = copy.deepcopy(sol)
    for idx in range(len(sol)):
      if random.uniform(0, 1) < self.mut_rate:
        letter = random.choice(self.all_characters)
        offspring = offspring[:idx] + letter + offspring[idx + 1:]
    return offspring

  def run(self, num_gens, verbose = False):
    self.summary_file = 'evo_results.csv'
    self.max_file = 'max_org.csv'
    with open(self.summary_file, 'w') as out_fp:
      with open(self.max_file, 'w') as max_fp:
        out_fp.write('gen,avg_fitness,max_fitness\n')
        for gen_idx in range(num_gens):
          print(f'==== Gen {gen_idx} ====')
          parents = self.select(self.pop_size)
          self.pop = []
          for idx, parent in enumerate(parents):
            if idx >= self.num_elites:
              self.pop.append(self.mutate(parent))
            else:
              self.pop.append(parent)
          max_fitness = None
          max_orgs = []
          avg_fitness = 0
          for org in self.pop:
            fitness = self.get_solution_fitness(org)
            if max_fitness is None or fitness > max_fitness: 
              max_fitness = fitness
              max_orgs = [org]
            avg_fitness += fitness
          avg_fitness /= len(self.pop)
          print(f'Max fitness: {round(max_fitness, 2)}, Avg. fitness: {round(avg_fitness, 2)}')
          out_fp.write(f'{gen_idx},{avg_fitness},{max_fitness}\n')
          max_fp.write(f'{gen_idx},{max_orgs[0]},{max_fitness}\n')
          if verbose:
            self.print_population(verbose = True)



if __name__ == '__main__':
  target = 'CIS 678 - Machine Learning'
  solver = StringSolver(target, pop_size = 100, mut_rate = 0.01, num_elites = 3)
  solver.run(2000)
  solver.print_population(verbose = True)


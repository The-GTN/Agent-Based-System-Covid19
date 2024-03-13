from PolynomProblem import PolynomProblem
from PolynomInvidual import PolynomInvidual
import matplotlib.pyplot as plt

class AlgoGen:
    
    def __init__(self,problem,population_size,crossover_rate,mutation_probability):
        '''
        build an genetic algorithm to solve problem using a population of size population_size and a probability of muation of mutation_probability

        :param problem: (a Problem object) – the problem to solve
        :type problem: Problem
        :param population_size: the size of the population (must be even)
        :type population_size: int
        :param mutation_probability: the mutation probability
        :type mutation_probability: float

        :UC: population_size must be even and mutation_probability must be 0<= and <1
        '''
        assert population_size%2 == 0, "must have even population"
        assert 0 <= mutation_probability < 1, "probability..."
        self.problem = problem
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_probability = mutation_probability
        
    def run(self,nb_gene):
        population = [self.problem.create_individual() for _ in range(self.population_size)]
        self.problem.evaluate_all(population)
        for g in range(nb_gene):
            next_gen_1 = self.tournament(population)
            next_gen_2 = self.croisements(population)
            next_gen = next_gen_1 + next_gen_2
            for i in next_gen:
                i.mutate(self.mutation_probability)
            self.problem.evaluate_all(next_gen)
            self.problem.sort_population(population)
            self.problem.sort_population(next_gen)
            meilleurs = population[:5]
            next_gen = next_gen[len(next_gen)-5:]
            population = meilleurs + next_gen
        res = self.problem.best_individual(population)
        print(res.value[0])
        self.show(self.f(res))
        return res.value[0]
            
        
    def select(self,population,fct):
        l = len(population)
        res = []
        for i in range(l//2):
            res += fct(population[i],population[l-1-i])
        return res
    
    def melange(self,c1,c2):
        return c1.cross_with(c2)[0]
        
    def croisements(self,population):
        l = len(population)
        res = []
        for i in range(l//2):
            res += [self.melange(population[i],population[l-1-i])]
        return res
        
    def tournament(self,population):
        l = len(population)
        res = []
        for i in range(l//2):
            res += [self.problem.tournament(population[i],population[l-1-i])]
        return res
            
    def show(self,res):
        plt.figure(figsize=(12,10))
        plt.plot(self.problem.best, label="expected")
        plt.plot(res, label="result")
        plt.legend()
        plt.show()
        
    def f(self,res):
        return res.compute_coeff(res.value[0])
from functools import cmp_to_key
from PolynomInvidual import PolynomInvidual

class PolynomProblem():
    
    def __init__(self,funct,nb_degree,max_value,n):
        self.best = [funct(i) for i in range(n)]
        self.size = nb_degree
        self.max_value = max_value
        self.n = n
    
    def best_individual(self,population):
        '''
        return the best fitted individual from population.
        Depending on the problem, it can correspond to the individual
        with the highest or the lowest fitness value.
        '''
        best = population[0]
        for i in population:
            best = self.tournament(best,i)
        return best
    
    def create_individual(self):
        '''
        create a randomly generated indidivual for this problem
        '''
        return PolynomInvidual(self.size,self.max_value,self.n)
    
    def evaluate_all(self,pop):
        for i in pop:
            self.evaluate_fitness(i)
    
    def evaluate_fitness(self,individual):
        '''
        compute the fitness of individual for this problem
        '''
        individual.evaluate(self)
        
    def sort_population(self,population):
        '''
        sort population from best fitted to worst fitted individuals.
        Depending on the problem, it can correspond to ascending or
        descending order with respect to the fitness function.
        '''
        list.sort(population,key=cmp_to_key(self.__compare))
        
    def __compare(self,first,second):
        if first.get_score() > second.get_score():
            return -1
        else:
            return 1
        
    def tournament(self,first,second):
        '''
        perform a rounament between two individuals,
        the winner is the most fitted one, it is returned
        '''
        if first.get_score() > second.get_score():
            return first
        else:
            return second

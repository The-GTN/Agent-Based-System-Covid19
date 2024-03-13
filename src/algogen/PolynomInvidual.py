from random import randint

class PolynomInvidual():
    
    def __init__(self,size,max_value,n):
        self.size = size
        self.max_value = max_value
        self.n = n
        self.value = self.init_value()
        self.score = None
        
    def copy(self):
        '''
        build a copy of self, the genome is a copy of self’s genome
        '''
        other = PolynomInvidual(self.size,self.max_value,self.n)
        other.set_score(self.score)
        other.set_value(self.value)
        return other

    def cross_with(self,other):
        '''
        perform a 1 point crossover between self and other, two new built individuals are returned
        '''
        copyself = self.copy()
        copyother = other.copy()
        
        firsthalf = copyself.value[0][:len(copyself.value[0])//2]
        secondhalf = copyself.value[0][len(copyself.value[0])//2:]
        thirdhalf = copyself.value[0][:len(copyother.value[0])//2]
        quarterhalf = copyself.value[0][len(copyother.value[0])//2:]
        
        copyself_part1 = firsthalf + quarterhalf
        copyself_part2 = copyself.compute_coeff(copyself_part1)
        copyself.value = (copyself_part1,copyself_part2)
        copyother_part1 = thirdhalf + secondhalf
        copyother_part2 = copyother.compute_coeff(copyother_part1)
        copyother.value = (copyother_part1,copyother_part2)
        
        return (copyself,copyother)
        
    def evaluate(self,problem):
        '''
        set the fitness score with the fitness computed by problem for self
        '''
        score = 0
        value = self.value[1]
        for v in range(len(value)):
            score += -(abs(problem.best[v] - value[v])*100)
        self.score = score
        

    def get_score(self):
        return self.score

    def get_size(self):
        return self.size

    def get_value(self):
        return self.value

    def init_value(self):
        '''
        randomly initialize the genome value of self
        '''
        coeff = [randint(0,self.max_value) for _ in range(self.size)]
        value = self.compute_coeff(coeff)
        return (coeff,value)
        
    def mutate(self,probability):
        '''
        apply mutation operation to self : each element of the geome sequence is randomly changed with given probabiliy
        '''
        p = probability*100
        changement = False
        for i in range(len(self.value[0])):
            if randint(0,100) <= p:
                self.value[0][i] = (self.value[0][i]+1)%self.max_value
                changement = True
        if changement:
            self.value = (self.value[0],self.compute_coeff(self.value[0]))
            
    def compute_coeff(self,coeff):
        value = []
        for i in range(self.n):
            res = 0
            for j in range(self.size):
                res += coeff[j]*(i**j)
            value += [res]
        return value

    def set_score(self,new_score):
        '''
        change the fitness score of self
        '''
        self.score = new_score

    def set_value(self,new_value):
        '''
        change the genome value of self
        '''
        self.value = new_value

# Briar Doty
# Nov 2013
# GeneticAlg.py
# Genetic algorithm trains Neural network

import random
import Common

class Chromosome:

	# Input:
	# Output:
	# Description:
	def __init__(self, weights):
		self.weights = weights
		self.fitness = 0
		
	def __eq__(self, other):
		return self.fitness == other.fitness
		
	def __lt__(self, other):
		return self.fitness < other.fitness
		
class GenAlg:

	# Input:
	#     popSize - number of Chromosomes in population
	#     mutRate - probability a weight will mutate in a single epoch
	#     crossRate - probability two chromosomes will cross over in single epoch
	#     numWeight - total number of weights in NN each Chromosome represents
	# Output:
	# Description:
	#     Initializes state necessary to evolve population of NNs using genetic alg
	def __init__(self, popSize, mutRate, crossRate, numWeight):
		self.popSize = popSize
		self.mutRate = mutRate
		self.crossRate = crossRate
		self.numWeight = numWeight
		
		self.createPop()
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#     Initialize population of Chromosomes for each neural net, containing random weights
	def createPop(self):
		self.population = []
		for i in range(self.popSize):
			self.population.append(Chromosome([random.uniform(-1, 1) for j in range(self.numWeight)]))
		
	# Input:
	#     c - chromosome to mutate
	# Output:
	#		mutated chromosome
	# Description:
	#		Perturb chromosome weights depending on mutation rate
	def mutate(self, c):
		# traverse chromosome and mutate weights depending on rate
		for i in range(len(c.weights)):
			if (random.uniform(0, 1) < self.mutRate): # mutate this weight
				c.weights[i] += random.uniform(-1, 1) * Common.maxPerturbation
		
	# Input:
	# 		c1, c2 - chromosomes to cross over
	# Output:
	#		tuple containing resulting chromosomes
	# Description:
	#		Switch gene segments between 2 given chromosomes based on crossover rate
	def crossover(self, c1, c2):
		if (random.uniform(0, 1) > self.crossRate or c1.weights == c2.weights): # no crossover
			return (c1, c2)

		# index of crossover
		crossPoint = random.randint(0, self.numWeight - 1)
		
		# create offspring
		r1 = Chromosome(c1.weights[:crossPoint] + c2.weights[crossPoint:])
		r2 = Chromosome(c2.weights[:crossPoint] + c1.weights[crossPoint:])
		
		return (r1, r2)
	
	# Input:
	#		population - vector of chromosomes representing population of NNs
	# Output:
	#		an evolved population, new generation
	# Description:
	#		Evolves the given population one generation
	def evolve(self, population):
		result = []
		
		# sort population according to fitness
		population.sort()
		
		# increase frequency of fittest chromosomes in population
		population = self.replicateFittest(Common.numElite, Common.numCopiesElite, population)
		
		# main GA loop
		while (len(result) < self.popSize):
			# pick 2 chromosomes to alter
			c1 = random.choice(population)
			c2 = random.choice(population)
			
			(c3, c4) = self.crossover(c1, c2)
			
			self.mutate(c3)
			self.mutate(c4)
			
			# add to result new generation
			result.append(c3)
			result.append(c4)
		
		return result
		
	# Input:
	#		nFittest - number of top-ranked chromosomes to replicate
	#		nCopies - number copies of chromosomes to make
	#		population - vector of chromosomes representing population of NNs
	# Output:
	#		a population with increased number of fit chromosomes
	# Description:
	#		Increases the frequency of the fittest chromosomes
	def replicateFittest(self, nFittest, nCopies, population):
		# take nFittest chromosomes and copy them nCopies times
		fittest = population[:nFittest]
		result = population + nCopies * fittest
		
		return result
		
		
		
		
		
		
		
		
		
		
		
		
		
	
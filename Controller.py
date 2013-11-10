# Briar Doty
# Oct 2013
# Controller.py
# Wires units together into 2d demo/game

from tkinter import *
from Unit import Unit
import Common
import random
from GeneticAlg import *
import math
import numpy as np
from scipy import spatial
import pylab
import time
import sys
import ast

class Controller:

	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Initializes game state and starts app
	def __init__(self, importFlag=False):
		# create units
		self.player = Unit(random.uniform(0,Common.boardWidth),
									random.uniform(0,Common.boardHeight), 
									0, 0, Common.boardWidth, Common.boardHeight)
		
		self.predators = [Unit(random.uniform(0,Common.boardWidth),
									random.uniform(0,Common.boardHeight),
									0, 0, Common.boardWidth, Common.boardHeight)
									for i in range(Common.numEnemies)]

		self.prey = [Unit(random.uniform(0,Common.boardWidth),
								random.uniform(0,Common.boardHeight),
								0, 0, Common.boardWidth, Common.boardHeight)
								for i in range(Common.numPrey)]
								
		self.preyCoordTree = spatial.cKDTree(np.array([(p.x,p.y) for p in self.prey]))
								
		
								
		# create AI
		for e in self.predators: 
			e.createBrain()
			
		if (importFlag):
			# import weights from file
			with open('weights.txt','r') as f:
				content = f.readlines()
				importWeights = [ast.literal_eval(lst) for lst in content]
			
			for p in self.predators:
				p.neuralNet.putWeights(random.choice(importWeights))
		
		# wrapper class for GA functionality
		self.genAlg = GenAlg(Common.numEnemies, Common.mutRate, Common.crossRate, 
										self.predators[0].neuralNet.getNumWeights())
		
		# initialize tk, other fields and main loop
		self.initCanvas()
		self.killCount, self.ticker, self.epochs = 0, 0, 0
		self.animate = True
		self.avgFitness = []
		self.maxFitness = []
		self.gameLoop()
		self.root.mainloop()
		
	# Input:
	#		None
	# Output:
	#		 None
	# Description:
	#		Initializes fields related to tkinter UI library
	def initCanvas(self):
		# create root and canvas
		self.root = Tk()
		self.canvas = Canvas(self.root, width=Common.boardWidth, height=Common.boardHeight)
		self.canvas.pack()
		self.root.canvas = self.canvas.canvas = self.canvas
		self.root.bind("<Key>", self.keyPressed)
		
	# Input:
	#		event - tkinter keypress even to process
	# Output:
	#		None
	# Description:
	#		Accepts user arrow-key input and translates to unit acceleration
	def keyPressed(self, event):
		if (event.keysym == "Up"):
			self.player.accY(-1)
		elif (event.keysym == "Down"):
			self.player.accY(1)
		elif (event.keysym == "Left"):
			self.player.accX(-1)
		elif (event.keysym == "Right"):
			self.player.accX(1)
		elif (event.keysym == "f"):
			# end animation and enter simulation
			self.animate = not self.animate
	
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Timer function calls functions to advance game state
	def gameLoop(self):
		self.moveUnits()
		self.drawState()
		self.ticker += 1
		if (self.ticker > Common.epochLen):
			self.endEpoch()
			self.epochs += 1
			self.canvas.after(Common.delay, self.gameLoop)
		elif (self.animate):
			self.canvas.after(Common.delay, self.gameLoop)
		elif (self.epochs >= Common.numEpochs):
			self.genPlot()
			self.root.destroy()
			sys.exit()
		else:
			# destroy game canvas and start pure simulation
			self.root.destroy()
			self.simLoop()
			
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Timer function advances simulation state by whole epochs
	def simLoop(self):
	
		while (self.epochs < Common.numEpochs):
			# advance epoch
			while (self.ticker <= Common.epochLen):
				self.moveUnits()
				self.ticker += 1
			self.endEpoch()
			self.epochs += 1
		
		# generate fitness plot
		self.genPlot()
		
		# export data to text file
		f = open('weights.txt', 'w')
		for i in range(Common.numElite):
			netWeights = self.predators[i].neuralNet.getWeights()
			f.write(str(netWeights) + '\n')
			
		f.close()
		
		# exit app
		sys.exit()
			
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Calls functions to advance unit state and positions 
	def moveUnits(self):
		# advance player
		self.player.advance()
	
		# update enemy AI and advance
		for e in self.predators:
			output = e.neuralNet.update(self.getNNInput(e))
			e.accX(output[0])
			e.accY(output[1])
			e.advance()
			# check if distance to nearest is small enough to clear
			(nearest, index) = self.getNearestPrey(e)
			if (self.getDist(e.x, e.y, nearest.x, nearest.y) < 10):
				# increment fitness
				e.fitness += 1 
				self.killCount += 1

				# remove prey
				self.prey.pop(index)
				
				# add new prey
				self.prey.append(Unit(random.uniform(0,Common.boardWidth),
											random.uniform(0,Common.boardHeight),
											0, 0, Common.boardWidth, Common.boardHeight))
											
				# rebuild cKDTree
				self.preyCoordTree = spatial.cKDTree(np.array([(p.x,p.y) for p in self.prey]))
		
		# sort predators WRT fitness to keep track of most fit
		self.predators.sort()
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Clears old and draws new game state
	def drawState(self):
		# clear canvas
		self.canvas.delete(ALL)
	
		# draw player
		(l,r,t,b) = self.player.getDim()
		self.canvas.create_oval(l, t, r, b, fill="blue")
		
		# draw prey
		for p in self.prey:
			(l,r,t,b) = p.getPreyDim()
			self.canvas.create_rectangle(l, t, r, b, fill="green")
		
		# draw predators
		for i in range(len(self.predators)):
			e = self.predators[i]
			(l,r,t,b) =e.getDim()
			if (i < Common.numElite):
				# draw most fit preds in purple
				self.canvas.create_rectangle(l, t, r, b, fill="orange")
			else:
				self.canvas.create_rectangle(l, t, r, b, fill="red")
			(nearest, index) = self.getNearestPrey(e)
			self.canvas.create_line(e.x, e.y, nearest.x, nearest.y, fill="red", dash=(4,4))
			
	# Input:
	#		e - enemy unit for which to generate NN input
	# Output:
	#		result - vector input for given unit's Neural Net
	# Description:
	#		Returns input vector to given unit's Neural Net
	def getNNInput(self, e):
		# get vector towards nearest prey
		(nearest, index) = self.getNearestPrey(e)
		#nearest = self.player
		preyDir = [nearest.x - e.x, nearest.y - e.y]

		# and vector of this unit's current direction
		unitDir = [e.vx, e.vy]
		result = [preyDir[0], preyDir[1], unitDir[0], unitDir[1]]
		
		return result
		
	# Input:
	#		unit - the unit for which to find the nearest prey
	# Output:
	#		(prey, i) - where prey is the nearest prey and i is its index
	# Description:
	#		Uses KDTree Nearest Neighbor search to find the prey nearest the given predator unit
	def getNearestPrey(self, unit):
		(dist, i) = self.preyCoordTree.query((unit.x, unit.y), k=1)
		return (self.prey[i], i)
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Runs GA to evolve NN weights and restarts game
	def endEpoch(self):
		# store fitnesses
		fitness = []
		for e in self.predators:
			fitness.append(e.fitness)
		
		self.avgFitness.append(sum(fitness)/len(fitness))
		self.maxFitness.append(max(fitness))
	
		print("Generation " + str(self.epochs))
		print("Average fitness: " + str(self.avgFitness[-1]))
		print("Maximum fitness: " + str(self.maxFitness[-1]))
		print()
		
		# run GA on population of enemies
		population = [Chromosome(e.neuralNet.getWeights(), e.fitness) for e in self.predators]
		population = self.genAlg.evolve(population)
		
		# put weights into NNs
		for i in range(Common.numEnemies):
			self.predators[i].neuralNet.putWeights(population[i].weights)
			self.predators[i].fitness = 0
		
		# start next epoch
		self.ticker = 0
		self.killCount = 0
		
	# Input:
	#		x1, y1 - coordinates of  point 1
	#		x2, y2 - coordinates of point 2
	# Output:
	#		Distance
	# Description:
	#		Returns euclidean distance between given points
	def getDist(self, x1, y1, x2, y2):
		return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
		
	# Input:
	#		v - vector to normalize
	# Output:
	#		result - normalized copy of given vector
	# Description:
	#		Returns a normalized copy of the given vector (2-norm)
	def normalize(self, v):
		norm = math.sqrt(sum([x**2 for x in v]))
		if (norm != 0):
			result = [x/norm for x in v]
		else:
			result = v
		return result
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Plots fitness of generations after simulation is complete
	def genPlot(self):
		pylab.plot(range(len(self.avgFitness)), self.avgFitness, 'b--', range(len(self.maxFitness)), self.maxFitness, 'r--')
		pylab.xlabel('epoch')
		pylab.ylabel('fitness')
		pylab.savefig('fitness.png')
		
# Run app
if (__name__ == "__main__"):
	c = Controller(Common.importFlag)
















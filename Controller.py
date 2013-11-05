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

class Controller:

	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Initializes game state and starts app
	def __init__(self):
		# create root and canvas
		root = Tk()
		self.canvas = Canvas(root, width=Common.boardWidth, height=Common.boardHeight)
		self.canvas.pack()
		root.canvas = self.canvas.canvas = self.canvas
		
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
								
		# create AI
		for e in self.predators: 
			e.createBrain()
		
		# wrapper class for GA functionality
		self.genAlg = GenAlg(Common.numEnemies, Common.mutRate, Common.crossRate, 
										self.predators[0].neuralNet.getNumWeights())
		
		# wire events and start loop
		self.killCount = 0
		self.ticker = 0
		root.bind("<Key>", self.keyPressed)
		self.timerFired()
		root.mainloop()
		
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
	
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Timer function calls functions to advance game state
	def timerFired(self):
		self.moveUnits()
		self.ticker += 1
		if (self.ticker > Common.epochLen):
			self.endEpoch()
		else:
			delay = Common.delay # milliseconds
			self.canvas.after(delay, self.timerFired)
		
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
			nearest = self.getNearest(e, self.prey)
			if (self.getDist(e.x, e.y, nearest.x, nearest.y) < 10):
				# increment fitness
				e.fitness += 1 
				self.killCount += 1

				# remove prey
				self.prey.remove(nearest)
				
				# add new prey
				self.prey.append(Unit(random.uniform(0,Common.boardWidth),
											random.uniform(0,Common.boardHeight),
											0, 0, Common.boardWidth, Common.boardHeight))
		
		# draw new state
		self.drawState()
		
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
		for e in self.predators:
			(l,r,t,b) =e.getDim()
			self.canvas.create_rectangle(l, t, r, b, fill="red")
			
	# Input:
	#		e - enemy unit for which to generate NN input
	# Output:
	#		result - vector input for given unit's Neural Net
	# Description:
	#		Returns input vector to given unit's Neural Net
	def getNNInput(self, e):
		result = []
		
		# get vector towards nearest prey
		nearest = self.getNearest(e, self.prey)
		preyDir = (nearest.x - e.x, nearest.y - e.y)

		# and vector of this unit's current direction
		unitDir = (e.vx, e.vy)
		
		#result = [self.player.x, self.player.y, e.x, e.y]
		result = [preyDir[0], preyDir[1], unitDir[0], unitDir[1]]
		
		return result
		
	# Input:
	#		unit - unit from which to minimize distance
	#		listOfUnits - vector of units to search through
	# Output:
	#		result - unit in given list nearest the given unit
	# Description:
	#		Returns a reference to the unit in the given list nearest the given unit
	def getNearest(self, unit, listOfUnits):
		result = listOfUnits[0]
		dist = Common.boardWidth + Common.boardHeight
		
		for u in listOfUnits:
			test = self.getDist(unit.x, unit.y, u.x, u.y)
			if (test < dist):
				dist = test
				result = u
				
		return result
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Runs GA to evolve NN weights and restarts game
	def endEpoch(self):
		# print fitnesses
		for e in self.predators:
			print(e.fitness)
		print("Total eaten: " + str(self.killCount))
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
		self.timerFired()
		
	# Input:
	#		x1, y1 - coordinates of  point 1
	#		x2, y2 - coordinates of point 2
	# Output:
	#		Distance
	# Description:
	#		Returns euclidean distance between given points
	def getDist(self, x1, y1, x2, y2):
		return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
		
# Run app
if (__name__ == "__main__"):
	c = Controller()
















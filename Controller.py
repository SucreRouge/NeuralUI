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
	# Output:
	# Description:
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
		
		self.enemies = [Unit(random.uniform(0,Common.boardWidth),
									random.uniform(0,Common.boardHeight),
									0, 0, Common.boardWidth, Common.boardHeight)
									for i in range(Common.numEnemies)]
								
		# create AI
		for e in self.enemies: 
			e.createBrain()	# give each enemy a NN
		
		# wrapper class for GA functionality
		self.genAlg = GenAlg(Common.numEnemies, Common.mutRate, Common.crossRate, 
										self.enemies[0].neuralNet.getNumWeights())
		
		# wire events and start loop
		self.ticker = 0
		root.bind("<Key>", self.keyPressed)
		self.timerFired()
		root.mainloop()
		
	# Input:
	#		event - tkinter keypress even to process
	# Output:
	#		none
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
	#		canvas - tkinter game canvas
	# Output:
	#		none
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
	#		canvas - tkinter game canvas
	# Output:
	#		none
	# Description:
	#		calls functions to advance unit positions
	def moveUnits(self):
		# run update on all NNs
		for e in self.enemies:
			output = e.neuralNet.update([self.player.x, self.player.y, e.x, e.y])
			e.accX(output[0])
			e.accY(output[1])
	
		# advance player
		self.player.advance()
		(l,r,t,b) = self.player.getDim()
		
		# advance enemies
		for i in range(Common.numEnemies):
			self.enemies[i].advance()
		
		self.canvas.delete(ALL)
		
		# draw new state
		self.canvas.create_oval(l, t, r, b, fill="blue")
		
		for i in range(Common.numEnemies):
			(l,r,t,b) = self.enemies[i].getDim()
			self.canvas.create_rectangle(l, t, r, b, fill="red")
			
		self.adjustFitness()
		self.adjustFitness2()
			
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Adjust enemy fitness based on behavior
	def adjustFitness(self):
		closest = self.enemies[0]
		dist = Common.boardWidth + Common.boardHeight
		for e in self.enemies:
			test = math.sqrt((self.player.x - e.x)**2 + (self.player.y - e.y)**2)
			if (test < dist):
				dist = test
				closest = e
				
		e.fitness += 1
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Adjust enemy fitness based on behavior
	def adjustFitness2(self):
		# loop through enemies and find those close to player
		for e in self.enemies:
			if ((math.sqrt((self.player.x - e.x)**2 + (self.player.y - e.y)**2)) < 25):
				# adjust unit's fitness
				e.fitness += 1
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Runs GA to evolve NN weights and restarts game
	def endEpoch(self):
		# print fitnesses
		for e in self.enemies:
			print(e.fitness)
		print()
		
		# run GA on population of enemies
		population = [Chromosome(e.neuralNet.getWeights(), e.fitness) for e in self.enemies]
		population = self.genAlg.evolve(population)
		
		# put weights into NNs
		for i in range(Common.numEnemies):
			self.enemies[i].neuralNet.putWeights(population[i].weights)
		
		# start next epoch
		self.ticker = 0
		self.timerFired()
	
			
	
	
		


















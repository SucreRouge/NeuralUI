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
		self.player = Unit(100, 100, 0, 0, Common.boardWidth, Common.boardHeight)
		self.enemies = [Unit(random.uniform(0,Common.boardWidth),
									   random.uniform(0,Common.boardHeight),
									   0, 0, Common.boardWidth, Common.boardHeight)
								for i in range(Common.numEnemies)]
								
		# create AI
		for e in self.enemies: 
			e.createBrain()	# give each enemy a NN
		
		# create weights with GenAlg
		self.genAlg = GenAlg(Common.numEnemies, Common.mutRate, Common.crossRate, 
										self.enemies[0].neuralNet.getNumWeights())
										
		# put weights into NNs
		for i in range(len(self.enemies)):
			self.enemies[i].neuralNet.putWeights(self.genAlg.population[i].weights)
		
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
		if (self.ticker > 1500):
			self.endEpoch()
		else:
			delay = 25 # milliseconds
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
			
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Adjust enemy fitness based on behavior
	def adjustFitness(self):
		# loop through enemies and find closest to player
		closest = 0
		dist = Common.boardWidth + Common.boardHeight
		for i in range(len(self.enemies)):
			# if closer than current closest, replace closest
			test = math.sqrt((self.player.x - self.enemies[i].x)**2 + (self.player.y - self.enemies[i].y)**2)
			if ((test) < (dist)):
				dist = test
				closest = i
				
		# adjust fitness of corresponding genome
		self.genAlg.population[closest].fitness += 1
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		
	def endEpoch(self):
		# run GA on population of enemies
		for c in self.genAlg.population:
			print(c.fitness)
			
		self.genAlg.population = self.genAlg.evolve(self.genAlg.population)
		
		# start next epoch
		self.ticker = 0
		self.timerFired()
	
			
	
	
		


















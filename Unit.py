# Briar Doty
# Oct 2013
# Unit.py
# Defines class for units in neural net demo

from NeuralNet import NeuralNet
import Common

class Unit:

	# Input:
	#		x, y - xy coord of unit
	#		vx, vy - xy components to velocity
	#		boardW - board width (used for edge detection)
	#		boardH - ""
	# Output:
	#		None
	# Description:
	#		Constructor for game units
	def __init__(self, x, y, vx, vy, boardW, boardH):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.maxVel = Common.maxVel
		self.boardW = boardW
		self.boardH = boardH
		
	def __eq__(self, other):
		return self.fitness == other.fitness
		
	def __lt__(self, other):
		return self.fitness > other.fitness
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Called each time game timer fires, advances units position according to velocity
	def advance(self):
		# new x pos
		if (self.x + self.vx < 0):
			self.x = self.boardW + (self.x + self.vx)
		elif (self.x + self.vx > self.boardW):
			self.x = self.x + self.vx - self.boardW
		else:
			self.x = self.x + self.vx
			
		# new y pos
		if (self.y + self.vy < 0):
			self.y = self.boardH + (self.y + self.vy)
		elif (self.y + self.vy > self.boardH):
			self.y = self.y + self.vy - self.boardH
		else:
			self.y = self.y + self.vy
	
	# Input:
	#		dx - amount to perturb x velocity by
	# Output:
	#		None
	# Description:
	#		Adjust x velocity component according to given dx
	def accX(self, dx):
		if (abs(self.vx + dx) <= self.maxVel):
			self.vx = self.vx + dx
	
	# Input:
	#		dy - amount to perturb y velocity by
	# Output:
	#		None
	# Description:
	#		Adjust x velocity component according to given dy
	def accY(self, dy):
		if (abs(self.vy + dy) <= self.maxVel):
			self.vy = self.vy + dy
			
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Return dimensions for drawing this unit
	def getDim(self):
		# return (left right top bottom)
		return (self.x - 5, self.x + 5, self.y - 5, self.y + 5)
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Return dimensions for drawing this unit
	def getPreyDim(self):
		# return (left right top bottom)
		return (self.x - 3, self.x + 3, self.y - 3, self.y + 3)
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Initialize this AI unit with a Neural Network controller
	def createBrain(self):
		self.neuralNet = NeuralNet(Common.numInput, Common.numOutput, 
												Common.numHiddenLyr, Common.numNrnPerHiddenLyr)
		self.fitness = 0
			
			
			
			
			
			
			
			
			
			
			
# Briar Doty
# Oct 2013
# Unit.py
# Defines class for units in neural net demo

from NeuralNet import NeuralNet
import Common

class Unit:

	# constructor
	def __init__(self, x, y, vx, vy, boardW, boardH):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.maxVel = 5
		self.boardW = boardW
		self.boardH = boardH
		
	# print unit state to console
	def displayState(self):
		print(str(self.x) + str(self.y) + str(self.vx) + str(self.vy))
		
	# called each time game timer fires, advances units position according
	# to velocity
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
	
	# adjust x velocity component according to given dx
	def accX(self, dx):
		if (abs(self.vx + dx) <= self.maxVel):
			self.vx = self.vx + dx
	
	# adjust y velocity component according to given dy
	def accY(self, dy):
		if (abs(self.vy + dy) <= self.maxVel):
			self.vy = self.vy + dy
			
	# return dimensions for drawing this unit
	def getDim(self):
		# return (left right top bottom)
		return (self.x - 5, self.x + 5, self.y - 5, self.y + 5)
		
	def createBrain(self):
		self.neuralNet = NeuralNet(Common.numInput, Common.numOutput, 
												Common.numHiddenLyr, Common.numNrnPerHiddenLyr)
			
			
			
			
			
			
			
			
			
			
			
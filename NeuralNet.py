# Briar Doty
# Oct 2013
# NeuralNet.py
# Defines classes related to Neural Network implementation

import random
import math

# class defines single neurons
class Neuron:

	# constructor for single neuron
	def __init__(self, numInput):
		self.numInput = numInput # length of input vectors
		#self.weights = [random.uniform(-1, 1) for i in range(numInput + 1)] # rand weights + threshold
		self.weights = [0]*(numInput + 1)
	
# class defines single neuron layers	
class NeuronLayer:

	# constructor for single neuron layer
	def __init__(self, numNeuron, numInput):
		self.numNeuron = numNeuron # num neurons in this layer
		self.neurons = [Neuron(numInput) for i in range(numNeuron)] # layer
		
# class defines neural network
class NeuralNet:

	# constructor for network
	def __init__(self, numInput, numOutput, numHiddenLayer, numNeuron):
		# init state
		self.numInput = numInput
		self.numOutput = numOutput
		self.numHiddenLayer = numHiddenLayer
		self.numNeuron = numNeuron
		self.layers = []
		
		# initialize network
		self.createNet()
		
	# called by constructor, creates neuron layers
	def createNet(self):
		if (self.numHiddenLayer > 0):
			# create first layer
			self.layers.append(NeuronLayer(self.numNeuron, self.numInput))
			
			# create hidden layers
			for i in range(self.numHiddenLayer-1):
				self.layers.append(NeuronLayer(self.numNeuron, self.numNeuron))
			
			# create output layer
			self.layers.append(NeuronLayer(self.numOutput, self.numNeuron))
			
		else:
			# create output layer
			self.layers.append(NeuronLayer(self.numOutput, self.numInput))
			
	# return weights in network
	def getWeights(self):
		result = []
		for lyr in self.layers:
			for n in lyr.neurons:
				for w in n.weights:
					result.append(w)
		return result
		
	# return total number of weights in network
	def getNumWeights(self):
		result = 0
		for lyr in self.layers:
			for n in lyr.neurons:
				for w in n.weights:
					result+= 1
		return result
	
	# replace weights with new ones
	def putWeights(self, weights):
		cWeight = 0
		for lyr in self.layers:
			for n in lyr.neurons:
				for i in range(len(n.weights)):
					n.weights[i] = weights[cWeight]
					cWeight += 1
	
	# returns computed outputs given set of inputs
	def update(self, input):
		output = []
		
		if (len(input) != self.numInput): return output
	
		# for each layer
		for i in range(len(self.layers)):
			if (i > 0):
				input = output # secondary layers take output of previous layer as input
				
			output = [] # clear output
			
			weight = 0
			
			# for each neuron
			for j in range(self.layers[i].numNeuron):
				numInput = self.layers[i].neurons[j].numInput
				
				netInput = 0
				
				# for each weight
				for k in range(numInput):
					netInput += self.layers[i].neurons[j].weights[k] * input[weight]
					weight += 1
					
				# add threshold
				netInput += self.layers[i].neurons[j].weights[-1] * -1
				
				print(netInput)
				# append neuron response to output
				output.append(self.sigmoid(netInput))
				
				weight = 0
		return output
	
	# sigmoid response curve
	def sigmoid(self, activation):
		return 2 / (1 + math.exp(-1 * activation)) - 1
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
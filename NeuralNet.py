# Briar Doty
# Oct 2013
# NeuralNet.py
# Defines classes related to Neural Network implementation

import random
import math

# class defines single neurons
class Neuron:

	# Input:
	#		numInput - length of input vectors
	# Output:
	#		None
	# Description:
	#		Constructor for Neuron object, initializes weights and threshold of 0
	def __init__(self, numInput):
		self.numInput = numInput 
		self.weights = [random.uniform(-1, 1) for i in range(numInput + 1)] # rand weights + threshold
	
# class defines single neuron layers	
class NeuronLayer:

	# Input:
	#		numNeuron - number of Neuron objects in this layer
	#		numInput - length of input vectors to each Neuron in layer
	# Output:
	#		None
	# Description:
	#		Constructor for NeuronLayer object, initializes with new Neurons
	def __init__(self, numNeuron, numInput):
		self.numNeuron = numNeuron # num neurons in this layer
		self.neurons = [Neuron(numInput) for i in range(numNeuron)] # layer
		
# class defines neural network
class NeuralNet:

	# Input:
	#		numInput - length of input vector
	#		numOutput - length of output vector
	#		numHiddenLayer - number of hidden layers in the network
	#		numNeuron - number of neurons per hidden layer
	# Output:
	#		None
	# Description:
	#		Constructor for NeuralNet class
	def __init__(self, numInput, numOutput, numHiddenLayer, numNeuron):
		# init state
		self.numInput = numInput
		self.numOutput = numOutput
		self.numHiddenLayer = numHiddenLayer
		self.numNeuron = numNeuron
		self.layers = []
		
		# initialize network
		self.createNet()
		
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Called by constructor, creates neuron layers
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
			
	# Input:
	#		None
	# Output:
	#		None
	# Description:
	#		Return weights in network
	def getWeights(self):
		result = []
		for lyr in self.layers:
			for n in lyr.neurons:
				for w in n.weights:
					result.append(w)
		return result
		
	# Input:
	#		None
	# Output:
	#		result - count of all weights in this NN
	# Description:
	#		Return total number of weights in network
	def getNumWeights(self):
		result = 0
		for lyr in self.layers:
			for n in lyr.neurons:
				for w in n.weights:
					result+= 1
		return result
	
	# Input:
	#		weights - vector of weights to insert into this NN
	# Output:
	#		None
	# Description:
	#		Replace weights with new ones
	def putWeights(self, weights):
		cWeight = 0
		for lyr in self.layers:
			for n in lyr.neurons:
				for i in range(len(n.weights)):
					n.weights[i] = weights[cWeight]
					cWeight += 1
	
	# Input:
	#		input - input vector for NN
	# Output:
	#		output - result of running input through network
	# Description:
	#		Returns computed outputs given vector of inputs
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
				
				# append neuron response to output
				output.append(self.sigmoid(netInput))
				
				weight = 0
		return output
	
	# Input:
	#		activation - netOutput of Neuron object
	# Output:
	#		response - pass activation through sigmoid
	# Description:
	#		Sigmoid function to pass netOutput through
	def sigmoid(self, activation):
		try:
			x = float(math.exp(-1 * activation))
			return 2 / (1 + x) - 1
		except OverflowError:
			if (activation < 0):
				return -1
			else:
				return 1
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
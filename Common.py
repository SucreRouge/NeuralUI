# Briar Doty
# Nov 2013
# Common.py
# Common params and code

# genetic alg params
maxPerturbation = 0.3		# max value to perturb chromosome weight by
numElite = 2						# number of ranked elite chromosomes to replicate per generation
numCopiesElite = 2			# number of copies of elite chromosomes to make
mutRate = 0.06				# probability a given allele will mutate
crossRate = 0.3				# probability 2 selected chromosomes will cross over

# neural net params
numInput = 4					# length of input vector into NeuralNetwork.update() (must also change calls to this in Controller)
numOutput = 2					# length of output vector from NeuralNetwork.update()
numHiddenLyr = 1			# number of hidden layers in each NN
numNrnPerHiddenLyr = 3	# number of neurons in each hidden layer

# general params
numEnemies = 20				# number enemy units
numPrey = 40					# number prey units
boardWidth = 720				# game width in pixels
boardHeight = 540			# height
epochLen = 1000				# timer clicks per generation
delay = 25						# ms per frame
numEpochs = 100			# number of epochs simulated before killing app
maxVel = 5						# max speed in one axis of each unit
importFlag = False			# bool determines whether initial weights are randomly generated or imported from file (must have file)
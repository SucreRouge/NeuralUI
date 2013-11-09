# Briar Doty
# Nov 2013
# Common.py
# Common params and code

# genetic alg params
maxPerturbation = 0.3		# max value to perturb chromosome weight by
numElite = 1						# number of ranked elite chromosomes to replicate per generation
numCopiesElite = 3			# number of copies of elite chromosomes to make
mutRate = 0.05				# probability a given allele will mutate
crossRate = 0.3				# probability 2 selected chromosomes will cross over

# neural net params
numInput = 4					# length of input vector into NeuralNetwork.update() (must also change calls to this in Controller)
numOutput = 2					# length of output vector from NeuralNetwork.update()
numHiddenLyr = 1			# number of hidden layers in each NN
numNrnPerHiddenLyr = 3	# number of neurons in each hidden layer

# general params
numEnemies = 10				# number enemy units
numPrey = 20					# number prey units
boardWidth = 720				# game width in pixels
boardHeight = 540			# height
epochLen = 1000				# timer clicks per generation
delay = 25						# ms per frame
numEpochs = 50				# number of epochs simulated before killing app
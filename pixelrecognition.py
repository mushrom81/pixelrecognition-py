from neuralnetwork import *

f = open("tests.csv", "r")
fileText = f.read()
fileLines = fileText.split("\n")
for i in range(len(fileLines) - 1):
    fileLines[i] = fileLines[i].split(",")
    for j in range(len(fileLines[i])):
        fileLines[i][j] = int(fileLines[i][j])

questionNumber = -1

def getNewQuestion():
    global questionNumber
    global question
    global answer
    questionNumber = (questionNumber + 1) % 6144
    question = fileLines[questionNumber][1:]
    answer = fileLines[questionNumber][0]

def largestIndex(array):
    currentLargest = array[0]
    currentIndex = 0
    for i in range(len(array)):
        if (array[i] > currentLargest):
            currentLargest = array[i]
            currentIndex = i
    return currentIndex

def removeElementFromArray(array, index):
    newArray = []
    for i in range(len(array)):
        if i != index:
            newArray.append(array[i])
    return newArray

def mutate(inputNetwork, mutationRate):
    network = inputNetwork.clone()
    for layer in range(1, len(network.widths)):
        for width in range(network.widths[layer]):
            for connection in range(network.widths[layer - 1]):
                if random() < mutationRate:
                    network.layers[layer][width].mutateStrength(connection)
            if random() < mutationRate:
                network.layers[layer][width].bias += random() - 0.5
    return network;

def newNetwork():
    array = [2500, 50, 7, 1]
    network = Network(array)
    network.createHiddenLayers()
    network = mutate(network, 0.5)
    return network

generation = []
for i in range(20):
    generation.append(newNetwork())

generationNumber = 0
while True:
    generationNumber += 1
    fitness = sizedArray(len(generation), 0)
    for t in range(6144):
        getNewQuestion()
        for i in range(20):
            generation[i].createInputLayer(question)
            generation[i].runNetwork()
            if round(generation[i].outputs[0]) == answer:
                fitness[i] += 1
    highestFitness = fitness[largestIndex(fitness)]
    print(arrToStr(generation[largestIndex(fitness)].exportNetwork()))
    print([6144 - highestFitness, generationNumber])
    best = []
    for i in range(5):
        best.append(generation[largestIndex(fitness)].clone())
        fitness = removeElementFromArray(fitness, largestIndex(fitness))
    generation = best[:]
    for i in range(15):
        generation.append(mutate(generation[i % 5], -highestFitness / 3072 + 2))


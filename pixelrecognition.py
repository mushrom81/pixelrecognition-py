import math
from random import random

def sig(x):
    denominator = 1 + math.exp(-x)
    return 1 / denominator

def sizedArray(width, defaultValue):
    array = []
    for i in range(width):
        array.append(defaultValue)
    return array

def arrToStr(array):
    string = ""
    for i in array:
        string += str(i) + ","
    return string

class Node:
    def __init__(self, strengths, layer, bias, output):
        self.strengths = strengths
        self.layer = layer
        self.bias = bias
        self.output = output

    def mutateStrength(self, inputNode):
        newStrength = random() - 0.5
        self.strengths[inputNode] += newStrength
        if self.strengths[inputNode] > 1:
            self.strengths[inputNode] = 1
        if self.strengths[inputNode] < -1:
            self.strengths[inputNode] = -1

    def setOutput(self, nestingNetwork):
            sum = self.bias
            for i in range(len(self.strengths)):
                sum += nestingNetwork.layers[self.layer - 1][i].output * self.strengths[i]
            self.output = sig(sum)


class Network:
    def __init__(self, widths):
        self.widths = widths[:]
        self.layers = []
        self.outputs = []
        for i in range(len(self.widths)):
            self.layers.append([])

    def createInputLayer(self, inputArray):
        self.layers[0] = []
        for bit in inputArray:
            self.addNode(False, 0, 0, bit)
    
    def createHiddenLayers(self):
        for layer in range(1, len(self.widths)):
            for width in range(self.widths[layer]):
                self.addNode(sizedArray(self.widths[layer - 1], 0), layer, 0, 0)

    def clone(self):
        clone = Network(self.widths[:])
        for i in range(1, len(self.widths)):
            for j in range(self.widths[i]):
                clone.addNode(self.layers[i][j].strengths[:], i, self.layers[i][j].bias, 0)
        return clone

    def addNode(self, strengths, layer, bias, output):
        self.layers[layer].append(Node(strengths, layer, bias, output))

    def fireLayer(self, layer):
        for i in range(self.widths[layer]):
            self.layers[layer][i].setOutput(self)

    def runNetwork(self):
        for i in range(1, len(self.widths)):
            self.fireLayer(i)
        self.outputs = []
        for i in range(self.widths[len(self.widths) - 1]):
            self.outputs.append(self.layers[len(self.widths) - 1][i].output)
    
    def exportNetwork(self):
        exportedNetwork = []
        exportedNetwork.append(self.widths.length)
        for i in self.widths:
            exportedNetwork.append(i)
        for i in self.layers:
            for j in i:
                exportedNetwork.append(j.bias);
                for k in j.strengths:
                    exportedNetwork.append(k);
        return exportedNetwork

    # Does not include importNetwork

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
    array = [100, 5, 5, 1]
    network = Network(array)
    network.createHiddenLayers()
    network = mutate(network, 0.5)
    return network

generation = []
for i in range(200):
    generation.append(newNetwork())

generationNumber = 0
while True:
    generationNumber += 1
    fitness = sizedArray(len(generation), 0)
    for t in range(6144):
        getNewQuestion()
        for i in range(200):
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
    for i in range(195):
        generation.append(mutate(generation[i % 5], -highestFitness / 3072 + 2))


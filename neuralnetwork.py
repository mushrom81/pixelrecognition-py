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
        clone = Network(self.widths)
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
        exportedNetwork.append(len(self.widths))
        for i in self.widths:
            exportedNetwork.append(i)
        for i in self.layers[1:]:
            for j in i:
                exportedNetwork.append(j.bias)
                for k in j.strengths:
                    exportedNetwork.append(k)
        return exportedNetwork

    def importNetwork(self, exportedNetwork):
        self.outputs = []
        self.widths = []
        self.layers = [[]]
        networkSize = int(exportedNetwork[0])
        exportedNetwork = exportedNetwork[1:]
        for i in range(networkSize):
            self.widths.append(int(exportedNetwork[0]))
            exportedNetwork = exportedNetwork[1:]
        for i in range(1, networkSize):
            self.layers.append([])
            for j in range(self.widths[i]):
                nodeBias = exportedNetwork[0]
                exportedNetwork = exportedNetwork[1:]
                nodeStrengths = []
                for k in range(self.widths[i - 1]):
                    nodeStrengths.append(exportedNetwork[0])
                    exportedNetwork = exportedNetwork[1:]
                self.addNode(nodeStrengths, i, nodeBias, 0)

import numpy as np
import time as time
import random
import copy
from pprint import pprint


#Individual class
class Individual:
    def __init__(self, genoma, event):
        self.genes = np.zeros((28,6))
        self.genoma = genoma
        self.event = event
        self.fitness = 0

        counter=0
        characters_available_dict = {
            0: 11, #Hank
            1: 11, #Diana
            2: 11, #Sheila
            3: 11, #Presto
            4: 11, #Bob
            5: 11, #Eric
        }
        for i in range(28): #inicializando todas as posições com 1 personagem
            randomIndex = random.randint(0, 5)
            #print('\nrandomIndex', randomIndex, 'i', i)
            self.genes[i][randomIndex] = 1
            characters_available_dict[randomIndex] -= 1
            if i== 27:
                characters_available_dict[randomIndex] -= 1 #removendo personagem da ultima etapa novamente para que ele não seja adicionado mais 10 vezes em entapas anteriores 
        while (characters_available_dict[0] > 0 or characters_available_dict[1] > 0 or characters_available_dict[2] > 0 or characters_available_dict[3] > 0 or characters_available_dict[4] > 0 or characters_available_dict[5] > 0):
            randomIndex = random.randint(0, 5)
            randomIndividualIndex = random.randint(0, len(self.genes)-1)
            if self.genes[randomIndividualIndex][randomIndex] == 0 and characters_available_dict[randomIndex] > 0:
                self.genes[randomIndividualIndex][randomIndex] = 1
                characters_available_dict[randomIndex] -= 1
            else:
                
                while (self.genes[randomIndividualIndex][randomIndex] == 1 or characters_available_dict[randomIndex] == 0):
                    randomIndex = random.randint(0, 5)
                    randomIndividualIndex = random.randint(0, len(self.genes)-1)
                self.genes[randomIndividualIndex][randomIndex] = 1
                characters_available_dict[randomIndex] -= 1
        counter += 1
        
        self.fitness=self.calcFitness()
        
    #Calculate fitness
    def calcFitness(self):
        total_time = 0
        eventCounter = 1
        for groupIndex in range(len(self.genes)):
            agitili_sum = 0
            for character_index in range(len(self.genes[groupIndex])):
                if self.genes[groupIndex][character_index] == 1.0:
                    agitili_sum += self.genoma[character_index]['agility']
            t = self.event[eventCounter]['difficulty']/agitili_sum
            total_time += t
            eventCounter += 1
        return 10000/total_time

#Population class
class Population:
    def __init__(self):
        self.popSize = 10
        self.individuals = [None]*self.popSize
        self.fittest = 0
        self.events = readFile('caverna_dragao_v2.txt')[1]
        self.characters = {0:{'agility':1.5}, 1:{'agility':1.4}, 2:{'agility':1.3}, 3:{'agility':1.2}, 4:{'agility':1.1}, 5:{'agility':1.0}}

        self.individuals = self.createPopulation()

    def createPopulation(self):
        #1) criar a população 
        counter=0
        population = []
        while counter < self.popSize:
            individuo = Individual(event = self.events, genoma=self.characters)
            population.append(individuo.genes.tolist())
            counter += 1
            #print(characters_available_dict)
        return population

#Main class
class SimpleDemoGA:
    def __init__(self):
        self.population = Population()
        self.fittest = None
        self.secondFittest = None
        self.generationCount = 0


    def Roleta(population_dict):
        roleta = []
        fitness_sum = 0
        for key in population_dict.keys():
            fitness_sum += population_dict[key]['fitness']
        r = random.uniform(0,1)
        for key in population_dict.keys():
            pi = population_dict[key]['fitness']/fitness_sum
            if r < pi:
                return key
            else:
                r -= pi
        pprint( roleta)

    def selection(self):
        #Select the most fittest individual
        self.fittest = self.population.getFittest()

        #Select the second most fittest individual
        self.secondFittest = self.population.getSecondFittest()

    def crossover(self):
        #Select a random crossover point
        crossOverPoint = random.randint(0, self.population.individuals[0].geneLength-1)

        #Swap values among parents
        for i in range(crossOverPoint):
            temp = self.fittest.genes[i]
            self.fittest.genes[i] = self.secondFittest.genes[i]
            self.secondFittest.genes[i] = temp
    
    def mutation(self):
        # Select a random mutation point
        mutationPoint = random.randint(0, len(self.population.individuals[0].genes) - 1)

        # Flip values at the mutation point
        if self.fittest.genes[mutationPoint] == 0:
            self.fittest.genes[mutationPoint] = 1
        else:
            self.fittest.genes[mutationPoint] = 0

        mutationPoint = random.randint(0, len(self.population.individuals[0].genes) - 1)

        if self.secondFittest.genes[mutationPoint] == 0:
            self.secondFittest.genes[mutationPoint] = 1
        else:
            self.secondFittest.genes[mutationPoint] = 0

    # Get fittest offspring
    def getFittestOffspring(self):
        if self.fittest.fitness > self.secondFittest.fitness:
            return self.fittest
        return self.secondFittest

    # Replace least fittest individual from most fittest offspring
    def addFittestOffspring(self):
        # Update fitness values of offspring
        self.fittest.calcFitness()
        self.secondFittest.calcFitness()

        # Get index of least fit individual
        self.leastFittestIndex = self.population.getLeastFittestIndex()

        # Replace least fittest individual from most fittest offspring
        self.population.individuals[self.leastFittestIndex] = self.getFittestOffspring()

def readFile(file):
    file = open(file, 'r')
    map = []
    auxArray = []
    nodeCounter=0
    eventsDict={}
    while 1:
        char = file.read(1)
        if char == '\n':
            map.append(auxArray)
            auxArray = [] 
        elif char==".":
            auxArray.append("1")
            nodeCounter+=1
        elif char=="R":
            auxArray.append("5")
            nodeCounter+=1
        elif char=="D":
            auxArray.append("10")
            nodeCounter+=1
        elif char=="F" or char =="f":
            auxArray.append("15")
            nodeCounter+=1
        elif char=="A":
            auxArray.append("20")
            nodeCounter+=1
        elif char=="M":
            auxArray.append("100")
            nodeCounter+=1
        elif char:
            match char:
                case "1":
                    eventsDict[1] = {'node': nodeCounter, 'label': 'Helix', 'stage':'1', 'difficulty':10}
                case "2":
                    eventsDict[2] = {'node': nodeCounter, 'label': 'Valley of the Beholder','stage':'2', 'difficulty':20}
                case "3":
                    eventsDict[3] =  {'node': nodeCounter, 'label': 'Hall of Bones', 'stage':'3', 'difficulty':30}
                case "4":
                    eventsDict[4] = {'node': nodeCounter, 'label': 'Valley of the Unicorns', 'stage':'4', 'difficulty':60}
                case "5":
                    eventsDict[5] = {'node': nodeCounter, 'label': 'Slavemindes of Baltimore', 'stage':'5', 'difficulty':65}
                case "6":
                    eventsDict[6] = {'node': nodeCounter, 'label': 'Swap of Sorrows', 'stage':'6', 'difficulty':70}
                case "7":
                    eventsDict[7] = {'node': nodeCounter, 'label': 'Prison of Agony', 'stage':'7', 'difficulty':75}
                case "8":
                    eventsDict[8] = {'node': nodeCounter, 'label': 'Valley of the Bogbeasts', 'stage':'8', 'difficulty':80}
                case "9":
                    eventsDict[9] = {'node': nodeCounter, 'label': 'Tower of the Celestial Knights', 'stage':'9', 'difficulty':85}
                case "B":
                    eventsDict[10] = {'node': nodeCounter, 'label': 'City of Zinn', 'stage':'B', 'difficulty':90}
                case "C":
                    eventsDict[11] = {'node': nodeCounter, 'label': 'Skull Montain', 'stage':'C', 'difficulty':95}
                case "E":
                    eventsDict[12] = {'node': nodeCounter, 'label': 'Forest of the Lost Children', 'stage':'E', 'difficulty':100}
                case "G":
                    eventsDict[13] = {'node': nodeCounter, 'label': 'Disaster"	Floating Island', 'stage':'G', 'difficulty':110}
                case "H":
                    eventsDict[14] = {'node': nodeCounter, 'label': 'The maze of Darkness', 'stage':'H', 'difficulty':120}
                case "I":
                    eventsDict[15] = {'node': nodeCounter, 'label': 'Tardos Keep', 'stage':'I', 'difficulty':130}
                case "J":
                    eventsDict[16] = {'node': nodeCounter, 'label': 'Oasis of no Return', 'stage':'J', 'difficulty':140}
                case "K":
                    eventsDict[17] = {'node': nodeCounter, 'label': 'Cloud Forest', 'stage':'K', 'difficulty':150}
                case "L":
                    eventsDict[18] = {'node': nodeCounter, 'label': 'Darkhaven', 'stage':'L', 'difficulty':160}
                case "N":
                    eventsDict[19] = {'node': nodeCounter, 'label': 'Forbidden Tower', 'stage':'N', 'difficulty':170}
                case "O":
                    eventsDict[20] = {'node': nodeCounter, 'label': 'Great Glaciers', 'stage':'O', 'difficulty':180}
                case "P":
                    eventsDict[21] = {'node': nodeCounter, 'label': 'City of Turodh', 'stage':'P', 'difficulty':190}
                case "Q":
                    eventsDict[22] = {'node': nodeCounter, 'label': 'Tower of Darkness', 'stage':'Q', 'difficulty':200}
                case "S":
                    eventsDict[23] = {'node': nodeCounter, 'label': 'Citadel of Shadow', 'stage':'S', 'difficulty':210}
                case "T":
                    eventsDict[24] = {'node': nodeCounter, 'label': 'Tower of Chronos', 'stage':'T', 'difficulty':220}
                case "U":
                    eventsDict[25] = {'node': nodeCounter, 'label': 'Human Tribes', 'stage':'U', 'difficulty':230}
                case "W":
                    eventsDict[26] = {'node': nodeCounter, 'label': 'Grotto of Darkness', 'stage':'W', 'difficulty':240}
                case "Y":
                    eventsDict[27] = {'node': nodeCounter, 'label': 'Cave of the Fairy Dragons', 'stage':'Y', 'difficulty':250}
                case "Z":
                    eventsDict[28] = {'node': nodeCounter, 'label': 'Abyss', 'stage':'Z', 'difficulty':260}
                case "_":
                    print('Erro ao determinar o evento')
            auxArray.append("1")
            nodeCounter += 1
        if not char:
            break
    file.close()
    return (map,eventsDict)



def createGraph(weightMatrix):
    #print(weightMatrix)
    matrixHeight = len(weightMatrix)
    matrixWidht = len(weightMatrix[0])
    adjMatrix = np.zeros((matrixHeight*matrixWidht,matrixHeight*matrixWidht))
    nodeCounter = 0
    for i in range(matrixHeight):
        for j in range(matrixWidht):
            currentNode = (i,j)
            neighbours = getNeighbours(i,j,matrixHeight,matrixWidht)
            #print('curent node: ',currentNode, 'neighbours :', neighbours)
            for element in neighbours:
                adjMatrix[nodeCounter][element[0]*matrixWidht+element[1]] = weightMatrix[element[0]][element[1]]
            nodeCounter += 1
    
    return adjMatrix

def createDistanceMatrix(matrix):
    startTime = time.time()
    matrixHeight = len(matrix)
    matrixWidht = len(matrix[0])
    heuristic = []
    for i in range (matrixHeight):
        for j in range (matrixWidht):
            auxArray = []
            currentNode = (i,j)
            for k in range (matrixHeight):
                for l in range (matrixWidht):
                    probedNode = (k,l)
                    distance = abs(currentNode[0]-probedNode[0]) + abs(currentNode[1]-probedNode[1])
                    auxArray.append(distance) 
            heuristic.append(auxArray)
    #print('Tempo de execução da função createDistanceMatrix: ', time.time()-startTime)
    return heuristic


def getNeighbours(i,j,matrixHeight,matrixWidht):
    neighbours = []
    if (i != 0 and j!=0) and (i != (matrixHeight-1) and j!= (matrixWidht-1) ): #nós com 4 vizinhos
        neighbours.append((i,j-1)) # <-
        neighbours.append((i,j+1)) # ->
        neighbours.append((i-1,j)) #  ^
        neighbours.append((i+1,j)) #  
                #print('1')
    else:
        if (i ==0 and j==0): #Quina superior Esquerda
            neighbours.append((i,j+1))
            neighbours.append((i+1,j))
            #print('2')

        if (i == matrixHeight-1 and j== matrixWidht-1): #Quina inferior direita
            neighbours.append((i-1,j))
            neighbours.append((i,j-1))
            #print('3')

        if (i ==0 and j== matrixWidht-1): #Quina superior direita
            neighbours.append((i,j-1))
            neighbours.append((i+1,j))
            #print('4')

        if (i == matrixHeight-1 and j==0): #Quina inferior esquerda
            neighbours.append((i,j+1))
            neighbours.append((i-1,j))
            #print('5')


        if i==0 and j != 0 and j!= matrixWidht -1:                     
            neighbours.append((i,j-1))
            neighbours.append((i,j+1)) 
            neighbours.append((i+1,j))
            #print('6')
        if j==0 and i != 0 and i!= matrixHeight -1:
            neighbours.append((i-1,j))
            neighbours.append((i+1,j))
            neighbours.append((i,j+1))
            #print('7')
        if i == matrixHeight-1 and j != 0 and j!= matrixWidht -1:
            neighbours.append((i-1,j))
            neighbours.append((i,j+1))
            neighbours.append((i,j-1))
            #print('8')
        if j == matrixWidht-1 and i != 0 and i!= matrixHeight -1:
            neighbours.append((i-1,j))
            neighbours.append((i+1,j))
            neighbours.append((i,j-1))
            #print('9cl')
    return neighbours



def a_star(graph, heuristic, start, goal):
    """
    Finds the shortest distance between two nodes using the A-star (A*) algorithm
    :param graph: an adjacency-matrix-representation of the graph where (x,y) is the weight of the edge or 0 if there is no edge.
    :param heuristic: an estimation of distance from node x to y that is guaranteed to be lower than the actual distance. E.g. straight-line distance
    :param start: the node to start from.
    :param goal: the node we're searching for
    :return: The shortest distance to the goal node and the best path.
    """
    # This contains the distances from the start node to all other nodes, initialized with a distance of "Infinity"
    distances = [float("inf")] * len(graph)

    # The distance from the start node to itself is of course 0
    distances[start] = 0

    # This contains the priorities with which to visit the nodes, calculated using the heuristic.
    priorities = [float("inf")] * len(graph)

    # start node has a priority equal to straight line distance to goal. It will be the first to be expanded.
    priorities[start] = heuristic[start][goal]
    # This contains whether a node was already visited
    visited = [False] * len(graph)

    # This contains the previous node on the best path from start to each node
    previous = [-1] * len(graph)

    # While there are nodes left to visit...
    while True:
        # ... find the node with the currently lowest priority...
        lowest_priority = float("inf")
        lowest_priority_index = -1
        for i in range(len(priorities)):
            # ... by going through all nodes that haven't been visited yet
            if priorities[i] < lowest_priority and not visited[i]:
                lowest_priority = priorities[i]
                lowest_priority_index = i

        if lowest_priority_index == -1:
            # There was no node not yet visited --> Node not found
            return -1, []

        elif lowest_priority_index == goal:
            # Goal node found
            # print("Goal node found!")
            # Construct the best path
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = previous[node]
            path.append(start)
            path.reverse()
            return distances[lowest_priority_index], path

        # ...then, for all neighboring nodes that haven't been visited yet....
        for i in range(len(graph[lowest_priority_index])):
            if graph[lowest_priority_index][i] != 0 and not visited[i]:
                # ...if the path over this edge is shorter...
                if distances[lowest_priority_index] + graph[lowest_priority_index][i] < distances[i]:
                    # ...save this path as new shortest path
                    distances[i] = distances[lowest_priority_index] + graph[lowest_priority_index][i]
                    # ...and set the priority with which we should continue with this node
                    priorities[i] = distances[i] + heuristic[i][goal]
                    # Update the previous node
                    previous[i] = lowest_priority_index

        # Lastly, note that we are finished with this node.
        visited[lowest_priority_index] = True


def Roleta(population_dict):
    roleta = []
    fitness_sum = 0
    for key in population_dict.keys():
        fitness_sum += population_dict[key]['fitness']
    r = random.uniform(0,1)
    for key in population_dict.keys():
        pi = population_dict[key]['fitness']/fitness_sum
        if r < pi:
            return key
        else:
            r -= pi
    pprint( roleta)
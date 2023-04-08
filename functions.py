import numpy as np

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
                    eventsDict[1] = {'node': nodeCounter, 'label': 'Helix'}
                case "2":
                    eventsDict[2] = {'node': nodeCounter, 'label': 'Valley of the Beholder'}
                case "3":
                    eventsDict[3] =  {'node': nodeCounter, 'label': 'Hall of Bones'}
                case "4":
                    eventsDict[4] = {'node': nodeCounter, 'label': 'Valley of the Unicorns'}
                case "5":
                    eventsDict[5] = {'node': nodeCounter, 'label': 'Slavemindes of Baltimore'}
                case "6":
                    eventsDict[6] = {'node': nodeCounter, 'label': 'Swap of Sorrows'}
                case "7":
                    eventsDict[7] = {'node': nodeCounter, 'label': 'Prison of Agony'}
                case "8":
                    eventsDict[8] = {'node': nodeCounter, 'label': 'Valley of the Bogbeasts'}
                case "9":
                    eventsDict[9] = {'node': nodeCounter, 'label': 'Tower of the Celestial Knights'}
                case "B":
                    eventsDict[10] = {'node': nodeCounter, 'label': 'City of Zinn'}
                case "C":
                    eventsDict[11] = {'node': nodeCounter, 'label': 'Skull Montain'}
                case "E":
                    eventsDict[12] = {'node': nodeCounter, 'label': 'Forest of the Lost Children'}
                case "G":
                    eventsDict[13] = {'node': nodeCounter, 'label': 'Disaster"	Floating Island'}
                case "H":
                    eventsDict[14] = {'node': nodeCounter, 'label': 'The maze of Darkness'}
                case "I":
                    eventsDict[15] = {'node': nodeCounter, 'label': 'Tardos Keep'}
                case "J":
                    eventsDict[16] = {'node': nodeCounter, 'label': 'Oasis of no Return'}
                case "K":
                    eventsDict[17] = {'node': nodeCounter, 'label': 'Cloud Forest'}
                case "L":
                    eventsDict[18] = {'node': nodeCounter, 'label': 'Darkhaven'}
                case "N":
                    eventsDict[19] = {'node': nodeCounter, 'label': 'Forbidden Tower'}
                case "O":
                    eventsDict[20] = {'node': nodeCounter, 'label': 'Great Glaciers'}
                case "P":
                    eventsDict[21] = {'node': nodeCounter, 'label': 'City of Turodh'}
                case "Q":
                    eventsDict[22] = {'node': nodeCounter, 'label': 'Tower of Darkness'}
                case "S":
                    eventsDict[23] = {'node': nodeCounter, 'label': 'Citadel of Shadow'}
                case "T":
                    eventsDict[24] = {'node': nodeCounter, 'label': 'Tower of Chronos'}
                case "U":
                    eventsDict[25] = {'node': nodeCounter, 'label': 'Human Tribes'}
                case "W":
                    eventsDict[26] = {'node': nodeCounter, 'label': 'Grotto of Darkness'}
                case "Y":
                    eventsDict[27] = {'node': nodeCounter, 'label': 'Cave of the Fairy Dragons'}
                case "Z":
                    eventsDict[28] = {'node': nodeCounter, 'label': 'Abyss'}
                case "_":
                    print('Erro ao determinar o evento')
            auxArray.append("0")
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
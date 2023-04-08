import numpy as np

def FileToWeightMatrix(file):
    file = open(file, 'r')
    adjMatrix = []
    auxArray = []
    no=0
    dicionario={}
    while 1:
        char = file.read(1)
        if char == '\n':
            adjMatrix.append(auxArray)
            auxArray = [] 
        elif char==".":
            auxArray.append("1")
            no+=1
            dicionario["."] = no
        elif char=="R":
            auxArray.append("5")
            no+=1
            dicionario["R"] = no
        elif char=="D":
            auxArray.append("10")
            no+=1
            dicionario["D"] = no
        elif char=="F" or char =="f":
            auxArray.append("15")
            no+=1
            dicionario["F"] = no
        elif char=="A":
            auxArray.append("20")
            no+=1
            dicionario["A"] = no
        elif char=="M":
            auxArray.append("100")
            no+=1
            dicionario["M"] = no
        elif char=="B" or char=="b" or char=="C" or char=="E" or char=="G"or char=="H"or char=="I"or char=="J"or char=="K"or char=="L"or char=="N"or char=="O"or char=="P"or char=="Q"or char=="S"or char=="T"or char=="U"or char=="W"or char=="Y"or char=="Z":
            no+=1
            match char:
                case "B":
                    dicionario["B"] = no
                case "E":
                    dicionario["E"] = no
                case "G":
                    dicionario["G"] = no
                case "H":
                    dicionario["H"] = no
                case "I":
                    dicionario["I"] = no
                case "J":
                    dicionario["J"] = no
                case "K":
                    dicionario["K"] = no
                case "L":
                    dicionario["L"] = no
                case "N":
                    dicionario["N"] = no
                case "O":
                    dicionario["O"] = no
                case "P":
                    dicionario["P"] = no
                case "Q":
                    dicionario["Q"] = no
                case "S":
                    dicionario["S"] = no
                case "T":
                    dicionario["T"] = no
                case "U":
                    dicionario["U"] = no
                case "Y":
                    dicionario["Y"] = no
                case "Z":
                    dicionario["Z"] = no
                case "b":
                    dicionario["b"] = no

            auxArray.append("0")
        else:       
            auxArray.append(char)
        if not char:
            break
    file.close()
    print(dicionario)
    return adjMatrix



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
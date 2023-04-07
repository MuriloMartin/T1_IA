from functions import *


weightMatrix = FileToWeightMatrix('testeAlgo.txt')
adjMatrix = createGraph(weightMatrix)
heuristic = createDistanceMatrix(weightMatrix)

#print(heuristic)

start = 0
goal = 61

shortest = a_starV2(adjMatrix,heuristic,start,goal)

print(shortest)



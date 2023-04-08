from functions import *


#weightMatrix = FileToWeightMatrix('testeAlgo.txt')
#adjMatrix = createGraph(weightMatrix)
#heuristic = createDistanceMatrix(weightMatrix)

weightMatrix = FileToWeightMatrix('caverna_dragao_v2.txt')
adjMatrix = createGraph(weightMatrix)
heuristic = createDistanceMatrix(weightMatrix)
#converted = ConvertCharToWeight(weightMatrix)
#print(converted)
#print(weightMatrix)

start = 0
goal = 61

shortest = a_star(adjMatrix,heuristic,start,goal)

print(shortest)




from functions import *


fileData = readFile('caverna_dragao_v2.txt')
weightMatrix = fileData[0]
eventsDict = fileData[1]
adjMatrix = createGraph(weightMatrix)
heuristic = createDistanceMatrix(weightMatrix)
#print('heuristic : ',heuristic)
#print('eventsDict : ',eventsDict)
#print('weightMatrix : ',weightMatrix)


# print('eventsDict : ',eventsDict)
# for i in range (2,29):
#     if i == 11 or i == 12 or i==28: #Faltou o "C" e o "Z" no arquivo do mapa
#         break
#     goal = eventsDict[i]
#     start = eventsDict[i-1]
#     print('Calculando entre : %s e %s\n' % (start['label'], goal['label']))
#     shortest = a_star(adjMatrix,heuristic,start['node'],goal['node'])[0]
#     print('Caminho menos custoso entre : %s e %s : %d \n' % (start['label'], goal['label'], shortest))

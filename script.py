from functions import *


fileData = readFile('caverna_dragao_v2.txt')
weightMatrix = fileData[0]
eventsDict = fileData[1]
adjMatrix = createGraph(weightMatrix)
heuristic = createDistanceMatrix(weightMatrix)
# print('heuristic : ',heuristic)
# #print('eventsDict : ',eventsDict)
# print('weightMatrix : ',weightMatrix)
print('adjMatrix : ',adjMatrix)

for i in range (2,28):
    if i == 11 or i == 12 or i==28: #Faltou o "C" e o "Z" no arquivo do mapa
        break
    goal = eventsDict[i]
    start = eventsDict[i-1]
    print('\n\n\ngoal',goal['node'])
    print('start',start['node'])
    print('Calculando entre : %s e %s\n' % (start['label'], goal['label']))
    results = a_star(adjMatrix,heuristic,start['node'],goal['node'])
    path = results[1]
    shortest = results[0]
    print('Caminho menos custoso entre : %s e %s : %d \n' % (start['label'], goal['label'], shortest))
    print('Caminho : ',path)

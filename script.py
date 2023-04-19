from functions import *


fileData = readFile('caverna_dragao_v2.txt')
weightMatrix = fileData[0]
eventsDict = fileData[1]
'''
adjMatrix = createGraph(weightMatrix)
heuristic = createDistanceMatrix(weightMatrix)
# print('heuristic : ',heuristic)
# #print('eventsDict : ',eventsDict)
# print('weightMatrix : ',weightMatrix)
# print('adjMatrix : ',adjMatrix)
'''
'''
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

'''
charactersDict = {
    'Hank':{'agility':1.5},
    'Diana':{'agility':1.4},
    'Sheila':{'agility':1.3},
    'Presto':{'agility':1.2},
    'Bob':{'agility':1.1},
    'Eric':{'agility':1.0}
}

characters = [{'name':'Hank','agility':'1.5', 'energy_points':11}, {'name':'Diana','agility':'1.4', 'energy_points':11}, {'name':'Sheila','agility':'1.3', 'energy_points':11}, 
              {'name':'Presto','agility':'1.2', 'energy_points':11}, {'name':'Bob','agility':'1.1', 'energy_points':11}, {'name':'Etic','agility':'1.0', 'energy_points':11}]

#characters = ['Hank','Diana','Sheila','Presto','Bob','Eric']

charactersAvailable = ['Hank','Hank','Hank','Hank','Hank','Hank','Hank','Hank','Hank','Hank','Hank','Diana','Diana','Diana','Diana','Diana','Diana','Diana','Diana','Diana','Diana','Diana','Sheila','Sheila','Sheila','Sheila','Sheila','Sheila','Sheila','Sheila','Sheila','Sheila','Sheila','Presto','Presto','Presto','Presto','Presto','Presto','Presto','Presto','Presto','Presto','Presto','Bob','Bob','Bob','Bob','Bob','Bob','Bob','Bob','Bob','Bob','Bob','Eric','Eric','Eric','Eric','Eric','Eric','Eric','Eric','Eric','Eric','Eric']

# Run the genetic algorithm
population = genetic(charactersAvailable)
#print('population : ',population)
# Print the best solution

# for individuo in population:
print('Fitness : ',fitnessFunction(population[0],charactersDict,eventsDict))



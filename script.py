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
    0:{'agility':1.5}, #Hank
    1:{'agility':1.4}, #Diana
    2:{'agility':1.3}, #Sheila
    3:{'agility':1.2}, #Presto
    4:{'agility':1.1}, #Bob
    5:{'agility':1.0} #Eric
}

characters = [{'name':'Hank','agility':'1.5', 'energy_points':11}, {'name':'Diana','agility':'1.4', 'energy_points':11}, {'name':'Sheila','agility':'1.3', 'energy_points':11}, 
              {'name':'Presto','agility':'1.2', 'energy_points':11}, {'name':'Bob','agility':'1.1', 'energy_points':11}, {'name':'Etic','agility':'1.0', 'energy_points':11}]


# Run the genetic algorithm

population = createPopulation(50)
#print('population : ',population)
# find fitest


####################################
# population_dict => dicinário com chaves numericas. cada chave representa um individuo. O valor de cada chave é um dict da forma {genoma: "string_com_o_genoma", fitness: valor_de_fitness}
# a string_com_o_genoma é gerada a partir de cada individuo (simplismente a transformação da lista com 28 sublistas  em uma string contendo a mesma informação)

population_dict = {}
for individuo_index in range(len(population)): #len(population)
    string_genoma = ''
    for sublist in population[individuo_index]:
        #print('sublist : ',sublist)
        for bit in sublist:
            string_genoma += str(int(bit))
        #print('tamanho da string : ',len(string_genoma)) # 28*6 = 168
    population_dict[individuo_index] = {'genoma':string_genoma,'fitness':fintess_function(population[individuo_index],charactersDict,eventsDict)}
    #population_dict[individuo_index]

pprint(population_dict)
print('\n\n')
#################################

############################################################################
#teste: forçando 10 dos indivudos a serem muito bons, eles devem ser escolhidos mais vezes
for i in range(40,50):
    population_dict[i]['fitness'] = 25 #se quiser pode testar 50, 100 ou 1000... vai ver que ele relamente é selecionado com mais frequencia
############################################################################

individuo_selecionado = Roleta(population_dict)
print('individuo_selecionado : ')
pprint(population_dict[individuo_selecionado])

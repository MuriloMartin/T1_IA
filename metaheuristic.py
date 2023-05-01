import numpy as np
from search_algorithm import readFile
import random

eventsDict = readFile('caverna_dragao_v2.txt')[1]

class Individual:
    def __init__(self, charactersDict, genesRecieved = []):
        self.genes = np.zeros((28,6))
        self.geneLength = 28
        self.charactersDict = charactersDict
        #self.event = event
        self.fitness = 0


        characters_available_dict = {
            0: 11, #Hank
            1: 11, #Diana
            2: 11, #Sheila
            3: 11, #Presto
            4: 11, #Bob
            5: 11, #Eric
        }

        if not len(genesRecieved) > 0:
            #creating individual
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

        else:
            self.genes = genesRecieved

        self.fitness=self.calcFitness()
        
    #Calculate fitness
    def calcFitness(self):
        total_time = 0
        eventCounter = 1
        for groupIndex in range(len(self.genes)):
            agitili_sum = 0
            for character_index in range(len(self.genes[groupIndex])):
                if self.genes[groupIndex][character_index] == 1.0:
                    agitili_sum += self.charactersDict[character_index]['agility']
            t = eventsDict[eventCounter]['difficulty']/agitili_sum
            total_time += t
            eventCounter += 1
        return 10000/total_time
    
    def isViable(self):
        counterDict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
        eventCounter = 0
        last_event_characters = []
        for sub_lista in self.genes:
            for i in range(6):
                if eventCounter == 27:
                    if sub_lista[i] == 1.0:
                        counterDict[i]+= 1
                        last_event_characters.append(i)
                        
                elif sub_lista[i] == 1.0:
                   counterDict[i] += 1
            eventCounter += 1
            

       
        one_character_survives = False
        for key in last_event_characters:
            if counterDict[key] < 11:
                one_character_survives = True
        
        if one_character_survives:
            for key in counterDict.keys():
                if counterDict[key]> 11:
                    return False
                if key in last_event_characters and counterDict[key]<10:
                    return False
                if counterDict[key]<11 and key not in last_event_characters:
                     return False
            #print('\n\ncounterDict : ', counterDict)
            for key in last_event_characters:
                if counterDict[key] == 10:
                    remaining_keys = last_event_characters.copy()
                    remaining_keys.remove(key)
                    for remaining_key in remaining_keys:
                        if counterDict[remaining_key] <11:
                            return False
                    

            return True
            
        else:
            return False
        
#Population class   
class Population:
    def __init__(self, individualsReceived = []):
        self.popSize = 2000
        self.fittest = 0
        #self.eventsDict = readFile('caverna_dragao_v2.txt')[1]
        self.characters = {0:{'agility':1.5}, 1:{'agility':1.4}, 2:{'agility':1.3}, 3:{'agility':1.2}, 4:{'agility':1.1}, 5:{'agility':1.0}}
        self.individuals = []
        self.fitness = 0

        if not len(individualsReceived) > 0:
            self.individuals = self.createPopulation()
        else:
            self.individuals = individualsReceived
        
        self.fitness = self.calculateFitnessPopulation()

    def createPopulation(self):
        #1) criar a população 
        counter=0
        population = []
        while counter < self.popSize:
            individuo = Individual( charactersDict=self.characters)
            population.append(individuo)
            counter += 1
        return population
    
    def calculateFitnessPopulation(self):
        popFit = 0
        for individuo in self.individuals:
            popFit += individuo.fitness
        return popFit
    
class SimpleDemoGA:
    def __init__(self):
        self.population = Population()
        self.individuoPai = None
        self.individuoMae = None
        self.individuoFilho = None

        self.bestIndividual = self.GA()

    def GA(self):
        MaxIndividuos = self.population.popSize
        MaxGeracoes = 50
        geracao = 0
        
        highestFitnessOverall = 0
        while geracao < MaxGeracoes:
            novaPopulacao = []
            individuos = 0
            
            while individuos < MaxIndividuos:
                self.individuoPai = self.Roleta()
                self.individuoMae = self.Roleta()
                self.individuoFilho = self.crossover()
                while (self.individuoFilho.isViable() == False):
                     self.individuoPai = self.Roleta()
                     self.individuoMae = self.Roleta()
                     self.individuoFilho = self.crossover()

                probMutacao = random.uniform(0, 1)
                if probMutacao <= 0.05:
                      self.mutation()
                        
                    
                novaPopulacao.append(self.individuoFilho)
                individuos += 1

            
            self.population = Population(individualsReceived=novaPopulacao)
            
            highestFitness = 0
            for individuo in novaPopulacao:
                if individuo.fitness > highestFitness:
                    highestFitness = individuo.fitness
                    bestIndividual = individuo
                if individuo.fitness > highestFitnessOverall:
                    highestFitnessOverall = individuo.fitness
                    bestIndividualOverall = individuo

            print("\nGeração %d: \n" %(geracao))
            print("Fitness da pop: %f " %(self.population.fitness))
            print("Mais rápido até agora: %f\n"%(10000/highestFitnessOverall))


           
            if geracao == (MaxGeracoes-1):
                print("Melhor fitness: %f\n" %(highestFitness))
                print('Melhor individuo: ', bestIndividual.genes)
                print('Melhor individuo overall: ', bestIndividualOverall.genes)
                print('Melhor fitness overall: ', highestFitnessOverall)
                print("Custo total do melhor: %f\n"%(10000/highestFitnessOverall))

                #for individual in self.population.individuals:
                       #print("Individuo é viavel? : %s" %(individual.isViable()))
            geracao += 1
            
        return bestIndividualOverall
        #return max(PopulacaoAtual, key=individuo.fitness) # retorna o individuo com maior fitness (máximo local)

    def Roleta(self):
        roleta = []
        fitness_sum = 0
        for individuo in self.population.individuals:
            fitness_sum += individuo.fitness
        r = random.uniform(0,1)
        for individuo in self.population.individuals:
            pi = individuo.fitness/fitness_sum
            if r < pi:
                return individuo
            else:
                r -= pi


    def crossover(self):
        # seleção do ponto de crossover
        
        pontoCorte = 1 #random.randint(1, self.individuoPai.geneLength-1)


        partePai = self.individuoPai.genes[:pontoCorte].tolist()
        parteMae = self.individuoMae.genes[pontoCorte:].tolist()
        # criação do filho
        new_genes = partePai + parteMae
        filho = Individual(charactersDict = self.population.characters, genesRecieved = np.array(new_genes))
        return filho
    
    def mutation(self):

        generated_viable_child = False
        genesCopy = self.individuoFilho.genes.copy()
        counter = 0
        #print('genes: ', self.individuoFilho.genes)
        randomPosition1 = random.randint(1, 26)
        randomPosition2 = random.randint(1,26)
        auxElement = self.individuoFilho.genes[randomPosition1]
        auxElement2 = self.individuoFilho.genes[randomPosition2]
        genesCopy[randomPosition1] = auxElement2
        genesCopy[randomPosition2] = auxElement
        counter += 1

        self.individuoFilho = Individual(charactersDict= self.individuoFilho.charactersDict, genesRecieved=genesCopy)
        

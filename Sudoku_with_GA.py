
import random
import datetime

random.seed()

# /////////////////////////////////////////////////////////////////////////////////////////////////           Funtions

def filler(input): # Filling the Input Table by Random Numbers With No Repeated Values in Each Row
    total = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ans = []
    input1 = list(input)
    input1 = [list(x) for x in input1]
    for c in range(9):
        tmp = input1[c].copy()
        for i, m in enumerate(input1[c]):
            the_list = [x for x in total if x not in tmp]
            if m == 0:
                tmp[i] = random.choice(the_list)
        ans.append(tmp)
    return ans

def zeros_maker(input): # Creating a List of Zeros' Index inside Input Table
    zeros = [[i for i in range(9) if j[i] == 0] for j in input]    
    return zeros

def state_maker(filled_input, zeros): # Extracting the State Out of The Filled Table
    state = []
    filled_input1 = filled_input.copy()
    for i in range(9):
        tmp = []
        for j in zeros[i]:
            tmp.append(filled_input1[i][j])
        state.append(tmp)
    return state

def mutation(child, p): # Mutation
    if random.random() < p:
        for i in range(9):
            if len(child[i]) > 1 and random.random() < p:
                positions = random.choices(range(len(child[i])), k=2)
                child[i][positions[0]], child[i][positions[1]] = child[i][positions[1]], child[i][positions[0]] 
    return child

def crossover(parent1, parent2): # Crossover
    child1 = []
    child2 = []
    for index in range(9):
        if len(parent1[index]) != 0:
            tmp1 = []
            tmp2 = []
            length = len(parent1[index])
            position = random.randint(1, length-1)
            tmp1.extend(parent1[index][:position])
            tmp2.extend(parent2[index][:position])
            for i1 in parent2[index]:
                if i1 not in tmp1:
                    tmp1.append(i1)
            for i2 in parent1[index]:
                if i2 not in tmp2:
                    tmp2.append(i2)
        child1.append(tmp1)
        child2.append(tmp2)
    return child1, child2

def substitute(state, input): # Substituting The Calculated State Inside The Input Table
    table = list(input)
    table = [list(x) for x in table]
    for i in range(9):
        counter = -1
        for j in range(9):
            if table[i][j] == 0:
                counter += 1
                table[i][j] = state[i][counter]
    return table

def fitness_vertical(parent, input): # Calculating Fitness Value According to The Columns Values
    count = 0
    input1 = input
    table = substitute(parent, input1)
    for j in range(9):
        tmp = []
        for i in range(9):
            tmp.append(table[i][j])
        count += (9-len(set(tmp)))
    return 81-count

def fitness_square(parent, input): # Calculating Fitness Value According to The 9 Squares Values
    count = 0
    input1 = input
    table = substitute(parent, input1)
    for k1 in range(0, 9, 3):
        for k2 in range(0, 9, 3):
            tmp = []
            for i in range(k1, k1+3):
                for j in range(k2, k2+3):
                    tmp.append(table[i][j])
            count += (9-len(set(tmp)))
    return 81-count

def fitness_horizontal(parent, input): # Calculating Fitness Value According to The Rows Values
    count = 0
    input1 = input
    table = substitute(parent, input1)
    for i in range(9):
        tmp = []
        for j in range(9):
            tmp.append(table[i][j])
        count += (9-len(set(tmp)))
    return 81-count

# /////////////////////////////////////////////////////////////////////////////////////////////////           Input Prepration

f = open('sample.txt', 'r')
#f = open('sample.txt', 'r')
#f = open('sample3.txt', 'r')

lines = []
for line in f.readlines():
    lines.append(line.split())

input = tuple([tuple([int(x) for x in y]) for y in lines])
#input = [[0,0,0,2,6,9,7,8,1],[6,0,2,0,7,1,4,9,0],[1,9,7,0,0,4,5,0,2],[8,2,6,0,9,5,0,4,7],[3,7,4,6,0,0,9,0,5],[0,5,0,7,4,3,6,2,8],[5,1,0,3,2,0,0,7,4],[2,4,8,9,5,0,1,0,6],[7,6,0,4,1,0,2,5,0]]
#answer = [[4,3,5,2,6,9,7,8,1],[6,8,2,5,7,1,4,9,3],[1,9,7,8,3,4,5,6,2],[8,2,6,1,9,5,3,4,7],[3,7,4,6,8,2,9,1,5],[9,5,1,7,4,3,6,2,8],[5,1,9,3,2,6,8,7,4],[2,4,8,9,5,7,1,3,6],[7,6,3,4,1,8,2,5,9]]

for i in input:
    print(i)

zeros = zeros_maker(input) # OR -> zeros = [[i for i in range(9) if j[i] == 0] for j in input]

# /////////////////////////////////////////////////////////////////////////////////////////////////           Genetic

# Setting Parameters
population = 16
generation_number = 1000
mutation_probability = 0.2

# Producing the Population
States_fitness = []
States = list()
for i in range(population):
    filled = filler(input)
    state = state_maker(filled, zeros)
    Fitness = fitness_horizontal(state, input) + fitness_vertical(state, input) + fitness_square(state, input)
    States.append(state)
    States_fitness.append(Fitness)
    #print('The State:', state, 'its fitness:', Fitness)

# Parents Selection
Parents = random.choices(States, weights=States_fitness, k=population)
print('........................................................................')

start = datetime.datetime.now()
Parents_fitness = []
for parent in Parents:
    Parents_fitness.append(fitness_horizontal(parent, input) + fitness_vertical(parent, input) + fitness_square(parent, input))

# Crossover and Mutation
flag = False
g = 0
while g < generation_number:
    Children = []
    for i in range(0, population-1, 2):
        tmp = crossover(Parents[i], Parents[i+1])
        for child in tmp:
            Children.append(mutation(child, mutation_probability))
    Children_fitness = []
    population_fitness = 0
    for child in Children:
        Fitness = fitness_horizontal(child, input) + fitness_vertical(child, input) + fitness_square(child, input)
        #print('The child:', child,'its fitness:', Fitness)
        population_fitness += Fitness
        if Fitness == 3 * 81:
            print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
            print('The Answer ->')
            for i in substitute(child, input):
                print(i)
            flag = True
            break
        Children_fitness.append(Fitness)
    if flag:
        break
    #print(f'-------------------sum={population_fitness}------------------------')
    #Parents = random.choices(Parents + Children, weights=Parents_fitness + Children_fitness, k=population) # Parents Selection
    Parents = random.choices(Children, weights=Children_fitness, k=population) # Parents Selection
    g += 1

print('Time spent:', datetime.datetime.now() - start)

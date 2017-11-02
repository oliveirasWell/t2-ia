import json
from pprint import pprint

def main():
    with open('train.json') as data_file:
        data = json.load(data_file)
    #print(data[0])
    ingredientes = []
    for j in data:
        ingredientes.append(j['ingredients'])
        todosOsIngredientes = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
            todosOsIngredientes.append((ingredientes[i][j]).lower())
    #print(len(ingredi))
    todosOsIngredientes = set(todosOsIngredientes)
    #print(len(ingredi))

    variaveis = []

    for i in data:
        aux = ""
        aux = aux + str(i['id']) + ", "
        for j in todosOsIngredientes:
            aux = aux + ('1, ' if j in i['ingredients'] else '0, ')
        aux = aux + i['cuisine'] + ", \n"
        variaveis.append(aux)
        print(aux)
    return



if __name__ == '__main__':
    main()
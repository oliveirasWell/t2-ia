import json
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors

def leArquivoJson():
    with open('train.json') as data_file1:
        dataTreino = json.load(data_file1)
    with open('test.json') as data_file2:
        dataTeste = json.load(data_file2)

    return dataTreino, dataTeste

def criarTodosOsIngrediente(dataTreino, dataTeste):

    # Acrescenta os ingredientes do conjunto de treino em ingredientes
    ingredientes = []
    for j in dataTreino:
        ingredientes.append(j['ingredients'])
    todosOsIngredientesTreino = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
            todosOsIngredientesTreino.append((ingredientes[i][j]))

    # Acrescenta os ingredientes do conjunto de teste em ingredientes
    ingredientes = []
    for j in dataTeste:
        ingredientes.append(j['ingredients'])
    todosOsIngredientesTeste = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
            todosOsIngredientesTeste.append((ingredientes[i][j]))

    todosOsIngredientesTreino = set(todosOsIngredientesTreino)
    todosOsIngredientesTeste = set(todosOsIngredientesTeste)

    #print(len(todosOsIngredientes))
    return todosOsIngredientesTreino

def criarXSYIDS(dicionarioDeJson, todosOsIngredientes):
    id = []
    xs = []
    y = []
    quant = []

    for j in todosOsIngredientes:
        cont = 0
        for i in dicionarioDeJson:
            if j in i['ingredients']:
                cont = cont + 1;
        quant.append(cont)

    quant, todosOsIngredientes = zip(*sorted(zip(quant, todosOsIngredientes)))

    ingredientesMaioresQue100 = []
    quantIngredientesMaioresQue100 = []

    for i in range (0, len(todosOsIngredientes)):
        if quant[i]>= 100:
            ingredientesMaioresQue100.append(todosOsIngredientes[i])
            quantIngredientesMaioresQue100.append(quant[i])

    for i in dicionarioDeJson:
        xIngredientes = []
        id.append(str(i['id']))
        for j in ingredientesMaioresQue100:
            if j in i['ingredients']:
                xIngredientes.append(1)
            else:
                xIngredientes.append(0)
        xs.append(xIngredientes)
        y.append(i['cuisine'])
    return xs, y, id

def main():
    dicionarioDeJsonTrieno, dicionarioDeJsonTEste = leArquivoJson()
    #print(dicionarioDeJson[0])
    todosOsIngredientes = criarTodosOsIngrediente(dicionarioDeJsonTrieno, dicionarioDeJsonTEste)

    #print(len(todosOsIngredientes))
    xs, y, id = criarXSYIDS(dicionarioDeJsonTrieno, todosOsIngredientes)
    #print(id[0])
    #print(xs[0])
    #print(y[0])
    X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.3, random_state=0)
    clf = neighbors.KNeighborsClassifier(15, weights='uniform')
    clf.fit(xs, y)
    maiorScore = clf.score(X_test, y_test)
    print("Melhores resultados: Weight: uniform, k = 15, Score: %f" % (maiorScore))
    return



if __name__ == '__main__':
    main()
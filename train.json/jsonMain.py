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

def criarTodosOsIngrediente(dataTreino):

    # Acrescenta os ingredientes do conjunto de treino em ingredientes
    ingredientes = []
    for j in dataTreino:
        ingredientes.append(j['ingredients'])
    todosOsIngredientesTreino = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
            todosOsIngredientesTreino.append((ingredientes[i][j]))


    todosOsIngredientesTreino = set(todosOsIngredientesTreino)

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

    #quant, todosOsIngredientes = zip(*sorted(zip(quant, todosOsIngredientes)))
    #print(quant)
    #print(todosOsIngredientes)
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

def retornaTeste(todosOsIngredientesTreino, dicionarioDeJsonTEste):
    for i in (dicionarioDeJsonTEste):
        xTeste = []
        for j in range(0, len(todosOsIngredientesTreino)):
            xTeste.append(0)
        for ingrediente in range (i['igredients']):
            for j in range(0, len(todosOsIngredientesTreino)):
                if ingrediente == todosOsIngredientesTreino[j]:
                    xTeste[j] = 1

def main():
    dicionarioDeJsonTrieno, dicionarioDeJsonTEste = leArquivoJson()

    todosOsIngredientesTreino = criarTodosOsIngrediente(dicionarioDeJsonTrieno)

    #print(len(todosOsIngredientes))
    xsTreino, yTreino, id = criarXSYIDS(dicionarioDeJsonTrieno, todosOsIngredientesTreino)

    #xsTeste, yTeste, idTeste = criarXSYIDS(dicionarioDeJsonTEste, todosOsIngredientesTeste)

    #print(id[0])
    #print(xs[0])
    #print(y[0])
    #X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.3, random_state=0)
    clf = neighbors.KNeighborsClassifier(15, weights='uniform')
    clf.fit(xsTreino, yTreino)
    maiorScore = clf.predict(X_test)
    print(maiorScore)
    #result_dict = dict(zip(id, maiorScore))
    print("Melhores resultados: Weight: uniform, k = 15, Score: %f" % (maiorScore))
    return



if __name__ == '__main__':
    main()
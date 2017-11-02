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
    with open('train.json') as data_file:
        data = json.load(data_file)
    print(len(data))
    return data

def criarTodosOsIngrediente(data):
    ingredientes = []
    for j in data:
        ingredientes.append(j['ingredients'])
        todosOsIngredientes = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
            todosOsIngredientes.append((ingredientes[i][j]).lower())
    # print(len(ingredi))
    todosOsIngredientes = set(todosOsIngredientes)
    return todosOsIngredientes

def criarXSYIDS(dicionarioDeJson, todosOsIngredientes):
    id = []
    xs = []
    y = []
    for i in dicionarioDeJson:
        xIngredientes = []
        id.append(str(i['id']))
        for j in todosOsIngredientes:
            if j in i['ingredients']:
                xIngredientes.append('1')
            else:
                xIngredientes.append('0')
        xs.append(xIngredientes)
        y.append(i['cuisine'])
    return xs, y, id

def main():
    dicionarioDeJson = leArquivoJson()
    #print(dicionarioDeJson[0])
    todosOsIngredientes = criarTodosOsIngrediente(dicionarioDeJson)
    print(len(todosOsIngredientes))
    #print(len(todosOsIngredientes))
    xs, y, id = criarXSYIDS(dicionarioDeJson, todosOsIngredientes)
    #print(id[0])
    print(xs[0])
    print(y[0])
    #X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.3, random_state=0)
    clf = neighbors.KNeighborsClassifier(15, weights='uniform')
    clf.fit(xs, y)
    maiorScore = clf.score(xs, y)
    print("Melhores resultados: Weight: uniform, k = 15, Score: %f" % (maiorScore))
    return



if __name__ == '__main__':
    main()
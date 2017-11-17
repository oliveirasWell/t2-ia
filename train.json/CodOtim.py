import json
import scipy as scipy
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
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
    ingredientesTreino = [item['ingredients'] for item in dataTreino]
    ingredientesUnicosTreino = set(item for sublist in ingredientesTreino for item in sublist)

    # Acrescenta os ingredientes do conjunto de teste em ingredientes
    ingredientesTeste = [item['ingredients'] for item in dataTeste]
#    ingredientesUnicosTeste = set(item for sublist in ingredientesTeste for item in sublist)

    return ingredientesTreino, ingredientesUnicosTreino, ingredientesTeste

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
    #print(quant)
    # print(todosOsIngredientes)
    ingredientesMaioresQue100 = []
    quantIngredientesMaioresQue100 = []

    for i in range(0, len(todosOsIngredientes)):
        if quant[i] >= 100:
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
    return xs, y, id, ingredientesMaioresQue100

def retornaTeste(todosOsIngredientesTreino, dicionarioDeJsonTEste, todosOsIngredientesTeste):
    xsTeste = []
    for i in (dicionarioDeJsonTEste):
        xTeste = []
        ids = []
        for j in range(0, len(todosOsIngredientesTreino)):
            xTeste.append(0)
        for ingrediente in (i['ingredients']):
            for j in range(0, len(todosOsIngredientesTreino)):
                if ingrediente == todosOsIngredientesTreino[j] and ingrediente in todosOsIngredientesTeste:
                    xTeste[j] = 1
                    todosOsIngredientesTeste.remove(ingrediente)
        xsTeste.append(xTeste)
        ids.append(str(i['id']))
    return xsTeste, ids

def criarMatrizesEsparsas(ingredientesTreino, ingredientesUnicosTreino, ingredientesTeste):

    big_data_matrix = scipy.sparse.dok_matrix((len(ingredientesTreino), len(ingredientesUnicosTreino)), dtype=np.dtype(bool))
    big_test_matrix = scipy.sparse.dok_matrix((len(ingredientesTeste), len(ingredientesUnicosTreino)), dtype=np.dtype(bool))

    for d, prato in enumerate(ingredientesTreino):
        for i, ingredient in enumerate(ingredientesUnicosTreino):
            if ingredient in prato:
                big_data_matrix[d, i] = True

    for d, dish in enumerate(ingredientesTeste):
        for i, ingredient in enumerate(ingredientesUnicosTreino):
            if ingredient in dish:
                big_test_matrix[d, i] = True

    return big_data_matrix, big_test_matrix

def main():
    dicionarioDeJsonTreino, dicionarioDeJsonTEste = leArquivoJson()

    todosOsIngredientesTreino, ingredientesUnicosTreino, todosOsIngredientesTeste = criarTodosOsIngrediente(dicionarioDeJsonTreino, dicionarioDeJsonTEste)
    #print(todosOsIngredientesTeste)

    big_data_matrix, big_test_matrix = criarMatrizesEsparsas(todosOsIngredientesTreino, ingredientesUnicosTreino, todosOsIngredientesTeste)

    print(big_data_matrix, big_test_matrix)

 #   xsTreino, yTreino, idTreino, ingredientesMaioresQue100 = criarXSYIDS(dicionarioDeJsonTreino, todosOsIngredientesTreino)
 #   xsTeste, idsTeste = retornaTeste(ingredientesMaioresQue100, dicionarioDeJsonTEste, todosOsIngredientesTeste)
    # xsTeste, yTeste, idTeste = criarXSYIDS(dicionarioDeJsonTEste, todosOsIngredientesTeste)
 #   print(len(xsTreino[0]))
 #   print(len(xsTeste[0]))
    # print(id[0])
    # print(xs[0])
    # print(y[0])
    # X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.3, random_state=0)
 #  clf = neighbors.KNeighborsClassifier(15, weights='uniform')
 #   clf.fit(xsTreino, yTreino)
 #   maiorScore = clf.score(xsTeste, yTreino)
    # result_dict = dict(zip(id, maiorScore))
 #   print("Melhores resultados: Weight: uniform, k = 15, Score: %f" % (maiorScore))
    return


if __name__ == '__main__':
    main()
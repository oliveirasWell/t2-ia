import csv
import json
import scipy as scipy
import numpy as np

from sklearn.naive_bayes import BernoulliNB
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
### --------------------------------------------------------------------------------------

def criarTodosOsIngrediente(dataTreino, dataTeste):
    ingredientesTreino = [item['ingredients'] for item in dataTreino]
    ingredientesUnicosTreino = set(item for sublist in ingredientesTreino for item in sublist)

    ingredientesTeste = [item['ingredients'] for item in dataTeste]
#    ingredientesUnicosTeste = set(item for sublist in ingredientesTeste for item in sublist)

    return ingredientesTreino, ingredientesUnicosTreino, ingredientesTeste
### --------------------------------------------------------------------------------------

def verificaCulinaria(dataTreino, dataTeste):
    culinaria = [item['cuisine'] for item in dataTreino]
    culinariaUnica = set(culinaria)
    return culinaria, culinariaUnica
### --------------------------------------------------------------------------------------


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
### --------------------------------------------------------------------------------------

def calculaBernoulliNB(culinaria, big_data_matrix, big_test_matrix, dicionarioDeJsonTEste):
    clf2 = BernoulliNB(alpha=0, fit_prior=False)
    f = clf2.fit(big_data_matrix, culinaria)
    result = [(ref == res, ref, res) for (ref, res) in zip(culinaria, clf2.predict(big_data_matrix))]
    accuracy_learn = sum(r[0] for r in result) / len(result)

    print('Accuracy on the learning set: ', accuracy_learn)

    result_test = clf2.predict(big_test_matrix)
    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, result_test))

    writer = csv.writer(open('SubmissionBernoulli.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    for key, value in result_dict.items():
        writer.writerow([key, value])

    print('Result saved in file: SubmissionBernoulli.csv')

    return
### --------------------------------------------------------------------------------------

def main():
    dicionarioDeJsonTreino, dicionarioDeJsonTEste = leArquivoJson()

    todosOsIngredientesTreino, ingredientesUnicosTreino, todosOsIngredientesTeste = criarTodosOsIngrediente(dicionarioDeJsonTreino, dicionarioDeJsonTEste)
    culinaria, culinariaUnica = verificaCulinaria(dicionarioDeJsonTreino, dicionarioDeJsonTEste)

    big_data_matrix, big_test_matrix = criarMatrizesEsparsas(todosOsIngredientesTreino, ingredientesUnicosTreino, todosOsIngredientesTeste)

    calculaBernoulliNB(culinaria, big_data_matrix, big_test_matrix, dicionarioDeJsonTEste)

    clf = neighbors.KNeighborsClassifier(10, weights='uniform')
    clf.fit(big_data_matrix, culinaria)
    resultado = clf.predict(big_test_matrix)

    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, resultado))

    writer = csv.writer(open('submissionKNN.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    for key, value in result_dict.items():
        writer.writerow([key, value])

    print('Result saved in file: submissionKNN.csv')
    return


if __name__ == '__main__':
    main()
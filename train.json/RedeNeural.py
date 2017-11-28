#! /usr/bin/python3

import scipy as scipy
import csv
import json
import numpy as np
from sklearn.neural_network import MLPClassifier
import time
import timeit
from sklearn.model_selection import GridSearchCV


def leArquivoJson():
    with open('train.json') as data_file1:
        dataTreino = json.load(data_file1)
    data_file1.close()
    with open('test.json') as data_file2:
        dataTeste = json.load(data_file2)
    data_file2.close()
    return dataTreino, dataTeste


def main():
    dicionarioDeJsonTrieno, dicionarioDeJsonTEste = leArquivoJson()

    ingredientesTreino = [item['ingredients'] for item in dicionarioDeJsonTrieno]
    ingredientesSemRepeticaoTreino = set(item for sublist in ingredientesTreino for item in sublist)

    yTreino = [item['cuisine'] for item in dicionarioDeJsonTrieno]
    # unique_cuisines = set(yTreino)

    xTreino = scipy.sparse.dok_matrix((len(ingredientesTreino), len(ingredientesSemRepeticaoTreino)),
                                      dtype=np.dtype(bool))

    for numeroPrato, exemplo in enumerate(ingredientesTreino):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in exemplo:
                xTreino[numeroPrato, numeroIngrediente] = True

    parameters = {
        'activation': ['logistic', 'relu'],
        'hidden_layer_sizes': [35, 37, 40],
        'alpha': [0.01, 0.05],
        'learning_rate': ['adaptive'],
        'solver': ['adam'],
        'shuffle': [True, False],
        'beta_1': [0.999, 0.99, 0.9, 0.8],
        'beta_2': [0.999, 0.99, 0.9, 0.8],
        'epsilon': [1e-9, 1e-8, 1e-7]
    }

    inicio = timeit.default_timer()
    clf = MLPClassifier()
    gs = GridSearchCV(clf, param_grid=parameters, cv=5)

    gs.fit(xTreino, yTreino)

    ingredientesTeste = [item['ingredients'] for item in dicionarioDeJsonTEste]
    xTeste = scipy.sparse.dok_matrix((len(ingredientesTeste), len(ingredientesSemRepeticaoTreino)),
                                     dtype=np.dtype(bool))
    for numeroExemplo, dish in enumerate(ingredientesTeste):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in dish:
                xTeste[numeroExemplo, numeroIngrediente] = True

    result_test = gs.predict(xTeste)
    fim = (timeit.default_timer())
    print('duracao: %f' % (fim - inicio))
    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, result_test))

    print(gs.best_params_)

    writer = csv.writer(open('redeNeural.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    for key, value in result_dict.items():
        writer.writerow([key, value])

    print('Result saved in file: redeNeural.csv')


if __name__ == '__main__':
    main()

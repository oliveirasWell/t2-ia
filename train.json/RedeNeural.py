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
        'hidden_layer_sizes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 35, 40],
        'learning_rate': ["constant", "invscaling", "adaptive"],
        'alpha': [1, 0.01, 0.001, 0.0001],
        'activation': ["logistic", "identity", "tanh"],
        'solver': ['adam', 'lbfgs', 'sgd'],
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

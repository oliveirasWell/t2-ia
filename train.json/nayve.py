#! /usr/bin/python3

import scipy as scipy
import csv
import json
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import GridSearchCV
import time
import timeit

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

    xTreino = scipy.sparse.dok_matrix((len(ingredientesTreino), len(ingredientesSemRepeticaoTreino)), dtype=np.dtype(bool))

    for numeroPrato, exemplo in enumerate(ingredientesTreino):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in exemplo:
                xTreino[numeroPrato, numeroIngrediente] = True

    parameters = {'binarize': [0.0],
                  'fit_prior': [False, True],
                  'alpha': [0.0001, 1e-3, 1e-2, 0.1, 1]}

    inicio = timeit.default_timer()
    clf = GridSearchCV(BernoulliNB(), parameters, n_jobs=-1, refit=True, cv=5)
    clf.fit(xTreino, yTreino)

    ingredientesTeste = [item['ingredients'] for item in dicionarioDeJsonTEste]
    xTeste = scipy.sparse.dok_matrix((len(ingredientesTeste), len(ingredientesSemRepeticaoTreino)), dtype=np.dtype(bool))
    for numeroExemplo, dish in enumerate(ingredientesTeste):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in dish:
                xTeste[numeroExemplo, numeroIngrediente] = True

    result_test = clf.predict(xTeste)
    fim = (timeit.default_timer())
    print('duracao: %f' % (fim - inicio))
    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, result_test))

    writer = csv.writer(open('nayve.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    for key, value in result_dict.items():
        writer.writerow([key, value])

    print('Result saved in file: nayve.csv')
    print(clf.best_params_)


if __name__ == '__main__':
    main()

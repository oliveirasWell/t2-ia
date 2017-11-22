#! /usr/bin/python3

import scipy as scipy
import csv
import json
import numpy as np
from sklearn import linear_model
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

    xTreino = scipy.sparse.dok_matrix((len(ingredientesTreino), len(ingredientesSemRepeticaoTreino)), dtype=np.dtype(bool))

    for numeroPrato, exemplo in enumerate(ingredientesTreino):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in exemplo:
                xTreino[numeroPrato, numeroIngrediente] = True

    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        'solver': ['newton-cg', 'sag', 'saga', 'lbfgs']
    }

    clf = GridSearchCV(linear_model.LogisticRegression(penalty='l2'), param_grid, cv=5)

    clf.fit(xTreino, yTreino)

    ingredientesTeste = [item['ingredients'] for item in dicionarioDeJsonTEste]
    xTeste = scipy.sparse.dok_matrix((len(ingredientesTeste), len(ingredientesSemRepeticaoTreino)), dtype=np.dtype(bool))
    for numeroExemplo, dish in enumerate(ingredientesTeste):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in dish:
                xTeste[numeroExemplo, numeroIngrediente] = True

    result_test = clf.predict(xTeste)
    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, result_test))

    writer = csv.writer(open('regressaumlogistica.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    for key, value in result_dict.items():
        writer.writerow([key, value])
    print(clf.best_params_)
    print('Result saved in file: regressaumlogistica.csv')


if __name__ == '__main__':
    main()

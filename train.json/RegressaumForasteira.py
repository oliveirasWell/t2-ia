#! /usr/bin/python3

import scipy as scipy
import csv
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
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


    xTreino = scipy.sparse.dok_matrix((len(ingredientesTreino), len(ingredientesSemRepeticaoTreino)), dtype=np.dtype(bool))

    param_grid = {"max_depth": [3, None],
                  "max_features": [1, 3, 10],
                  "min_samples_split": [2, 3, 10],
                  "min_samples_leaf": [1, 3, 10],
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}

    for numeroPrato,exemplo in enumerate(ingredientesTreino):
        for numeroIngrediente,ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in exemplo:
                xTreino[numeroPrato,numeroIngrediente] = True

    clf = RandomForestClassifier(n_estimators=20)
    grid_search = GridSearchCV(clf, param_grid=param_grid)

    # specify parameters and distributions to sample from
    #param_dist = {"max_depth": [3, None], "max_features": sp_randint(1, 11),
              #"min_samples_split": sp_randint(1, 11),
              #"min_samples_leaf": sp_randint(1, 11),
              #"bootstrap": [True, False],
              #"criterion": ["gini", "entropy"]}

    # run randomized search
    #n_iter_search = 20
    #random_search = RandomizedSearchCV(clf, param_distributions=param_dist, n_iter=n_iter_search)

    grid_search.fit(xTreino, yTreino)

    ingredientesTeste = [item['ingredients'] for item in dicionarioDeJsonTEste]
    xTeste = scipy.sparse.dok_matrix((len(ingredientesTeste), len(ingredientesSemRepeticaoTreino)), dtype=np.dtype(bool))
    for numeroExemplo,dish in enumerate(ingredientesTeste):
        for numeroIngrediente,ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in dish:
                xTeste[numeroExemplo,numeroIngrediente] = True


    result_test = grid_search.predict(xTeste)
    print(clf.best_params_)

    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, result_test))

    writer = csv.writer(open('RegressaoForasteira.csv', 'wt'))
    writer.writerow(['id','cuisine'])
    for key, value in result_dict.items():
       writer.writerow([key, value])

    print('Result saved in file: RegressaoForasteira.csv')

if __name__ == '__main__':
    main()
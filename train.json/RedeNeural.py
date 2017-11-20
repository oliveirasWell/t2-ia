#! /usr/bin/python3

import json as js
import csv as csv
import scipy as scipy
import numpy as np
import pdb
import csv
import json
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import linear_model, datasets
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import itertools

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
        'learning_rate': ['constant', 'invscaling', 'adaptive'],
        'hidden_layer_sizes': [x for x in itertools.product((10,20,30,40,50,100),repeat=3)],
        'alpha': [10.0 ** -np.arange(1, 7)],
        'activation': ['logistic', 'relu', 'Tanh']
    }

    clf = GridSearchCV(estimator=MLPClassifier(), param_grid=parameters, n_jobs=-1, verbose=2, cv=10)
    #clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)


    clf.fit(xTreino, yTreino)

    ingredientesTeste = [item['ingredients'] for item in dicionarioDeJsonTEste]
    xTeste = scipy.sparse.dok_matrix((len(ingredientesTeste), len(ingredientesSemRepeticaoTreino)),
                                     dtype=np.dtype(bool))
    for numeroExemplo, dish in enumerate(ingredientesTeste):
        for numeroIngrediente, ingredient in enumerate(ingredientesSemRepeticaoTreino):
            if ingredient in dish:
                xTeste[numeroExemplo, numeroIngrediente] = True

    result_test = clf.predict(xTeste)
    ids = [item['id'] for item in dicionarioDeJsonTEste]
    result_dict = dict(zip(ids, result_test))

    writer = csv.writer(open('redeNeural.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    for key, value in result_dict.items():
        writer.writerow([key, value])

    print('Result saved in file: redeNeural.csv')


if __name__ == '__main__':
    main()
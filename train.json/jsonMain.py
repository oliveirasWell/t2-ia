import csv
import json
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV


def leArquivoJson():
    with open('train.json') as data_file1:
        dataTreino = json.load(data_file1)
    data_file1.close()
    with open('test.json') as data_file2:
        dataTeste = json.load(data_file2)
    data_file2.close()
    return dataTreino, dataTeste


def criarTodosOsIngrediente(dataTreino, dataTeste):

    # Acrescenta os ingredientes do conjunto de treino em ingredientes
    ingredientes = []
    for j in dataTreino:
        ingredientes.append(j['ingredients'])

    todosOsIngredientesTreino = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
            todosOsIngredientesTreino.append((ingredientes[i][j]))

    # Acrescenta os ingredientes do conjunto de teste em ingredientes
    ingredientes = []
    for j in dataTeste:
        ingredientes.append(j['ingredients'])

    todosOsIngredientesTeste = []
    for i in range(0, len(ingredientes)):
        for j in range(0, len(ingredientes[i])):
             todosOsIngredientesTeste.append((ingredientes[i][j]))

    todosOsIngredientesTreino =  [x for x in set(todosOsIngredientesTreino)]
    todosOsIngredientesTeste = [x for x in set(todosOsIngredientesTeste)]
   # print(todosOsIngredientesTeste)
    #print(todosOsIngredientesTreino)



    return todosOsIngredientesTreino, todosOsIngredientesTeste


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
    # print(todosOsIngredientes)
    ingredientesMaioresQue100 = []
    quantIngredientesMaioresQue100 = []

    for i in range(0, len(todosOsIngredientes)):
        if quant[i] >= 50:
            ingredientesMaioresQue100.append(todosOsIngredientes[i])
            quantIngredientesMaioresQue100.append(quant[i])

    for i in dicionarioDeJson:
        xIngredientes = []
        id.append(str(i['id']))
        for j in ingredientesMaioresQue100:
            if j in i['ingredients']:
                xIngredientes.append(True)
            else:
                xIngredientes.append(False)
        xs.append(xIngredientes)
        y.append(i['cuisine'])
    return xs, y, id, ingredientesMaioresQue100


def retornaTeste(todosOsIngredientesTreino, dicionarioDeJsonTEste, todosOsIngredientesTeste):
    xsTeste = []
    ids = []
    for i in (dicionarioDeJsonTEste):
        xTeste = []
        for j in range(0, len(todosOsIngredientesTreino)):
            xTeste.append(False)
        for ingrediente in (i['ingredients']):
            for j in range(0, len(todosOsIngredientesTreino)):
                if ingrediente == todosOsIngredientesTreino[j] and ingrediente in todosOsIngredientesTeste:
                    xTeste[j] = True
                    todosOsIngredientesTeste.remove(ingrediente)
        xsTeste.append(xTeste)
        ids.append(str(i['id']))
    return xsTeste, ids



def main():
    dicionarioDeJsonTrieno, dicionarioDeJsonTEste = leArquivoJson()

    todosOsIngredientesTreino, todosOsIngredientesTeste = criarTodosOsIngrediente(dicionarioDeJsonTrieno, dicionarioDeJsonTEste)
    #print(todosOsIngredientesTeste)

    xsTreino, yTreino, idTreino, ingredientesMaioresQue100 = criarXSYIDS(dicionarioDeJsonTrieno, todosOsIngredientesTreino)
    xsTeste, idsTeste = retornaTeste(ingredientesMaioresQue100, dicionarioDeJsonTEste, todosOsIngredientesTeste)
    # xsTeste, yTeste, idTeste = criarXSYIDS(dicionarioDeJsonTEste, todosOsIngredientesTeste)



    print(len(xsTreino[0]))
    print(len(xsTeste[0]))
    # print(id[0])
    # print(xs[0])
    # print(y[0])
    # X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.3, random_state=0)
    k_range = list(range(1, 31))
    knn = neighbors.KNeighborsClassifier(15, weights='distance')
    weight_options = ['uniform', 'distance']
    param_grid = dict(n_neighbors=k_range, weights=weight_options)
    #print(param_grid)
    clf = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')

    clf.fit(xsTreino, yTreino)



    yTeste = clf.predict(xsTeste)
    print(clf.best_params_)
    #print (len(yTeste))
 #   yTeste = clf.inverse_transform(yTeste)

    writer = csv.writer(open('submission.csv', 'wt'))
    writer.writerow(['id', 'cuisine'])
    print(len(idsTeste))
    for i in range (0, len(idsTeste)):
        writer.writerow([idsTeste[i], yTeste[i]])

    print('Result saved in file: submission.csv')
    print(clf.best_params_)
    # result_dict = dict(zip(id, maiorScore))
    #print("Melhores resultados: Weight: uniform, k = 15, Score: %f" % (clf.score(xsTeste, yTeste)))
 #   return


if __name__ == '__main__':
    main()
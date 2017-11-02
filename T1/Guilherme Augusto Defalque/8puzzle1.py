import sys
import copy
import math
#!/usr/bin/python

#Retorna os pais dos nos

def son2str(s):
    s1 = s[0] + s[1] + s[2]
    return ''.join([str(v) for v in s1])


#Verifica se as coordenadas de um movimento realizado saum validas
def valid(x, y):
    r = True
    if x < 0 : r = False
    if x > 2 : r = False
    if y < 0 : r = False
    if y > 2 : r = False
    return r


#Variaveis globais que armazenam os nos que ja foram visitados e os que naum foram
visited = None
Node_No_visited = []

#Retorna a distancia otima da heurista h(n) que faz a soma da quantidade de movimentos que cada numero necessita receber para estar em sua posicaum correta.

def distance(ts):
    d = 0
    for i in range(len(ts)):
        for j in range(len(ts[i])):
            if ts[i][j] == 0:
                coord_i = i - 2
                coord_j = j - 2
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j   
            if ts[i][j] == 1:
                coord_i = i - 0
                coord_j = j - 0
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j  
            if ts[i][j] == 2:
                coord_i = i - 0
                coord_j = j - 1
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j  
            if ts[i][j] == 3:
                coord_i = i - 0
                coord_j = j - 2
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j  
            if ts[i][j] == 4:
                coord_i = i - 1
                coord_j = j - 0
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j  
            if ts[i][j] == 5:
                coord_i = i - 1
                coord_j = j - 1
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j 
            if ts[i][j] == 6:
                coord_i = i - 1
                coord_j = j - 2
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j 
            if ts[i][j] == 7:
                coord_i = i - 2
                coord_j = j - 0
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j 
            if ts[i][j] == 8:
                coord_i = i - 2
                coord_j = j - 1
                if coord_i<0:
                    coord_i = coord_i*(-1)
                if coord_j<0:
                    coord_j = coord_j*(-1)
                d = d + coord_i + coord_j  
    return d


#Responsavel por verificar os filhos de um determinado no e escolher, segundo a heuristica, qual de ve ser o no que leva ao caminho otimo
#buscado. Encontrando-o, Verifica se sua distancia e a melhor comparando-a com os elementos ainda naum verificaos. Caso seja, retorna o no
#Caso naum, retorna o no naum visitado com menor distancia
def sons(s):

    #r
    r = []
    x = None
    y = None
    d = 10000
    ajuda = []
    global visited
    global Node_No_visited
    filhos = []
    Elementos = []
    
    inicial_element = s[1]
    #localiza zero
    for i in range(len(inicial_element)):
        for j in range(len(inicial_element[i])):
            if inicial_element[i][j] == 0:
                x = i
                y = j

    #cima
    vx = x - 1
    vy = y
    if(valid(vx,vy)):
        ts = copy.deepcopy(inicial_element)
        t = ts[vx][vy]
        ts[vx][vy] = ts[x][y]
        ts[x][y] = t

        if ts not in visited:
            Elementos.append(distance(ts))
            Elementos.append(copy.deepcopy(ts))
            filhos.append(Elementos)
            Elementos = []
        if d > distance(ts):
            if ts not in visited:
                d = distance(ts)
                ajuda.append(d)
                ajuda.append(copy.deepcopy(ts))
                r = copy.deepcopy(ajuda)
                ajuda = []
    #baixo
    vx = x+1
    vy = y
    if(valid(vx,vy)):
        ts = copy.deepcopy(inicial_element)
        t = ts[vx][vy]
        ts[vx][vy] = ts[x][y]
        ts[x][y] = t

        if ts not in visited:
            Elementos.append(distance(ts))
            Elementos.append(copy.deepcopy(ts))
            filhos.append(Elementos)
            Elementos = []
        if d > distance(ts):
            if ts not in visited:
                d = distance(ts)
                ajuda.append(d)
                ajuda.append(copy.deepcopy(ts))
                r = copy.deepcopy(ajuda)
                ajuda = []

    #esquerda

    vx = x
    vy = y - 1
    if(valid(vx,vy)):
        ts = copy.deepcopy(inicial_element)
        t = ts[vx][vy]
        ts[vx][vy] = ts[x][y]
        ts[x][y] = t

        if ts not in visited:
            Elementos.append(distance(ts))
            Elementos.append(copy.deepcopy(ts))
            filhos.append(Elementos)
            Elementos = []
        if d > distance(ts):
            if ts not in visited:
                d = distance(ts)
                ajuda.append(d)
                ajuda.append(copy.deepcopy(ts))
                r = copy.deepcopy(ajuda)
                ajuda = []
    #direita
    vx = x
    vy = y + 1
    if(valid(vx,vy)):
        ts = copy.deepcopy(inicial_element)
        t = ts[vx][vy]
        ts[vx][vy] = ts[x][y]
        ts[x][y] = t

        if ts not in visited:
            Elementos.append(distance(ts))
            Elementos.append(copy.deepcopy(ts))
            filhos.append(Elementos)
            Elementos = []
        if d > distance(ts):
            if ts not in visited:
                d = distance(ts)
                ajuda.append(d)
                ajuda.append(copy.deepcopy(ts))
                r = copy.deepcopy(ajuda)
                ajuda = []
     

    for element in filhos:
        if element[1] != r[1]:
            Node_No_visited.append(element) 
    sorted(Node_No_visited, key = ordena);
    if Node_No_visited[0][0] < d:
        Node_No_visited.append(r)
        r = Node_No_visited.pop(0)       

    return r

def ordena(t):
    return (t[0])

#Funcaum que verifia se o no retornado pela funcaum sons e o procurado. Caso naum, marca-o como visitado e o retorna para sons.
def bfs(start,goal):
    inicio = []
    inicio.append(1000)
    inicio.append(start)
    l = [inicio]
    global visited
    global Node_No_visited
    fathers = dict()
    visited = [start]
    j = 1
    while (len(l) > 0):
        father = l[0]
        print "estado", j
        print father
        j = j + 1
        del l[0]
        son = sons(father)
        if son[1] not in visited:
            visited.append(son[1])
            i = 0
            while i < len(Node_No_visited):
                if Node_No_visited[i] == son:
                    Node_No_visited.pop(i)
                else:
                    i = i + 1
            fathers[son2str(son[1])] =  father
            if son[1] == goal:
                return son
            else:
                l.append(son)

#funcao inicial mais responsavel por ler a variavel de entrada e imprimir o no buscado
if __name__ == '__main__':
    f = open(sys.argv[1])
    entrada = []
    for line in f:
        tv = [int(v) for v in line.rstrip('\n').split(' ')]
        entrada.append(tv)
    final = [[1,2,3],[4,5,6],[7,8,0]]
    if entrada != final:
       resp = bfs(entrada, final)
       print "estado final"
       print resp
       
    else:
        print entrada
    







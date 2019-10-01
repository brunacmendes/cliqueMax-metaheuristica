#!/usr/bin/env python3

import sys
import random
import time
import os
import item as items

QTD_ITENS = 0
TAM_MAX_PACOTE = 0
ITENS = []
NUM_REST = 0

list1 = list()
list2 = list()
list3 = list()
list4 = list()

def lerArquivo():

    global QTD_ITENS
    global TAM_MAX_PACOTE
    global ITENS

    #leitura do arquivo passado como primeiro parametro
    arquivo = open('instancias/'+sys.argv[1], 'r')
    info = arquivo.readline()
    graph = arquivo.readlines()
    arquivo.close()
    
    #armazenamento das informacoes
    info = info.split( )

    QTD_ITENS = info[0]
    TAM_MAX_PACOTE = info[1]
    
    #preenchimento dos dados dos itens
    for i in graph :
        token = i.split()
        if token :
            aux = items.Item( token[0], token[1], token[2:])
            ITENS.append(aux)

def ordenaItens():
    global ITENS

    aux = sorted(ITENS, key = items.Item.get_peso)
    return aux

def geraConjuntos(itens):

    global list1
    global list2
    global list3
    global list4

    tam = int(TAM_MAX_PACOTE)

    for i in itens:
        if i.get_peso() <= ( tam * 0.25 ) :
            list1.append(i)
        elif i.get_peso() <= ( tam * 0.50 ) :
            list2.append(i)
        elif i.get_peso() <= ( tam * 0.75 ) :
            list3.append(i)
        else:
            list2.append(i)

def geraRCL(lista, capacidade, conflitos, itensAtuais):

    itat = set(itensAtuais)

    rcl = []
   
    for i in lista:
        
        if i.get_peso() < capacidade:
            
            confItem = set(i.conflitos)
            
            if not(i in conflitos) and  ( confItem & itat != {} ) :
                rcl.append(i)

    return rcl

def solver(itens):

    #enquanto nao acabar os itens do vetor 3
        #pega um item aleatorio dele e adiciona no pacote
        #gera a rcl do vetor 2
        #se a rcl nao for vazia
            #escolhe um aleatorio e adiciona no pacote
        #gera a rcl do vetor 1
        #enquanto a rcl n for vazia
            #escolhe um aleatorio e adiciona no pacote
            #gera a rcl do vetor 1
            #se a rcl for vazia
                #termina esse pacote e abre um novo
                #break

    #enquanto nao acabar os itens do vetor 2
        #pega um item aleatorio dele e adiciona no pacote
        #gera a rcl do vetor 2
        #enquanto a rcl n for vazia
                #escolhe um aleatorio e adiciona no pacote
                #gera a rcl do vetor 2
                #se a rcl for vazia
                    #gera a rcl do vetor 1
                    #enquanto a rcl n for vazia
                        #escolhe um aleatorio e adiciona no pacote
                        #gera a rcl do vetor 1
                        #se a rcl for vazia
                            #termina esse pacote e abre um novo
                            #break
    
    #enquanto nao acabar os itens do vetor 4
        #pega um item aleatorio dele e adiciona no pacote
        #gera a rcl do vetor 1
        #enquanto a rcl n for vazia
            #escolhe um aleatorio e adiciona no pacote
            #gera a rcl do vetor 1
            #se a rcl for vazia
                #termina esse pacote e abre um 
                #break

     #enquanto nao acabar os itens do vetor 1
        #pega um item aleatorio dele e adiciona no pacote
        #gera a rcl do vetor 1
        #enquanto a rcl n for vazia
            #escolhe um aleatorio e adiciona no pacote
            #gera a rcl do vetor 1
            #se a rcl for vazia
                #termina esse pacote e abre um novo
                #break



    global TAM_MAX_PACOTE
    
    pacotes = 0
    conf = []
    itensAtuais = []
    peso_pacote = int(TAM_MAX_PACOTE)
    capAtual = peso_pacote

    #esvazia a lista 3

    while list3 :
        pacotes += 1
        conf = []
        itensAtuais = []
        capAtual = peso_pacote

        item = random.choice(list3)
        
        capAtual -= item.get_peso()
        conf += item.conflitos
        itensAtuais.append(item)
        list3.remove(item)

        rcl = geraRCL(list2, capAtual, conf, itensAtuais)

        while rcl :

            item = random.choice(rcl)

            capAtual -= item.get_peso()
            conf += item.conflitos
            itensAtuais.append(item)
            list2.remove(item)

            rcl = geraRCL(list1, capAtual, conf, itensAtuais)

            while rcl :
                
                item = random.choice(rcl)

                capAtual -= item.get_peso()
                conf += item.conflitos
                itensAtuais.append(item)
                list1.remove(item)

                rcl = geraRCL(list1, capAtual, conf, itensAtuais)

                if rcl == [] :
                    break

    #esvazia a lista 2

    while list2 :
        
        pacotes += 1
        conf = []
        itensAtuais = []
        capAtual = peso_pacote

        item = random.choice(list2)
        
        capAtual -= item.get_peso()
        conf += item.conflitos
        itensAtuais.append(item)
        list2.remove(item)

        rcl = geraRCL(list2, capAtual, conf, itensAtuais)
        while rcl :

            item = random.choice(rcl)

            capAtual -= item.get_peso()
            conf += item.conflitos
            itensAtuais.append(item)
            list2.remove(item)

            rcl = geraRCL(list2, capAtual, conf, itensAtuais)

            if rcl == [] :
                
                rcl = geraRCL(list1, capAtual, conf, itensAtuais)

                while rcl :
                    
                    item = random.choice(rcl)

                    capAtual -= item.get_peso()
                    conf += item.conflitos
                    itensAtuais.append(item)
                    list1.remove(item)

                    rcl = geraRCL(list1, capAtual, conf, itensAtuais)

                    if rcl == [] :
                        break
    
    #esvazia a lista 4

    while list4 :
        
        pacotes += 1
        conf = []
        itensAtuais = []
        capAtual = peso_pacote

        item = random.choice(list4)
        
        capAtual -= item.get_peso()
        conf += item.conflitos
        itensAtuais.append(item)
        list4.remove(item)

        rcl = geraRCL(list1, capAtual, conf, itensAtuais)
        while rcl :

            item = random.choice(rcl)

            capAtual -= item.get_peso()
            conf += item.conflitos
            itensAtuais.append(item)
            list1.remove(item)

            rcl = geraRCL(list1, capAtual, conf, itensAtuais)

            if rcl == [] :
                break

    #esvazia a lista 1

    while list1 :
        
        pacotes += 1
        conf = []
        itensAtuais = []
        capAtual = peso_pacote

        item = random.choice(list1)
        
        capAtual -= item.get_peso()
        conf += item.conflitos
        itensAtuais.append(item)
        list1.remove(item)

        rcl = geraRCL(list1, capAtual, conf, itensAtuais)
        while rcl :

            item = random.choice(rcl)

            capAtual -= item.get_peso()
            conf += item.conflitos
            itensAtuais.append(item)
            list1.remove(item)

            rcl = geraRCL(list1, capAtual, conf, itensAtuais)

            if rcl == [] :
                break

    return pacotes

        
def saida(nomeArq, instancia, parametro, runtime, objetivo) :

    dir =  f'{nomeArq}.out'

    if os.path.isfile(f'{dir}') :
        opcao = 'a' 
    else :
        opcao = 'w'
        with open(dir,opcao) as arq :
            arq.writelines(f'Instancia\t\tParametro\tRuntime\t\tObjetivo\n')
        opcao = 'a'

    with open(dir,opcao) as arq :
        arq.write(f'{instancia}\t\t{parametro}\t\t{runtime:.2}s\t\t{objetivo}\n')
    
    
def main():

    lerArquivo()


    #coloca essa linha antes da funcao que calcula o resultado
    inicio = time.time()


    itens = ordenaItens() 

    geraConjuntos(itens)

    resultado = solver(itens)
    
    #aqui capta o tempo final e faz a diferença
    fim = time.time()

    tempo = fim - inicio
    
    #passa como 1 parametro o nome do arquivo de saida, depois nome da instancia, os parametros
    # o tempo e o resultado
    saida('solverGR', sys.argv[1], '-', tempo, resultado)

    print(f'Devem ser utilizados *{resultado}* pacotes para essa instancia!')
    


main()


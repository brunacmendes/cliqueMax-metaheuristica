from heuristica import Heuristica

ITER = 100

#file_name = 'C125.9.clq' #optimal
#file_name = 'C250.9.clq' #optimal
#file_name = 'C500.9.clq' 
#file_name = 'C1000.9.clq'
#file_name = 'C2000.5.clq' #optimal
#file_name = 'p_hat700-3.clq' #optimal
#file_name = 'p_hat700-2.clq'
#file_name = 'p_hat300-3.clq'
#file_name = 'p_hat300-2.clq'
#file_name = 'p_hat1500-2.clq' #optimal

files = []
files.append('benchmarks/C125.9.clq')
files.append('benchmarks/C250.9.clq')
files.append('benchmarks/C500.9.clq')
files.append('benchmarks/C1000.9.clq')
files.append('benchmarks/C2000.5.clq')
files.append('benchmarks/p_hat700-3.clq')
files.append('benchmarks/p_hat700-2.clq')
files.append('benchmarks/p_hat300-3.clq')
files.append('benchmarks/p_hat300-2.clq')
files.append('benchmarks/p_hat1500-2.clq')


result = []
size = len(files)
heuristica = Heuristica()
# roda heurística ITER vezes e salva resultados
for x in range(0,size):
    path = files[x]
    
    result = heuristica.executa(path,ITER)

    content = 'Heuristica para Clique Maxima\n\n'

    #cria conteúdo 
    content += 'INSTANCE\tITERATION\tMAXIMUM CLIQUE\tRUNTIME\n\n'    # MIN\tMAX\tMÉDIA\tMEDIANA\tVARIÂNCIA\tDESVIO\tQ1\tQ3\n\n

    for i in range(0,ITER):
        content += '{}\t{}\t{}\t{}\n'.format(files[x], i+1, result[i][0], result[i][1])
        
    print(content)

    with open(files[x]+"_results.txt", "w") as file:
        file.write(content)
from main import Main

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


files.append('C250.9.clq')
files.append('C500.9.clq')
files.append('C1000.9.clq')
files.append('C2000.5.clq')
files.append('p_hat700-1.clq')
files.append('p_hat700-3.clq')
files.append('p_hat700-2.clq')
files.append('p_hat300-3.clq')
files.append('p_hat300-2.clq')
files.append('p_hat300-1.clq')
files.append('p_hat1500-2.clq')
files.append('p_hat1500-1.clq')



size = len(files)
vns = Main()

for x in range(0,size):
    path = files[x]
    result = []
    for _ in range(ITER):
        result.append(vns.run(path))




    content = 'INSTANCE\tITERATION\tMAXIMUM CLIQUE\tRUNTIME\n\n'    # MIN\tMAX\tMÉDIA\tMEDIANA\tVARIÂNCIA\tDESVIO\tQ1\tQ3\n\n

    for i in range(0,ITER):
        content += '{}\t{}\t{}\t{}\n'.format(files[x], i+1, result[i][0], result[i][1])
        print(content)

    with open(files[x]+"_results.txt", "w") as file:
        file.write(content)
        
        
    

    

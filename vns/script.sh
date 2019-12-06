
diretorio_benchmark=$(cat Benchmark/arquivos2.txt);
diretorio_resultados="resultados.r";
for line in $diretorio_benchmark; 
do 
	for cont in {1..5};
	do
		execucao=$(python3 main.py Benchmark/$line);
		echo -e "$line\t$cont\t$execucao" >> $diretorio_resultados;
		echo "$line: $cont";
	done
done

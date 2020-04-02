# Projeto Máquina de busca

Neste projeto estamos desenvolvendo uma máquina de busca com as seguintes
características:

- queries booleanas;
- entendimento de query e auto-correção
- ranqueamento de resultados;

Fase 1: Construção do repositório e do índice.

Fase 2: Construção de uma ferramenta para busca com queries booleanas (AND, OR)

Fase 3: Ranking

Fase 4: Aperfeiçoamentos e melhoramento do ranking

## Como rodar

Primeiramente, rodar o ´setup_windows.bat´ ou ´setup_linux.sh´ estando no diretorio raiz do repositorio.

Para rodar o buscador, basta executar ´python buscador.py *corpus* *repo* *index* *num_docs* *query* *corretor*´, onde

- *corpus* é o arquivo do corpus
- *repo* é o arquido do repositorio (de palavras)
- *index* é o arquivo do indice (de palavras)
- *num_docs* é a quantidade de documentos que a busca deve retornar
- *query* é a pesquisa a ser feita (entre aspas)
- *corretor* é o numero do corretor a ser utilizado  : corretor por distancia; ou 2 : corretor norvig)


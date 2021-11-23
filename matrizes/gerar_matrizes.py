import line_profiler
import sys
from io import StringIO
from datetime import datetime

profile = line_profiler.LineProfiler()
stdout_trap = StringIO()

# funcao para criar arquivo de saida txt
def matrizes(nome = 'matrizes/arquivos_saida_matrizes/matrizes.txt'):
    with open(nome, 'w') as m:
        m.write('Data Hora: '+str(datetime.now()))
        m.write('\n\nMatrizes geradas\n\n')

# funcao que imprime em um arquivo txt o tempo total de execucao de cada funcao
# e o tempo de cada linha
def desempenho(stdout_trap = stdout_trap, arquivo = 'matrizes/arquivos_saida_matrizes/desempenho.txt'):
    profile.print_stats(stdout_trap)
    output = stdout_trap.getvalue()
    output = output.rstrip()

    with open(arquivo, 'w') as des:
        des.write('Data Hora: '+str(datetime.now())+'\n\n')
        des.write(output)

# funcao para transpor uma planilha
def transposta(lista):
    return list(map(list, zip(*lista))) 

# funcao para imprimir na tela uma matriz e gravar em um arquivo de saida txt
def imprime_matriz(nome_matriz, matriz, arq = 'matrizes/arquivos_saida_matrizes/matrizes.txt'):
    print(f'{nome_matriz} = ')
    with open(arq, 'a+') as m:
        m.write(f'{nome_matriz} = \n')
        for row in matriz:
            elems = ' '.join([str(e) for e in row])
            m.write(f'    | {elems} |\n')
            print(f'    | {elems} |')
        m.write('\n')
        print()

# funcao para gerar uma matrizes A e B aleatoria e fazer o produto delas
# sem usar bibliotecas intermediarias, alem da bibliotera random, para gerar numeros aleatorios
@profile
def gerar_matrizes_produto(m1, n1, m2, n2, n = 10):
    if n1 == m2:
        import random

        A = []

        for i in range(m1):
            A.append([random.randint(0, n) for j in range(n1)])

        B = []

        for i in range(m2):
            B.append([random.randint(0, n) for j in range(n2)])

        trans_B = transposta(B)
        prod = []
        for row in A:
<<<<<<< HEAD
            aux = []
            
            for rowt in trans_B:
                elem = sum([row[i]*rowt[i] for i in range(len(row))])
                aux.append(elem)
=======
            aux = [] 
            for i in range(m1):
                a = 0
                for j in range(m2):
                    a += row[j]*trans_B[i][j]
                aux.append(a)
>>>>>>> e6b299bcd95fbba21c58ea8977c5f1871eeb538c
            prod.append(aux)

        imprime_matriz('A',A)
        imprime_matriz('B',B)
        imprime_matriz('Produto', prod)
        return A, B, prod
    else:
        print('O numero de colunas (n1) da matriz A deve ser igual ao numero de linhas (n2) da matriz B')
        sys.exit()

# funcao para gerar matrizes A e B aleatorias e fazer o produto delas usando a 
# biblioteca Numpy
@profile
def gerar_matrizes_prod_np(m1, n1, m2, n2, n = 10):   
    if n1 == m2:
        import numpy as np

        A = np.random.randint(n, size=(m1,n1))
        B = np.random.randint(n, size=(m2,n2))

        prod = np.dot(A, B)

        imprime_matriz('A',A.tolist(), arq='matrizes/arquivos_saida_matrizes/matrizes_numpy.txt')
        imprime_matriz('B',B.tolist(), arq='matrizes/arquivos_saida_matrizes/matrizes_numpy.txt')
        imprime_matriz('Produto', prod.tolist(), arq='matrizes/arquivos_saida_matrizes/matrizes_numpy.txt')
        return A, B, prod
    else:
        print('O numero de colunas (n1) da matriz A deve ser igual ao numero de linhas (n2) da matriz B')
        sys.exit()

# funcao para validar opcoes, de acordo com o que foi exposto pro usuario
def valida_opcoes(opcao, min, max):
    return min <= opcao <= max


if __name__ == '__main__':
    import sys

    while 1:
        # menu de escolha
        print("""
    Por favor, escolha as opcoes abaixo:
            1 - gerar matriz aleatoria
            2 - gerar matriz aleatoria numpy

            0 - Sair

            ***Obs.: Numero de colunas (n1) da matriz A deve igual ao numero de linhas (m2) da matriz B 
        """)
        choice = input()
        # checando de se o valor digitado pelo usuario é digito
        if not choice.isdigit():
            print(f'Por favor, digite um valor dentro da faixa valida')
            continue
        # validando se as opcoes estao dentro da faixa indicada
        if not valida_opcoes(int(choice), 0, 2):
            print(f'Por favor, digite um valor dentro da faixa valida')
            continue
        
        elif int(choice) == 0:
            desempenho()
            sys.exit()

        # ==== Processo para definir tamanho da matriz
        print("Digite o numero de Linhas (m1) da matriz A: ")
        m1 = input()

        if not m1.isdigit():  
            print(f'Por favor, digite valor valido')
            continue
        
        print("Digite o numero de colunas (n1) da matriz A: ")
        n1 = input() 

        if not n1.isdigit():  
            print(f'Por favor, digite valor valido')
            continue   
        
        print("Digite o numero de Linhas (m2) da matriz B: ")
        m2 = input()

        if not m2.isdigit():  
            print(f'Por favor, digite valor valido')
            continue
            
        print("Digite o numero de colunas (n2) da matriz B: ")
        n2 = input()

        if not n2.isdigit():  
            print(f'Por favor, digite valor valido')
            continue
        
        if n1 != m2:
            print("\nNumero de colunas da matriz A (n1) deve ser igual ao numero de linhas (m2) da matriz B")
            continue
        
        # Executando processo da funcao gerar_matrizes_produto
        if int(choice) == 1:
            matrizes()
            gerar_matrizes_produto(int(m1), int(n1), int(m2), int(n2))
            desempenho()
            sys.exit()

        # Executando processo da funcao gerar_matrizes_prod_np
        elif int(choice) == 2:
            matrizes('matrizes/arquivos_saida_matrizes/matrizes_numpy.txt')
            gerar_matrizes_prod_np(int(m1), int(n1), int(m2), int(n2))
            desempenho(arquivo='matrizes/arquivos_saida_matrizes/desempenho_numpy.txt')
            sys.exit()

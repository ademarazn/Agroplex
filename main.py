import os
from os import system

from click.termui import pause

from problem1 import Problem1
from problem2 import Problem2
from problem3 import Problem3

from utils import header

__author__ = ["Ademar Zório Neto", "Carlos Felipe Almeida Gonçalo"]
__copyright__ = "Copyright 2017"
__credits__ = []
__version__ = "1.0"
__status__ = "Development"


os.environ['FOR_IGNORE_EXCEPTIONS'] = '1'
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'

if __name__ == "__main__":
    import sys

    while True:
        try:
            while True:
                system('cls')  # limpa a tela
                header()  # exibe nome do sistema, nomes dos desenvolvedores e telefone da FATEC Ourinhos
                # escolha de qual problema ser executado
                option = input(
                    ' 1. Determinar quantos hectares devem ser cultivados para cada uma das plantações e '
                    'tendo lucro máximo.\n'
                    ' 2. Determinar quantos hectares devem ser cultivados para cada uma das plantações e '
                    'quanto de cada criação deve ser mantido para maximizar a receita líquida.\n'
                    ' 3. Maximizar o valor presente das plantações e escolher quais cultivar.\n\n'
                    ' Qual problema deve ser executado? ')
                system('cls')  # limpa a tela
                header()  # exibe nome do sistema, nomes dos desenvolvedores e telefone da FATEC Ourinhos
                if option.__eq__('1'):
                    Problem1()
                    break
                elif option.__eq__('2'):
                    Problem2()
                    break
                elif option.__eq__('3'):
                    Problem3()
                    break
                else:
                    print(' Opção inválida!', end='\n\n')
                    pause(' Pressione qualquer tecla para continuar...')
            print(end='\n')
            # verificando se deseja executar o Agroplex novamente
            a = ''
            while not a.lower().startswith('s') and not a.lower().startswith('n'):
                a = input('\n Executar novamente? (S/N): ')

            if not a.lower().startswith('s'):  # então deseja finalizar o sistema
                print('\n Finalizando...', end='\n')
                break
        except KeyboardInterrupt:  # Ctrl+C foi pressionado
            print('\n\n Finalizando...', end='\n')
            break
    sys.exit(0)

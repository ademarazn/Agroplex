import pulp

import sys

from utils import ler_float, ler_int

__author__ = ["Ademar Zório Neto", "Carlos Felipe Almeida Gonçalo"]
__copyright__ = "Copyright 2017"
__credits__ = []
__version__ = "1.0"
__status__ = "Development"


class Problem3:
    def ler(self):
        while True:
            plant = input(' Qual é o nome da planta? ')
            self.x.append(pulp.LpVariable(plant, cat=pulp.LpBinary))
            ler = ''
            while not ler.lower().startswith('s') and not ler.lower().startswith('n'):
                ler = input(' Adicionar planta? (S/N): ')
            if not ler.lower().startswith('s'):
                break
        print(end='\n')

        # valores da função objetivo
        for i in range(len(self.x)):
            valor = ler_float(' Valor presente da plantação de {}: '.format(self.x[i].name))
            self.obj.append((self.x[i], valor))
        print(end='\n')

        # primeira restrição
        self.c.append([])
        for i in range(len(self.x)):
            valor = ler_float(' Despesa inicial da plantação de {}: '.format(self.x[i].name))
            self.c[0].append((self.x[i], valor))
        self.b.append(ler_float(' Despesa inicial máxima: '))
        print(end='\n')

        # segunda restrição
        self.c.append([])
        for i in range(len(self.x)):
            valor = ler_int(' Pessoal necessário na plantação de {}: '.format(self.x[i].name))
            self.c[1].append((self.x[i], valor))
        self.b.append(ler_float(' Disponibilidade máxima de pessoal: '))
        print(end='\n')

        # terceira restrição
        self.c.append([])
        for i in range(len(self.x)):
            valor = ler_float(' Capital de giro médio anual da plantação de {}: '.format(self.x[i].name))
            self.c[2].append((self.x[i], valor))
        self.b.append(ler_float(' Necessidade de capital de giro médio anual mínimo: '))
        print(end='\n')

        # quarta restrição
        self.c.append([])
        for i in range(len(self.x)):
            valor = ler_float(' Lucro anual estimado da plantação de {}: '.format(self.x[i].name))
            self.c[3].append((self.x[i], valor))
        self.b.append(ler_float(' Lucro anual mínimo: '))
        print(end='\n')

        # exclusividade
        for i in range(len(self.x)):
                print(' {} - {}'.format(i+1, self.x[i].name))
        while True:
            ler = ''
            while not ler.lower().startswith('s') and not ler.lower().startswith('n'):
                ler = input(' Adicionar exclusividade entre duas plantas? (S/N): ')
            if not ler.lower().startswith('s'):
                break
            self.xor.append([])
            while True:
                plant1 = ler_int(' Primeira planta: ')
                if 0 < plant1 <= len(self.x):
                    break
            while True:
                plant2 = ler_int(' Segunda planta: ')
                if 0 < plant2 <= len(self.x) and plant2 != plant1:
                    break
            pos = len(self.xor)-1
            self.xor[pos].append((self.x[plant1-1], 1))
            self.xor[pos].append((self.x[plant2-1], 1))
        print(end='\n')
        
        # plantas que só podem ser cultivadas em conjunto com outra
        for i in range(len(self.x)):
                print(' {} - {}'.format(i+1, self.x[i].name))
        while True:
            ler = ''
            while not ler.lower().startswith('s') and not ler.lower().startswith('n'):
                ler = input(' Adicionar planta que só pode ser cultivada em conjunto com outra? (S/N): ')
            if not ler.lower().startswith('s'):
                break
            self.c2.append([])
            while True:
                plant1 = ler_int(' Primeira planta: ')
                if 0 < plant1 <= len(self.x):
                    break
            while True:
                plant2 = ler_int(' Segunda planta: ')
                if 0 < plant2 <= len(self.x) and plant2 != plant1:
                    break
            pos = len(self.c2)-1
            self.c2[pos].append((self.x[plant1-1], -1))
            self.c2[pos].append((self.x[plant2-1], 1))
        print(end='\n')

    def __init__(self):
        try:
            self.modelo = pulp.LpProblem("Maximizar o valor presente", pulp.LpMaximize)

            self.x = []  # variáveis/plantas
            self.obj = []  # função objetivo
            self.b = []  # valores base
            self.c = []  # restrições
            self.xor = []  # exclusividade
            self.c2 = []  # plantas que só podem ser cultivadas em conjunto com outra
            self.ler()  # ler os dados

            print(" Resolvendo...", end="")

            self.modelo.setObjective(pulp.LpAffineExpression(self.obj))

            self.modelo += pulp.LpAffineExpression(self.c[0]) <= self.b[0]
            self.modelo += pulp.LpAffineExpression(self.c[1]) <= self.b[1]
            self.modelo += pulp.LpAffineExpression(self.c[2]) >= self.b[2]
            self.modelo += pulp.LpAffineExpression(self.c[3]) >= self.b[3]
            for i in range(len(self.xor)):
                self.modelo += pulp.LpAffineExpression(self.xor[i]) <= 1
            for i in range(len(self.c2)):
                self.modelo += pulp.LpAffineExpression(self.c2[i]) >= 0
            self.modelo.solve()
            # print(self.modelo)
            if self.modelo.status.__eq__(pulp.LpStatusOptimal):  # Modelo resolvido com sucesso
                print("\n\n Deve cultivar", end=" ")
                for i in range(len(self.x)):
                    if self.x[i].varValue == 1:
                        print(self.x[i].name, end=", ")
                print("e terá um valor presente de ${}.".format(pulp.value(self.modelo.objective)), end="")
            elif self.modelo.status.__eq__(pulp.LpStatusNotSolved):  # Falha ao solucionar
                print("\n\n Modelo não solucionado.", end=" ")
            elif self.modelo.status.__eq__(pulp.LpStatusInfeasible):  # Falha ao solucionar
                print("\n\n Falha ao solucionar. O problema parece ser inviável.", end=" ")
            elif self.modelo.status.__eq__(pulp.LpStatusUnbounded):  # Falha ao solucionar
                print("\n\n Falha ao solucionar. O problema parece ser ilimitado.", end=" ")
            elif self.modelo.status.__eq__(pulp.LpStatusUndefined):  # Falha ao solucionar
                print("\n\n Falha ao solucionar. O problema parece ser indefinido.", end=" ")
        except ValueError:
            print(end='')
        except KeyboardInterrupt:
            print('\n\n Finalizando...', end='\n')
            sys.exit(0)

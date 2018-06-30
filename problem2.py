import sys

from utils import ler_float, resolver

__author__ = ["Ademar Zório Neto", "Carlos Felipe Almeida Gonçalo"]
__copyright__ = "Copyright 2017"
__credits__ = []
__version__ = "1.0"
__status__ = "Development"


class Problem2:
    def ler(self):
        self.m = input(' Qual a medida agrária? (ex.: are, hectare, alqueire): ')
        print(end='\n')
        # Leitura dos nomes das N plantas
        while True:
            self.plants.append(input(' Qual é o nome da planta? '))
            ler = ''
            while not ler.lower().startswith('s') and not ler.lower().startswith('n'):
                ler = input(' Adicionar planta? (S/N): ')
            if not ler.lower().startswith('s'):
                break
        print(end='\n')
        # Leitura dos nomes dos N animais
        while True:
            self.animals.append(input(' Qual é o nome do animal? '))
            ler = ''
            while not ler.lower().startswith('s') and not ler.lower().startswith('n'):
                ler = input(' Adicionar animal? (S/N): ')
            if not ler.lower().startswith('s'):
                break
        print(end='\n')

        # leitura dos valores de receita líquida anual das plantações para a função objetivo
        for i in range(len(self.plants)):
            self.x.append(ler_float(' Receita líquida anual por {} de {}: '.format(self.m, self.plants[i])))

        # leitura dos valores de receita líquida anual das criações para a função objetivo
        for i in range(len(self.animals)):
            self.x.append(ler_float(' Receita líquida anual por {}: '.format(self.animals[i])))
        print(end='\n')

        self.t = ''
        while not self.t.lower().startswith('s') and not self.t.lower().startswith('n'):
            self.t = input(' Deseja adicionar trabalho dos membros mais jovens da família nas fazendas vizinhas durante'
                           ' o inverno e o verão? (S/N): ')
        if self.t.lower().startswith('s'):
            # leitura dos valores de custo por hora de trabalho dos membros mais jovens da família nas fazendas vizinhas
            # durante os meses do inverno e verão para a função objetivo
            self.x.append(ler_float(' Custo por hora de trabalho dos membros mais jovens da família nas fazendas '
                                    'vizinhas durante o inverno: '))
            self.x.append(ler_float(' Custo por hora de trabalho dos membros mais jovens da família nas fazendas '
                                    'vizinhas durante o verão: '))
        print(end='\n')

        # primeira restrição: área disponível
        self.r.append([])
        for i in range(len(self.plants)):
            self.r[0].append(1)

        for i in range(len(self.animals)):
            self.r[0].append(ler_float(' Quantos {}s de terra para cada {}? '.format(self.m, self.animals[i])))

        self.b.append(ler_float(' {} de terra disponíveis: '.format(self.m[0].upper() + self.m[1:] +
                                                                    ('s' if not self.m.endswith('s') else ''))))
        print(end='\n')

        # segunda restrição: fundos disponíveis para investimento
        self.r.append([])
        for i in range(len(self.plants)):
            self.r[1].append(ler_float(' Valor de investimento para {}: '.format(self.plants[i])))

        for i in range(len(self.animals)):
            self.r[1].append(ler_float(' Valor de investimento para cada {}: '.format(self.animals[i])))

        self.b.append(ler_float(' Fundos disponíveis para investimento: '))
        print(end='\n')

        # terceira restrição: homens-hora de trabalho durante o inverno
        self.r.append([])
        for i in range(len(self.plants)):
            self.r[2].append(ler_float(' Homens-hora por plantação de {} durante o inverno: '.format(self.plants[i])))

        for i in range(len(self.animals)):
            self.r[2].append(ler_float(' Homens-hora por criação de {} durante o inverno: '.format(self.animals[i])))

        self.b.append(ler_float(' Homens-hora disponíveis durante o inverno: '))
        print(end='\n')

        # quarta restrição: homens-hora de trabalho durante o verão
        self.r.append([])
        for i in range(len(self.plants)):
            self.r[3].append(ler_float(' Homens-hora por plantação de {} durante o verão: '.format(self.plants[i])))

        for i in range(len(self.animals)):
            self.r[3].append(ler_float(' Homens-hora por criação de {} durante o verão: '.format(self.animals[i])))

        self.b.append(ler_float(' Homens-hora disponíveis durante o verão: '))
        print(end='\n')

        var = 4
        var2 = 0
        # quinta..N restrições: número máximo de criação
        for i in range(len(self.animals)):
            self.r.append([])
            for j in range(var2 + len(self.plants)):
                self.r[var].append(0)
            self.r[var].append(1)
            for j in range(len(self.animals) - (var2 + 1)):
                self.r[var].append(0)
            self.b.append(ler_float(
                ' Número máximo de {}: '.format(self.animals[i] + ('s' if not self.animals[i].endswith('s') else ''))))
            var += 1
            var2 += 1

        #  Adiciona os valores caso os adicionou a opção de trabalho dos membros mais jovens...
        if self.t.lower().startswith('s'):
            for i in range(len(self.r)):
                if i == 2:
                    self.r[i].append(1)
                    self.r[i].append(0)
                elif i == 3:
                    self.r[i].append(0)
                    self.r[i].append(1)
                else:
                    self.r[i].append(0)
                    self.r[i].append(0)

    def __init__(self):
        try:
            self.m = ''  # Tipo da medida agrária
            self.t = ''  # Adicionou ou não a opção de trabalho dos membros mais jovens
            self.plants = []  # Nome das plantas
            self.animals = []  # Nome dos animais
            self.x = []  # Função objetivo, X1, X2, ...
            self.r = []  # Valores das restrições
            self.b = []  # Valores bases das restrições
            self.ler()  # Iniciar a leitura dos dados
            res = resolver(self)  # Resolver o problema
            # Resultado encontrado, exibindo a mensagem
            if res.status == 0:  # Modelo solucionado com sucesso
                print('\n\n Cultivando', end=' ')
                for i in range(len(self.plants)):
                    rx = int(res.x[i]) if res.x[i] % 1 == 0 else round(res.x[i], 2)
                    print('{} {} de {}'.format(rx if rx != 0 else 'nenhum', self.m if rx <= 1 else self.m + 's',
                                               self.plants[i]), end='')
                    print(',', end=' ')
                print('mantendo', end=' ')
                for i in range(len(self.animals)):
                    ii = len(self.plants) + i
                    rx = int(res.x[ii]) if res.x[ii] % 1 == 0 else round(res.x[ii], 2)
                    print('{} {}'.format(rx if rx != 0 else 'nenhum(a)',
                                         self.animals[i] + 's' if rx > 1 else self.animals[i]), end='')
                    if i == len(self.animals) - 2 and self.t.lower().startswith('n'):
                        print(' e ', end='')
                    else:
                        print(', ', end='')
                if self.t.lower().startswith('s'):
                    i = len(self.plants) + len(self.animals)
                    rx1 = int(res.x[i]) if res.x[i] % 1 == 0 else round(res.x[i], 2)
                    rx2 = int(res.x[i + 1]) if res.x[i + 1] % 1 == 0 else round(res.x[i + 1], 2)
                    print('alocando {} home{}-hora nos meses de inverno na fazenda vizinha e {} home{}-hora no verão,'
                          .format(rx1 if rx1 != 0 else 'nenhum', 'm' if rx1 <= 1 else 'ns', rx2 if rx2 != 0 else 'nenhum',
                                  'm' if rx2 <= 1 else 'ns', end=' '))
                rf = int(res.fun * -1) if res.fun * -1 % 1 == 0 else round(res.fun * -1, 2)
                print('terá uma receita líquida de ${}.'.format(rf), end='')
            elif res.status == 1:  # Falha ao solucionar
                print('\n\n Falha ao solucionar. Limite de iteração alcançado.', end='')
            elif res.status == 2:  # Falha ao solucionar
                print('\n\n Falha ao solucionar. O problema parece ser inviável.', end='')
            else:  # Falha ao solucionar
                print('\n\n Falha ao solucionar. O problema parece ser ilimitado.', end='')
        except ValueError:
            print(end='')
        except KeyboardInterrupt:
            print('\n\n Finalizando...', end='\n')
            sys.exit(0)

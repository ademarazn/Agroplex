import sys

from utils import ler_float, resolver

__author__ = ["Ademar Zório Neto", "Carlos Felipe Almeida Gonçalo"]
__copyright__ = "Copyright 2017"
__credits__ = []
__version__ = "1.0"
__status__ = "Development"


class Problem1:
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
        for i in range(len(self.plants)):
            self.x.append(ler_float(' Margem de lucro por {} de {}: '.format(self.m, self.plants[i])))
        print(end='\n')

        # Adicionando e realizando a leitura dos valores das restrições
        count = 0
        loop = True
        while loop:
            self.rt.append(input(' Qual restrição você deseja adicionar? (ex.: homens-horas): '))
            self.r.append([])
            for i in range(len(self.plants)):
                self.r[count].append(
                    ler_float(' {} por {} de {}: '.format(self.rt[count][0].upper() + self.rt[count][1:],
                                                          self.m, self.plants[i])))

            self.b.append(ler_float(' {} disponível: '.format(self.rt[count][0].upper() + self.rt[count][1:])))
            print(end='\n')
            count += 1
            ler = ''
            while not ler.lower().startswith('s') and not ler.lower().startswith('n'):
                ler = input(' Adicionar restrição? (S/N): ')
            if not ler.lower().startswith('s'):
                loop = False

    def __init__(self):
        try:
            self.m = ''  # Tipo da medida agrária
            self.plants = []  # Nome das plantas
            self.x = []  # Função objetivo, X1, X2, ...
            self.rt = []  # Nome das restrições
            self.r = []  # Valores das restrições
            self.b = []  # Valores bases das restrições
            self.ler()  # Iniciar a leitura dos dados
            res = resolver(self)  # Resolver o problema
            # Resultado encontrado, exibindo a mensagem
            if res.status == 0:  # Modelo solucionado com sucesso
                print('\n\n Plantando', end=' ')
                for i in range(len(self.plants)):
                    rx = int(res.x[i]) if res.x[i] % 1 == 0 else round(res.x[i], 2)
                    print('{} {} de {}'.format(rx if rx != 0 else 'nenhum', self.m if rx <= 1 else self.m + 's',
                                               self.plants[i]), end='')
                    if i < len(self.plants) - 1:
                        print(',', end=' ')
                rf = int(res.fun * -1) if res.fun * -1 % 1 == 0 else round(res.fun * -1, 2)
                if len(self.rt) == 1:
                    restrictions = " e "
                else:
                    restrictions = ", "
                for i in range(len(self.rt)):
                    rs = int(res.slack[i]) if res.slack[i] % 1 == 0 else round(res.slack[i], 2)
                    restrictions += ('não usando {} '.format(rs) if res.slack[i] != 0 else
                                     'usando todo(s)/toda(s) ') + self.rt[i]
                    if i == len(self.rt) - 2:
                        restrictions += ' e '
                    else:
                        restrictions += ', '
                print('{}terá um lucro de ${}.'.format(restrictions, rf), end='')
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

from numpy import multiply
from scipy.optimize import linprog

__author__ = ["Ademar Zório Neto", "Carlos Felipe Almeida Gonçalo"]
__copyright__ = "Copyright 2017"
__credits__ = []
__version__ = "1.0"
__status__ = "Development"


def header():
    print('\n Agroplex - © 2017\n\n'
          ' Ademar Zório Neto e Carlos Felipe Almeida Gonçalo\n'
          ' Faculdade de Tecnologia de Ourinhos - FATEC | Tel.: (14) 3512-2024\n\n')


def ler_float(text):
    while True:
        try:
            valor = float(input(text).replace(',', '.'))
            break
        except ValueError:
            continue
    return valor


def ler_int(text):
    while True:
        try:
            valor = int(input(text))
            break
        except ValueError:
            continue
    return valor


def resolver(self):
    print('\n Resolvendo...')
    r = self.r  # Restrição 1, 2, 3... ex.: [[X1, X2], [X1, X2], [X1, X2]]
    b = self.b  # valores bases das restrições

    # quando é para maximizar, multiplica por -1, ou seja, faz o inverso
    f = multiply(self.x, -1)  # valores da função objetivo

    xi_bounds = (0, None)

    return linprog(f, r, b, bounds=xi_bounds, options={"disp": False})

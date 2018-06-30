import sys
from cx_Freeze import setup, Executable

import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == 'win32':
    base = 'console'

executables = [
    Executable('main.py', base=base)
]

options = {
    'build_exe': {
        'packages': ["numpy", "Scipy", "click.termui", "sys", "PuLP"],
        'include_files': [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
        ],
        'include_msvcr': True
    },
}

setup(name='Agroplex',
      version='1.0',
      description='Resolva problemas do Agronegócio',
      options=options,
      executables=executables, requires=['cx_Freeze']
      )

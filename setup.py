import cx_Freeze
import sys

import os
import numpy.core._methods
import numpy.lib.format
import matplotlib

os.environ['TCL_LIBRARY'] = "C:\\Users\\User\\Anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\User\\Anaconda3\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("MAUFLEX.py", base=base, icon="E:\\INICTEL\\AguajesDeep\\Interfaz\\los_logos\\inictelico.ico")]

cx_Freeze.setup(
    name = "MAUFLEX",
    options = {"build_exe": {"packages":["tkinter","matplotlib"], "include_files":["aguaje_functions.py","tcl86t.dll","tcl86t.dll","los_logos/","Redes/"],
                             'includes': ['numpy.core._methods', 'numpy.lib.format']}},
    version = "1.0",
    description = "Software de Segmentación de Aguajes",
    executables = executables
    )
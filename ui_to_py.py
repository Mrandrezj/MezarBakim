# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PyQt5 import uic

with open('projeUI.py','w',encoding="utf-8") as fout:
          uic.compileUi('proje.ui', fout)

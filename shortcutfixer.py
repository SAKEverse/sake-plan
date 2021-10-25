# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:32:37 2021

@author: SuperComputer1
"""

import os

doit=True
conda_path=os.path.join(r"C:\Users",os.getlogin())
if 'miniconda3' in os.listdir(conda_path):
    conda_path=os.path.join(conda_path,r'miniconda3\Scripts','activate.bat')
elif 'anaconda3' in os.listdir(conda_path):
    conda_path=os.path.join(conda_path,r'anaconda3\Scripts','activate.bat')
else:
    print("Conda not found, recommend installing miniconda in user directory")
    input()
    doit=False

if doit == True:
    file = open("sake.cmd","w")
    lines=[]
    lines.append( r"call "+conda_path)
    lines.append( '\ncd '+os.getcwd() )
    lines.append( '\npipenv run python sake.py')
    file.writelines(lines)
    file.close()
    print("Shortcut Fixed!")
    input()
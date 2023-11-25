import os
import sys

file_dir = os.path.dirname(os.path.realpath('__file__')) #Obtener el directorio actual del archivo.
data_dir = file_dir + '\\data\\'
app_dir = file_dir + '\\app\\'

sys.path.insert(0, os.path.abspath(app_dir)) #Cambiar el path actual de trabajo al directorio del archivo.
sys.path.insert(1, os.path.abspath(file_dir)) #Cambiar el path actual de trabajo al directorio del archivo.

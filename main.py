import os
import re
import sys
from colorama import init
from termcolor import colored
import traceback
init()


DIRECTORIO = os.path.expanduser("./")
sys.path.append(DIRECTORIO)

from Lexer import *
from Parser import *
from Clases import *

PRACTICA = "03"  # Practica que hay que evaluar
DEBUG = True   # Decir si se lanzan mensajes de debug
NUMLINEAS = 3   # Numero de lineas que se muestran antes y después de la no coincidencia
MAX_LINEAS = 2000  # Maximo de lineas que se comprueban en el bucle de comparacion de la practica 1
sys.path.append(DIRECTORIO)
DIR = os.path.join(DIRECTORIO, PRACTICA, 'grading')
FICHEROS = os.listdir(DIR)
TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(DIR, fich)) and
         re.search(r"^[a-zA-Z].*\.(cs|test|cl)$",fich)]
TESTS.sort()
TESTS = ["badif.test"]

for fich in TESTS:
    lexer = CSharpLexer()
    f = open(os.path.join(DIR, fich), 'r', newline='')
    g = open(os.path.join(DIR, fich + '.out'), 'r', newline='')
    if os.path.isfile(os.path.join(DIR, fich)+'.nuestro'):
        os.remove(os.path.join(DIR, fich)+'.nuestro')
    if os.path.isfile(os.path.join(DIR, fich)+'.bien'):
        os.remove(os.path.join(DIR, fich)+'.bien')
    texto = ''
    entrada = f.read()
    f.close()
    if PRACTICA == '01':
        texto = '\n'.join(lexer.salida(entrada))
        texto = f'#name "{fich}"\n' + texto
        resultado = g.read()
        g.close()
        if texto.strip().split() != resultado.strip().split():
            print(f"Revisa el fichero {fich}")
            if DEBUG:
                our_output = texto.strip().split('\n')
                texto = re.sub(r'#\d+\b','',texto)
                resultado = re.sub(r'#\d+\b','',resultado)
                nuestro = [linea for linea in texto.split('\n') if linea]
                bien = [linea for linea in resultado.split('\n') if linea]
                linea = 0
                while nuestro[linea:linea+NUMLINEAS] == bien[linea:linea+NUMLINEAS] and linea < MAX_LINEAS:
                    linea += 1
                if linea == MAX_LINEAS:
                    print(f'Los números de línea no coinciden. Tu salida (compárala con el .out):')
                    for line in our_output:
                        print(line)
                    print('\n\n')
                else:
                    print(f'Líneas {linea+1}-{linea+NUMLINEAS+1}')
                    print(colored('\n'.join(nuestro[linea:linea+NUMLINEAS]), 'grey', 'on_red'))
                    print(colored('\n'.join(bien[linea:linea+NUMLINEAS]), 'grey', 'on_green'))
                f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                g = open(os.path.join(DIR, fich)+'.bien', 'w')
                f.write(texto.strip())
                g.write(resultado.strip())
                f.close()
                g.close()
    elif PRACTICA in ('02', '03'):
        parser = CSharpParser()
        parser.nombre_fichero = fich
        parser.errores = []
        bien = ''.join([c for c in g.readlines() if c and '#' not in c])
        g.close()
        j = parser.parse(lexer.tokenize(entrada))
        try:
            try:
                if PRACTICA == '03':
                    j.Tipo()
                if j and not parser.errores:
                    resultado = '\n'.join([c for c in j.str(0).split('\n')
                                           if c and '#' not in c])
                else:
                    resultado = '\n'.join(parser.errores)
                    resultado += '\n' + "Compilation halted due to lex and parse errors"
            except Exception as e:
                    resultado = f'{fich}: {str(e)}'
                    resultado += '\n' + "Compilation halted due to static semantic errors."
            if resultado.lower().strip().split() != bien.lower().strip().split():
                print(f"Revisa el fichero {fich}")
                if DEBUG:
                    nuestro = [linea for linea in resultado.split('\n') if linea]
                    bien = [linea for linea in bien.split('\n') if linea]
                    linea = 0
                    while nuestro[linea:linea+NUMLINEAS] == bien[linea:linea+NUMLINEAS]:
                        linea += 1
                    print(colored('\n'.join(nuestro[linea:linea+NUMLINEAS]), 'white', 'on_red'))
                    print(colored('\n'.join(bien[linea:linea+NUMLINEAS]), 'blue', 'on_green'))
                    f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                    g = open(os.path.join(DIR, fich)+'.bien', 'w')
                    f.write(resultado.strip())
                    g.write(bien.strip())
                    f.close()
                    g.close()
        except Exception as e:
            print(f"Lanza excepción en {fich} con el texto {e}")
            traceback.print_exc()
    elif PRACTICA == '04':
        parser = CSharpParser()
        parser.nombre_fichero = fich
        g.close()
        j = parser.parse(lexer.tokenize(entrada))
        try:
            out = j.codigo(0)
            exec(out)
            main = Main()
            orig_stdout = sys.stdout
            sys.stdout = open(os.path.join(DIR, fich)+'.nuestro', "w")
            main.main()
            sys.stdout.close()
            sys.stdout=orig_stdout 
            nuestro = open(os.path.join(DIR, fich)+'.nuestro','r')
            bien = open(os.path.join(DIR, fich)+'.out')

            nuestro_lines = nuestro.readlines()
            bien_lines = bien.readlines()

            for i in range(len(bien_lines)):
                if nuestro_lines[i] != bien_lines[i]:
                    print("Line " + str(i+1) + " doesn't match.")
                    print("Nuestro: " + nuestro_lines[i])
                    print("Bien: " + bien_lines[i])
                    print("------------------------")

            nuestro.close()
            bien.close()
        except Exception as e:
            print(f"Lanza excepción en {fich} con el texto {e}")
            traceback.print_exc()


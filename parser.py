import ply.yacc as yacc
import subprocess
import os
import sys
from CPP import CPP
from lexer import tokens
from lexer import lexer

variables = []

def p_program(p):
    '''program : GLOWNY LEWA_KLAMRA wyrazenia PRAWA_KLAMRA '''
    p[0] = (p[1], p[3])

def p_wyrazenia(p):
    '''wyrazenia : wyrazenia wyrazenie
                 | epsilon'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []
    
def p_wyrazenie(p):
    '''wyrazenie : CALKOWITA ID PRZYPISANIE LICZBA SREDNIK
                 | WYPISZ lista_id SREDNIK
                 | WCZYTAJ lista_id SREDNIK'''
    if len(p) == 6:
        nazwa = p[2]
        if nazwa in variables:
            print(f"Błąd semantyczny: zmienna '{nazwa}' już zdefiniowana, linia: {p.lineno(2)}")
            raise SyntaxError
        else:
            variables.append(nazwa)
        p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"
    
    if len(p) == 4:
        if p[1] == "wypisz" or "wczytaj_z_klawiatury":
            p[0] = f"{p[1]} {', '.join(p[2])}"


def p_lista_id(p):
    '''lista_id : lista_id PRZECINEK ID
                | ID'''
    if len(p) == 4:
        if p[3] not in variables:
            print(f"Błąd semantyczny: zmienna '{p[3]}' nie została zadeklarowana, linia: {p.lineno(3)}")
            raise SyntaxError
        p[0] = p[1] + [p[3]]
    else:
        if p[1] not in variables:
            print(f"Błąd semantyczny: zmienna '{p[1]}' nie została zadeklarowana, linia: {p.lineno(1)}")
            raise SyntaxError
        p[0] = [p[1]]


def p_wyrazenie_wypisz_error(p):
    '''wyrazenie : WYPISZ lista_id error
                 | WYPISZ error '''
    if len(p) == 4:
        print(f"Błąd składni: po 'wypisz' brakuje srednika lub zmiennej lub przecinka, linia: {p.lineno(1)}")
    elif len(p) == 3:
        print(f"Błąd składni: po 'wypisz' brakuje nazwy zmiennej, linia: {p.lineno(1)}")
    parser.errok() 

def p_wyrazenie_calkowita_error(p):
    '''wyrazenie : CALKOWITA ID PRZYPISANIE LICZBA error
                 | CALKOWITA ID PRZYPISANIE error
                 | CALKOWITA ID error
                 | CALKOWITA error '''
    
    if len(p) == 6:
        print(f"Błąd składni: po 'zmiennej' brakuje srednika, linia: {p.lineno(1)}")
    if len(p) == 5:
        print(f"Błąd składni: po 'zmiennej' brakuje liczby, linia: {p.lineno(1)}")
    if len(p) == 4:
        print(f"Błąd składni: po 'zmiennej' brakuje operatora przypisania, linia: {p.lineno(1)}")
    if len(p) == 3:
        print(f"Błąd składni: po 'zmiennej' brakuje nazwy, linia: {p.lineno(1)}")
    parser.errok() 

def p_epsilon(p):
    'epsilon :'
    p[0] = []

def p_error(p):
    pass        


parser = yacc.yacc()

with open("program.txt", "r", encoding="utf-8") as f:
    data = f.read()
    lexer.input(data)
    tok = lexer.token()
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)
    AST = parser.parse(data)
    print(AST)
    if AST != None:
        for symbol in AST[1]:
            if symbol == None:
                sys.exit(0)

        cpp_generator = CPP(AST)
        cpp_file = cpp_generator.create_cpp_file()
        cpp_generator.save(cpp_file)
        # cpp_generator.compile("output.cpp")


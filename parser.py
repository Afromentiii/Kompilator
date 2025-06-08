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
    '''wyrazenie : CALKOWITA ID PRZYPISANIE wyrazenie_arytmetyczne SREDNIK
                 | WYPISZ lista_id SREDNIK
                 | WCZYTAJ lista_id SREDNIK
                 | JEZELI LEWY_NAWIAS warunki_logiczne PRAWY_NAWIAS LEWA_KLAMRA wyrazenia PRAWA_KLAMRA
                 
                 '''
    if len(p) == 8:
        p[0] = [p[3]] + ['jezeli', p[6]]
    if len(p) == 6:
        nazwa = p[2]
        if nazwa in variables:
            print(f"Błąd semantyczny: zmienna '{nazwa}' już zdefiniowana, linia: {p.lineno(2)}")
            raise SyntaxError
        else:
            variables.append(nazwa)
        p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"
    
    if len(p) == 4:
        p[0] = f"{p[1]} {', '.join(p[2])}"

def p_warunki_logiczne(p):
    '''warunki_logiczne : warunki_logiczne KONIUNKCJA term
                        | warunki_logiczne ALTERNATYWA term
                        | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ' ' + p[2] + ' '+ p[3]

def p_wyrazenie_arytmetyczne(p):
    '''wyrazenie_arytmetyczne : wyrazenie_arytmetyczne PLUS term
                              | wyrazenie_arytmetyczne MINUS term
                              | wyrazenie_arytmetyczne RAZY term
                              | wyrazenie_arytmetyczne DZIELENIE term
                              | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '/' and (p[3] == 0 or p[3] == '0'):
            print(f"Błąd semantyczny: nie mozna dzielic przez 0, linia: {p.lineno(2)}")
            raise SyntaxError
        else:
            p[0] = p[1] + p[2] + p[3]
    
def p_term(p):
    '''term : ID
            | LICZBA'''
    if isinstance(p[1], str): 
        if p.slice[1].type == 'ID':
            if p[1] not in variables:
                print(f"Błąd semantyczny: zmienna '{p[1]}' nie została zadeklarowana, linia: {p.lineno(1)}")
                raise SyntaxError
    p[0] = p[1]

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

def p_wyrazenie_jezeli_error(p):
    '''wyrazenie : JEZELI LEWY_NAWIAS warunki_logiczne PRAWY_NAWIAS LEWA_KLAMRA wyrazenia error
                 | JEZELI LEWY_NAWIAS warunki_logiczne PRAWY_NAWIAS error
                 | JEZELI LEWY_NAWIAS warunki_logiczne error
                 | JEZELI LEWY_NAWIAS error
                 | JEZELI error'''

    if len(p) == 8:
        print(f"Błąd składni: po 'wyrażeniach' brakuje PRAWEJ_KLAMRY, linia: {p.lineno(1)}")
    elif len(p) == 6:
        print(f"Błąd składni: po 'prawym nawiasie' brakuje LEWEJ_KLAMRY, linia: {p.lineno(1)}")
    elif len(p) == 5:
        print(f"Błąd składni: po 'warunkach logicznych' brakuje PRAWEGO_NAWIASU, linia: {p.lineno(1)}")
    elif len(p) == 4:
        print(f"Błąd składni: po 'lewym nawiasie' brakuje WARUNKÓW_LOGICZNYCH, linia: {p.lineno(1)}")
    elif len(p) == 2:
        print(f"Błąd składni: po 'JEŻELI' brakuje LEWEGO_NAWIASU, linia: {p.lineno(1)}")

    sys.exit(1)
        

def p_wyrazenie_wypisz_error(p):
    '''wyrazenie : WYPISZ lista_id error
                 | WYPISZ error '''
    if len(p) == 4:
        print(f"Błąd składni: po 'wypisz' brakuje srednika lub zmiennej lub przecinka, linia: {p.lineno(1)}")
    elif len(p) == 3:
        print(f"Błąd składni: po 'wypisz' brakuje nazwy zmiennej, linia: {p.lineno(1)}")
    sys.exit(1)

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
    sys.exit(1)


def p_epsilon(p):
    'epsilon :'
    p[0] = []

def p_error(p):
    if p:
        print(f"Błąd składniowy przy tokenie '{p.value}', typ: {p.type}, linia: {p.lineno}")
    else:
        print("Błąd składniowy: nieoczekiwany koniec wejścia")


parser = yacc.yacc()

def main():
    if len(sys.argv) < 2:
        print("Użycie: python parser.py sciezka/do/pliku.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Plik '{file_path}' nie istnieje.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    
    lexer.input(data)
    # odkomentuj poniżej, jeśli chcesz zobaczyć tokeny
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)
    
    AST = parser.parse(data)
    print(AST)
    if AST is not None:
        for symbol in AST[1]:
            if symbol is None:
                sys.exit(0)

        cpp_generator = CPP(AST)
        cpp_file = cpp_generator.create_cpp_file()
        cpp_generator.save(cpp_file)
        # cpp_generator.compile("output.cpp")

if __name__ == "__main__":
    main()
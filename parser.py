import ply.yacc as yacc
from CPP import CPP
from lexer import tokens
from lexer import lexer
symbols = []

def p_program(p):
    '''program : GLOWNY LEWA_KLAMRA wyrazenia PRAWA_KLAMRA '''
    p[0] = (p[0], p[3])

def p_wyrazenia(p):
    '''wyrazenia : wyrazenia wyrazenie
                 | epsilon'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []
    
def p_wyrazenie(p):
    'wyrazenie : CALKOWITA ID PRZYPISANIE LICZBA SREDNIK'
    nazwa = p[2]
    if nazwa in symbols:
        print(f"Błąd semantyczny: zmienna '{nazwa}' już zdefiniowana, linia: {p.lineno(2)}")
        raise SyntaxError
    else:
        symbols.append(nazwa)
    p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"

def p_epsilon(p):
    'epsilon :'
    p[0] = []

def p_error(p):
    if p:
        print(f"Błąd składni w linii {p.lineno}, token: {p.value}")
    else:
        print("Błąd składni: nieoczekiwany koniec pliku")

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
    if AST != None:
        cpp_generator = CPP(AST)
        cpp_generator.create_cpp_file()


import ply.lex as lex
import ply.yacc as yacc

tokens = (
    #ZMIENNE
   'LICZBA',
   'ZMIENNA_CALKOWITA_SLOWO_KLUCZOWE',
   #OPERATORY ARYTMETYCZNE
   'PLUS',
   'MINUS',
   'RAZY',
   'DZIELENIE',
   #OPERATORY POROWNANIA
   'ROWNE',
   'WIEKSZE',
   'MNIEJSZE',
   'WIEKSZE_ROWNE',
   'MNIEJSZE_ROWNE',
   #OPERATORY LOGICZNE
   'KONIUNKCJA',
   'ALTERNATYWA',
   'NEGACJA',
   #OPERATORY PRZYPISANIA
   'PRZYPISANIE',
   #INSTRUKCJE
   'INSTRUKCJA_WARUNKOWA_SLOWO_KLUCZOWE',
   'WYPISANIE_NA_EKRANIE_SLOWO_KLUCZOWE',
   'WCZYTANIE Z KLAWIATURY_SLOWO_KLUCZOWE',
   'PETLA_DOPOKI_SLOWO_KLUCZOWE',
   #KOMENTARZE
   'KOMENTARZ_WIELOLINIJKOWY',
   'KOMENTARZ_JEDNOLINIJKOWY',
   #NAWIASY
   'LEWY_NAWIAS',
   'PRAWY_NAWIAS',
)

t_LICZBA = r'[0-9]+'
t_ZMIENNA_CALKOWITA = r'calkowita [a-zA-Z]+'

t_PLUS = r'\+'
t_MINUS = r'-'
t_RAZY = r'\*'
t_DZIELENIE = r':'

t_ROWNE = r'='
t_WIEKSZE = r'>'
t_WIEKSZE_ROWNE = r'>='
t_MNIEJSZE = r'<'

data = '''999 +++ 1 23 4  56436 24234 1'''

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
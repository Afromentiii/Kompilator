import ply.lex as lex
import ply.yacc as yacc

tokens = (
    #ZMIENNE
   'LICZBA',
   'ZMIENNA_CALKOWITA_SLOWO_KLUCZOWE',
   'NAZWA_ZMIENNEJ',
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
   'WCZYTANIE_Z_KLAWIATURY_SLOWO_KLUCZOWE',
   'PETLA_DOPOKI_SLOWO_KLUCZOWE',
   #KOMENTARZE
   'KOMENTARZ_WIELOLINIJKOWY',
   'KOMENTARZ_JEDNOLINIJKOWY',
   #NAWIASY
   'LEWY_NAWIAS',
   'PRAWY_NAWIAS',
)

#W REGEX ANALIZA ODBYWA SIE WZGLEDEM DLUGOSCI REGEXU, CZYLI DLUZSZE SA PIERWSZE W KOLEJNOSCi
t_LICZBA = r'[0-9]+'
t_ZMIENNA_CALKOWITA_SLOWO_KLUCZOWE = r'calkowita [a-zA-Z]+[0-9]*'

t_PLUS = r'\+'
t_MINUS = r'-'
t_RAZY = r'\*'
t_DZIELENIE = r':'

t_ROWNE = r'='
t_WIEKSZE = r'>'
t_WIEKSZE_ROWNE = r'>= '
t_MNIEJSZE = r'<'
t_MNIEJSZE_ROWNE = r'<='

t_KONIUNKCJA = r'oraz'
t_ALTERNATYWA = r'lub'
t_NEGACJA = r'nie'

t_PRZYPISANIE = r':='

t_INSTRUKCJA_WARUNKOWA_SLOWO_KLUCZOWE = r'jezeli'
t_WYPISANIE_NA_EKRANIE_SLOWO_KLUCZOWE = r'wypisz'
t_WCZYTANIE_Z_KLAWIATURY_SLOWO_KLUCZOWE = r'wczytaj_z_klawiatury'
t_PETLA_DOPOKI_SLOWO_KLUCZOWE = r'dopoki'

t_LEWY_NAWIAS = r'\('
t_PRAWY_NAWIAS = r'\)'

data = ''' ='''

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
    

parser = yacc.yacc()

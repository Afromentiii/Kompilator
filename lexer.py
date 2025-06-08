import ply.lex as lex

reserved = {
    'jezeli': 'JEZELI',
    'dopoki': 'DOPOKI',
    'wypisz': 'WYPISZ',
    'wczytaj_z_klawiatury': 'WCZYTAJ',
    'calkowita' : "CALKOWITA",
    'oraz': 'KONIUNKCJA',
    'lub': 'ALTERNATYWA',
    'nie': 'NEGACJA',
    'glowny' : 'GLOWNY',
}

tokens = [
    'LICZBA',
    'ID',
    'PLUS',
    'MINUS',
    'RAZY',
    'DZIELENIE',
    'ROWNE',
    'WIEKSZE',
    'MNIEJSZE',
    'WIEKSZE_ROWNE',
    'MNIEJSZE_ROWNE',
    'PRZYPISANIE',
    'LEWY_NAWIAS',
    'PRAWY_NAWIAS',
    'KOMENTARZ_JEDNOLINIJKOWY',
    'KOMENTARZ_WIELOLINIJKOWY',
    'LEWA_KLAMRA',
    'PRAWA_KLAMRA',
    'SREDNIK',
] + list(reserved.values())

# Regexy
t_PLUS = r'\+'
t_MINUS = r'-'
t_RAZY = r'\*'
t_DZIELENIE = r':'
t_ROWNE = r'='
t_WIEKSZE_ROWNE = r'>='
t_WIEKSZE = r'>'
t_MNIEJSZE_ROWNE = r'<='
t_MNIEJSZE = r'<'
t_PRZYPISANIE = r':='
t_LEWY_NAWIAS = r'\('
t_PRAWY_NAWIAS = r'\)'
t_LEWA_KLAMRA = r'\{'
t_PRAWA_KLAMRA = r'\}'
t_SREDNIK = r';'
# Liczby
def t_LICZBA(t):
    r'\d+'
    return t

# Identyfikatory i słowa kluczowe
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Komentarze
def t_KOMENTARZ_JEDNOLINIJKOWY(t):
    r'\@.*'
    pass


def t_KOMENTARZ_WIELOLINIJKOWY(t):
    r'\#\#(.|\n)*?\#\#' 
    t.lexer.lineno += t.value.count('\n')
    pass

# Nowe linie
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# Ignorowane znaki

# Obsługa błędów
def t_error(t):
    print(f"Nieprawidłowy znak: {t.value[0]} w linii {t.lineno}")

t_ignore  = ' \t'

# Tworzenie analizatora
lexer = lex.lex()
lexer.lineno = 0
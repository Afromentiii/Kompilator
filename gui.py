import tkinter as tk
from tkinter import filedialog, messagebox
import ply.yacc as yacc
import sys
import os

from lexer import tokens, lexer
from CPP import CPP
import parser as parser_module  

def run_parser(file_path):
    parser_module.variables.clear()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
            lexer.input(data)

            AST = parser_module.parser.parse(data)
            if AST is None:
                return "Nieprawidłowa składnia lub błąd semantyczny."

            for symbol in AST[1]:
                if symbol is None:
                    return "Błąd semantyczny."

            cpp_generator = CPP(AST)
            cpp_file = cpp_generator.create_cpp_file()
            cpp_generator.save(cpp_file)

            return f"Kod C++ zapisany jako: {cpp_file}"

    except Exception as e:
        return f"Błąd: {e}"

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def execute():
    path = entry_path.get()
    if not path:
        messagebox.showwarning("Brak pliku", "Podaj ścieżkę do pliku!")
        return
    result = run_parser(path)
    messagebox.showinfo("Wynik", result)

root = tk.Tk()
root.title("Parser języka własnego")

tk.Label(root, text="Ścieżka do pliku:").pack(pady=5)
entry_path = tk.Entry(root, width=50)
entry_path.pack(padx=10)
tk.Button(root, text="Przeglądaj", command=browse_file).pack(pady=5)
tk.Button(root, text="Uruchom parser", command=execute).pack(pady=10)

root.mainloop()

import subprocess
import os

class CPP:
    def __init__(self, AST):
            self.AST = AST
            self.code_lines = []
            self.cpp_equal = "="
            self.semicolon = ";"

    def create_main(self):
        self.code_lines.append("#include <iostream> \n")
        self.code_lines.append("using namespace std; \n")
        self.code_lines.append("int main() { \n")
    
    def ast_travelsal(self):
         for symbol in self.AST[1]:
              tokens = symbol.split()
              if (tokens[0] == "calkowita"):
                   line = self.create_int(tokens)
                   self.code_lines.append(line)
              if(tokens[0] == "wypisz"):
                   line = self.create_cout(tokens)
                   self.code_lines.append(line)
                   
    def create_cout(self, tokens):
         cpp_cout = "cout <<"
         cpp_cout_value = tokens[1]
         return cpp_cout + cpp_cout_value

    def create_int(self, tokens):
        cpp_int = "int"
        cpp_name = tokens[1]
        cpp_value = tokens[3]
        return cpp_int + " " + cpp_name + " " + self.cpp_equal + " " + cpp_value + self.semicolon + "\n"

    def create_cpp_file(self):
         self.create_main()
         self.ast_travelsal()
         self.code_lines.append("return 0;")
         self.code_lines.append("\n}")
         print(self.AST)
        
         output = str()
         for line in self.code_lines:
            output += line
         print(output)
         return output
    
    def save(self, output):
         with open("output.cpp", "w", encoding="utf-8") as f:
            f.write(output)

    def compile(self, cpp_filename):
        executable_name = "output.exe" if os.name == "nt" else "output"
        compile_command = ["g++", cpp_filename, "-o", executable_name]
        try:
            result = subprocess.run(compile_command, check=True, capture_output=True, text=True)
            print("Kompilacja zakończona sukcesem.")
            print(f"Plik wykonywalny: {executable_name}")
        except subprocess.CalledProcessError as e:
            print("Błąd kompilacji:")
            print(e.stderr)
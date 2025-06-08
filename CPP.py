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
    
    def ast_travelsal(self, AST):
        for symbol in AST[1]:
            if isinstance(symbol, list) and symbol[0] == "jezeli":
                self.code_lines.append("if (true) {\n")  
                self.ast_travelsal(('blok', symbol[1]))
                self.code_lines.append("}\n")
            elif isinstance(symbol, str):
                tokens = symbol.split()
                if tokens[0] == "calkowita":
                    self.code_lines.append(self.create_int(tokens))
                elif tokens[0] == "wypisz":
                    self.code_lines.append(self.create_cout(tokens))
                elif tokens[0] == "wczytaj_z_klawiatury":
                    self.code_lines.append(self.create_cin(tokens))

    def ast_inside_travelsal(self, AST):
         for symbol in AST[1]:
              tokens = symbol.split()
              if (tokens[0] == "calkowita"):
                   line = self.create_int(tokens)
                   self.code_lines.append(line)
              if(tokens[0] == "wypisz"):
                   line = self.create_cout(tokens)
                   self.code_lines.append(line)
              if(tokens[0] == "wczytaj_z_klawiatury"):
                   line = self.create_cin(tokens)
                   self.code_lines.append(line)
              if(tokens[0] == "jezeli"):
                  continue
                                     
                   
    def create_cout(self, tokens):
        # print(tokens)
        args = tokens[1:]
        args_clean = [token.replace(',', '') for token in args]
        cpp_cout_value =  ' << " " << '.join(args_clean)
        return "cout << " + cpp_cout_value + " << endl;\n"
    
    def create_cin(self, tokens):
        #print(tokens)
        args = tokens[1:]
        args_clean = [token.replace(',', '') for token in args]
        cpp_cout_value = " >> ".join(args_clean)
        return "cin >> " + cpp_cout_value + ";\n"
    
    # def generate_if(self, symbol):
    #      self.code_lines.append("if () {\n")
    #      self.ast_travelsal(symbol[1])
    #      self.code_lines.append("}\n")

    def create_int(self, tokens):
        cpp_int = "int"
        cpp_name = tokens[1]
        cpp_value = tokens[3]
        return cpp_int + " " + cpp_name + " " + self.cpp_equal + " " + cpp_value + self.semicolon + "\n"

    def create_cpp_file(self):
         self.create_main()
         self.ast_travelsal(self.AST)
         self.code_lines.append("return 0;")
         self.code_lines.append("\n}")
        
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
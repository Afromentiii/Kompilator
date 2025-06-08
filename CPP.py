class CPP:
    def __init__(self, AST):
            self.AST = AST
            self.code_lines = []

    def create_main(self):
        self.code_lines.append("#include <iostream>; \n")
        self.code_lines.append("using namespace std; \n")
        self.code_lines.append("void main() { \n")
        self.code_lines.append("\n}")

    def create_cpp_file(self):
         self.create_main()
         for line in self.code_lines:
              print(line, end="")

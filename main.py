from lexer import tokenize
from parser import Parser
from codegen import generate_c

if __name__ == '__main__':
    print("Enter your pseudo-code (end with an empty line):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    pseudocode = "\n".join(lines)

    tokens = tokenize(pseudocode)
    parser = Parser(tokens)
    ast = parser.parse()
    c_code = generate_c(ast)

    with open("output.c", "w") as f:
        f.write(c_code)
    print("\nC code has been written to output.c")

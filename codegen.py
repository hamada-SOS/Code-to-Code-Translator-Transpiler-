from parser import *

def generate_c(ast):
    lines = ["#include <stdio.h>", "int main() {"]
    declared_vars = set()
    string_vars = set()

    def emit(node, indent=4):
        sp = ' ' * indent
        if isinstance(node, Assignment):
            val = generate_expr(node.value)
            if node.var not in declared_vars:
                lines.append(f"{sp}int {node.var} = {val};")
                declared_vars.add(node.var)
            else:
                lines.append(f"{sp}{node.var} = {val};")

        elif isinstance(node, Read):
            if node.var not in declared_vars:
                lines.append(f"{sp}int {node.var};")
                declared_vars.add(node.var)
            lines.append(f'{sp}scanf("%d", &{node.var});')

        elif isinstance(node, ReadStr):
            if node.var not in string_vars:
                lines.append(f"{sp}char {node.var}[100];")
                string_vars.add(node.var)
            lines.append(f'{sp}scanf("%s", {node.var});')

        elif isinstance(node, Print):
            if node.value in string_vars:
                lines.append(f'{sp}printf("%s\\n", {node.value});')
            elif node.value in declared_vars:
                lines.append(f'{sp}printf("%d\\n", {node.value});')
            else:
                lines.append(f'{sp}printf("%s\\n", "{node.value}");')

        elif isinstance(node, ForLoop):
            lines.append(f"{sp}for (int {node.var} = {node.start}; {node.var} <= {node.end}; {node.var}++) {{")
            declared_vars.add(node.var)
            for stmt in node.body:
                emit(stmt, indent + 4)
            lines.append(f"{sp}}}")

        elif isinstance(node, WhileLoop):
            cond = generate_expr(node.condition)
            lines.append(f"{sp}while ({cond}) {{")
            for stmt in node.body:
                emit(stmt, indent + 4)
            lines.append(f"{sp}}}")

        elif isinstance(node, IfElse):
            cond = generate_expr(node.condition)
            lines.append(f"{sp}if ({cond}) {{")
            for stmt in node.if_body:
                emit(stmt, indent + 4)
            lines.append(f"{sp}}} else {{")
            for stmt in node.else_body:
                emit(stmt, indent + 4)
            lines.append(f"{sp}}}")

    def generate_expr(expr):
        if isinstance(expr, BinaryOp):
            left = generate_expr(expr.left)
            right = generate_expr(expr.right)
            return f"{left} {expr.op} {right}"
        return str(expr)

    for stmt in ast.statements:
        emit(stmt)

    lines.append("    return 0;")
    lines.append("}")
    return "\n".join(lines)

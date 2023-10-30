import ast
from miasm.expression.expression import *

# 문자열로부터 파이썬 AST 노드 생성
input_expr_str = "1 + Concat(mem32[130+EBP], mem32[129+EBP], mem32[128+EBP], mem32[127+EBP])"
python_ast = ast.parse(input_expr_str, mode="eval")
print(ast.dump(python_ast))
visitor = ast.NodeVisitor()
print(visitor.visit(python_ast))

# 파싱할 파이썬 코드 문자열
python_code = "a = 10 + 5"

# 파싱하여 AST 생성
parsed_ast = ast.parse(python_code)

# NodeVisitor를 상속한 사용자 정의 클래스 생성
class MyVisitor(ast.NodeVisitor):
    def visit_BinOp(self, node):
        print("Binary Operation:", node.op)
        self.generic_visit(node)  # 하위 노드 순회

    def visit_Assign(self, node):
        print("Assignment:", node.targets[0].id)
        self.generic_visit(node)

# 사용자 정의 Visitor 객체 생성
my_visitor = MyVisitor()

# AST를 순회하며 Visitor 객체를 통해 노드 방문
my_visitor.visit(python_ast)



# AST 노드를 Miasm의 Expr 표현식으로 변환
# def python_ast_to_miasm_expr(node):
#     if isinstance(node, ast.BinOp):
#         op = node.op
#         left = python_ast_to_miasm_expr(node.left)
#         right = python_ast_to_miasm_expr(node.right)
#         if isinstance(op, ast.Add):
#             return ExprOp("+", left, right)
#         elif isinstance(op, ast.Sub):
#             return ExprOp("-", left, right)
#         elif isinstance(op, ast.Mult):
#             return ExprOp("*", left, right)
#         # 더 많은 연산자에 대한 처리 추가 필요
#     elif isinstance(node, ast.Name):
#         return ExprId(node.id)
#     elif isinstance(node, ast.Num):
#         return ExprInt(node.n, 32)  # 32비트 정수로 가정
#
# miasm_expr = python_ast_to_miasm_expr(python_ast)
#
# # 생성된 Miasm 표현식 출력
# print(miasm_expr)

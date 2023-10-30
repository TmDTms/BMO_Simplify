from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz


num = ExprInt(6, 32)

concat_num = ExprInt(82, 32)
reg = ExprId('EBP', 32)
mem = ExprMem(concat_num + reg, 32)
original = ExprOp('+', num, mem)

concat_num1 = ExprInt(82, 8)
concat_num2 = ExprInt(81, 8)
concat_num3 = ExprInt(80, 8)
concat_num4 = ExprInt(79, 8)

reg1 = ExprId('EBP', 8)

mem1 = ExprMem(concat_num1 + reg1, 8)
mem2 = ExprMem(concat_num2 + reg1, 8)
mem3 = ExprMem(concat_num3 + reg1, 8)
mem4 = ExprMem(concat_num4 + reg1, 8)

compose = ExprCompose(mem1, mem2, mem3, mem4)
concat = ExprOp('+', num, compose)
canon = ExprVisitorCanonize()
res = canon.canonize(concat)
print(res)
origin_node = original.args
concat_node = concat.args
result = None
for node in concat_node:
    if isinstance(node, ExprCompose):
        compose_list = node.args
        for arg in compose_list:
            if str(mem.ptr) == str(arg.ptr):
                result = ExprOp('+', num, mem)
                break
        break
print("original : ", original)
print("concat : ", concat)
print("result : ", result)

# g = result.graph()
# open('a_8.dot', 'w').write(g.dot())
# with open('a_8.dot') as f:
#     dot_graph = f.read()
# graph = graphviz.Source(dot_graph)
# graph.view()

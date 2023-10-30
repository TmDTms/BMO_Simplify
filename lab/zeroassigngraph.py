from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz


num = ExprInt(6, 32)

concat_num1 = ExprInt(82, 8)
concat_num2 = ExprInt(81, 8)
concat_num3 = ExprInt(80, 8)
concat_num4 = ExprInt(79, 8)

reg = ExprId('EBP', 8)

mem1 = ExprMem(concat_num1 + reg, 8)
mem2 = ExprMem(concat_num2 + reg, 8)
mem3 = ExprMem(concat_num3 + reg, 8)
mem4 = ExprMem(concat_num4 + reg, 8)

compose = ExprCompose(mem1, mem2, mem3, mem4)
concat = ExprCompose(num, compose)

g = concat.graph()

open('a_8.dot', 'w').write(g.dot())
with open('a_8.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

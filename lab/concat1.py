from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz

num1 = ExprInt(144, 8)
num2 = ExprInt(82, 8)
reg = ExprId('EBP', 8)
one = ExprInt(1, 8)
zero = ExprInt(0, 8)

mem1 = ExprMem(num1 + reg, 32)
in_mem = ExprMem(num2 + reg, 8)
in_mem2 = ExprMem(one + in_mem, 8)
# concat = ExprCompose(zero, in_mem2, in_mem, zero)
mem2 = ExprMem(in_mem2 + in_mem, 32)

result = ExprOp('+', mem1, mem2)
g = result.graph()

open('a_8.dot', 'w').write(g.dot())
with open('a_8.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz

print("1st Expression graph")

a = ExprId('A', 32)
zero = ExprInt(0, 8)
assign_lst = []

for i in range(4):
    slice_expr = ExprSlice(a, i*8, (i+1)*8)
    a_i = ExprMem(slice_expr, 8)
    zero_assign = ExprAssign(a_i, zero)
    assign_lst.append(zero_assign)

compose = ExprCompose(*assign_lst)
g = compose.graph()
open('ex.dot', 'w').write(g.dot())
with open('ex.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()
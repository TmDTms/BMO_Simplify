from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz

print("1st Expression graph")

a = ExprId('A', 32)
a_mem = ExprMem(a, 32)
zero = ExprInt(0, 32)
zero_assign = ExprAssign(a_mem, zero)

compose = ExprCompose(zero_assign)
g = compose.graph()

# open('ex1.dot', 'w').write(g.dot())
# with open('ex1.dot') as f:
#     dot_graph = f.read()
# graph = graphviz.Source(dot_graph)
# graph.view()

print("2nd Expression 4 Slicing graph")
a1 = ExprId('A', 32)
zero1 = ExprInt(0, 8)
assign_lst = []

for i in range(4):
    slice_expr = ExprSlice(a1, i*8, (i+1)*8)
    a_i = ExprMem(slice_expr, 8)
    zero_assign = ExprAssign(a_i, zero1)
    assign_lst.append(zero_assign)

compose1 = ExprCompose(*assign_lst)
g1 = compose1.graph()

print(g.leaves())
print(g1.leaves())

# open('ex2.dot', 'w').write(g1.dot())
# with open('ex2.dot') as f:
#     dot_graph = f.read()
# graph = graphviz.Source(dot_graph)
# graph.view()
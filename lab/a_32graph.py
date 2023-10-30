from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz

a = ExprId('A', 32)
a_mem = ExprMem(a, 32)
zero = ExprInt(0, 32)
zero_assign = ExprAssign(a_mem, zero)

compose = ExprCompose(zero_assign)
g = compose.graph()

open('ex1.dot', 'w').write(g.dot())
with open('ex1.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

from miasm.expression.expression import *
from miasm.expression.parser import *
import graphviz

string = "Concat(mem32[144+EBP],mem32[143+EBP],mem32[142+EBP],mem32[141+EBP])+mem32[Concat(mem32[82+EBP],mem32[81+EBP],mem32[80+EBP],mem32[79+EBP])],0)"

def make_mem(num, reg):
    result = []
    for i in range(4):
        offset = ExprInt(num + i, 8)
        mem = ExprMem(offset + reg, 8)
        result.append(mem)
    return result

num1 = 144
num2 = 82
reg = ExprId('EBP', 8)
mem_list = make_mem(num1, reg)
concat1 = ExprCompose(*mem_list)

mem_list = make_mem(num2, reg)
mem_in_concat = ExprCompose(*mem_list)

one = ExprInt(1, 32)
mem1 = ExprMem(one + mem_in_concat, 8)
mem2 = ExprMem(mem_in_concat, 8)
zero = ExprInt(0, 8)
concat2 = ExprCompose(zero, mem1, mem2, zero)

result = ExprOp('+', concat1, concat2)

g = result.graph()
open('a_8.dot', 'w').write(g.dot())
with open('a_8.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

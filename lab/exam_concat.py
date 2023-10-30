from miasm.expression.expression import *
from miasm.expression.parser import *
from miasm.expression.expression_helper import *
from miasm.expression.simplifications import *
from concat_transformer_origin import ConcatTransformer
import graphviz

def make_mem(num, reg):
    result = []
    for i in range(4):
        offset = ExprInt(num - i, 32)
        mem = ExprMem(offset + reg, 32)
        result.append(mem)
    return result


# Concat(mem32[82+EBP],mem32[81+EBP],mem32[80+EBP],mem32[79+EBP])
reg = ExprId("EBP", 32)
num1 = 13
num2 = 156
num3 = ExprInt(4066502282, 128)
mem_list1 = make_mem(num1, reg)
mem_list2 = make_mem(num2, reg)
concat1 = ExprCompose(*mem_list1)
concat2 = ExprCompose(*mem_list2)
num4 = ExprInt(4294967295, 128)
op1 = ExprOp('*', num4, concat2)
op2 = ExprOp('+', num3, concat1)
res = ExprOp('+', op1, op2)
ct = ConcatTransformer(res)
result_expr = ct.replace_unsafe_concat_to_mem()

print(result_expr)

g = result_expr.graph()
open('a_8.dot', 'w').write(g.dot())
with open('a_8.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

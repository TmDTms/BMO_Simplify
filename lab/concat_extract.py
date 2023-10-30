from miasm.expression.expression import *
from miasm.expression.parser import *
from concat_transformer_origin import *
import graphviz

# Concat(mem32[82+EBP],mem32[81+EBP],mem32[80+EBP],mem32[79+EBP]) + 256 + Concat(mem32[130+EBP],mem32[129+EBP],mem32[128+EBP],mem32[127+EBP])
def make_mem(num, reg):
    result = []
    for i in range(4):
        offset = ExprInt(num - i, 32)
        mem = ExprMem(offset + reg, 32)
        result.append(mem)
    return result

num1 = 130
reg1 = ExprId('ESP', 32)
mem_list1 = make_mem(num1, reg1)
concat1 = ExprCompose(*mem_list1)
print(concat1)
num2 = 82
reg2 = ExprId('EBP', 32)
mem_list = make_mem(num2, reg2)
concat2 = ExprCompose(*mem_list)
expression = ExprOp('+', concat2, ExprInt(256, 128), concat1)
zero = ExprInt(0, 128)
assign_zero = ExprAssign(expression, zero)
ct = ConcatTransformer(assign_zero)
result = ct.replace_unsafe_concat_to_mem()
print('Concat(mem32[82+EBP],mem32[81+EBP],mem32[80+EBP],mem32[79+EBP]) + 256 + Concat(mem32[130+EBP],mem32[129+EBP],mem32[128+EBP],mem32[127+EBP]) = 0')
print(result)

# g = result.graph()
#
# open('a_8.dot', 'w').write(g.dot())
# with open('a_8.dot') as f:
#     dot_graph = f.read()
# graph = graphviz.Source(dot_graph)
# graph.view()

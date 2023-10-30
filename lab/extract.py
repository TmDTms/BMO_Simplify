from miasm.expression.expression import *
from miasm.expression.parser import *
from concat_transformer_origin import *
import graphviz

# Extract(2, 2, mem32[28+ESP])
# Extract(4, 4, mem32[30+ESP])
# Extract(6, 0, mem32[2+ESP])

num1 = ExprInt(28, 32)
reg = ExprId('ESP', 32)
mem1 = ExprMem(num1 + reg, 32)

num2 = ExprInt(30, 32)
mem2 = ExprMem(num2 + reg, 32)

num3 = ExprInt(2, 32)
mem3 = ExprMem(num3 + reg, 32)

et1 = ExtractTransformer(2, 2, mem1)
result1 = et1.make_extract_to_exprmem()
et2 = ExtractTransformer(4, 4, mem2)
result2 = et2.make_extract_to_exprmem()

print('Extract(2, 2, mem32[28+ESP])')
print(result1)
print('Extract(4, 4, mem32[30+ESP])')
print(result2)
try:
    et3 = ExtractTransformer(6, 0, mem3)
    result3 = et3.make_extract_to_exprmem()
    print('Extract(6, 0, mem32[2+ESP])')
    print(result3)
except:
    print('Error : offset == 0')


# g = result.graph()
#
# open('a_8.dot', 'w').write(g.dot())
# with open('a_8.dot') as f:
#     dot_graph = f.read()
# graph = graphviz.Source(dot_graph)
# graph.view()

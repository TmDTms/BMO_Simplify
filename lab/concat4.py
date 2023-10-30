from miasm.expression.expression import *
from miasm.expression.parser import *
from miasm.expression.expression_helper import *
from miasm.expression.simplifications import *
import graphviz

def make_mem(num, reg):
    result = []
    for i in range(4):
        offset = ExprInt(num + i, 8)
        mem = ExprMem(offset + reg, 8)
        result.append(mem)
    return result

num = 127
reg = ExprId("EBP", 8)
mem_list = make_mem(num, reg)
concat = ExprCompose(*mem_list)
op1 = ExprOp('^', concat, ExprInt(106, 32))
op2 = ExprOp('+', op1, ExprId("EBP", 32))

args = op2.args
for arg in args:
    print(arg)
dict_op = op2.args2expr
for key, value in dict_op.items():
    print(key, value)

result = op2.canonize()
lst = result.args2expr
concat_element = []
for key in lst.keys():
    print("key : ", key, " / value : ", lst[key])
    if isinstance(lst[key], ExprCompose):
        concat_element.append(merge_sliceto_slice(lst[key]))
        break
print(concat)
for e in concat_element[0]:
    print(e)
replace_dict = {concat: ExprMem(concat_element[0][0].ptr, 32)}
print(replace_dict)
op3 = op2.replace_expr(replace_dict)
print(op3)
print(concat)
from miasm.expression.expression import *
from miasm.expression.parser import *
from miasm.expression.expression_helper import *
from miasm.expression.simplifications import *
import graphviz

def make_mem(num, reg):
    result = []
    for i in range(4):
        offset = ExprInt(num - i, 32)
        mem = ExprMem(offset + reg, 32)
        result.append(mem)
    return result

def concat_slicing(dict):
    result = []
    for key, value in dict.copy().items():
        if isinstance(value, ExprCompose):
            result.append(merge_sliceto_slice(value))
    return result

def is_reg(lst):
    for mem in lst:
        if isinstance(mem, ExprMem) and mem.ptr.args[1].name not in ['ESP', 'EBP']:
            return False
    return True

def sub_one(x, y):
    return x.ptr.args[0].arg - y.ptr.args[0].arg == 1

def is_4expr_sub(lst):
    if len(lst) != 4:
        return False
    for i in range(3):
        if not sub_one(lst[i], lst[i+1]):
            return False
    return True

def is_concat(dict):
    concat_list = concat_slicing(dict)
    for lst in concat_list:
        if is_reg(lst) and is_4expr_sub(lst):
            return True
    return False

def replace_dictionary(concat_list, element_list):
    result = {}
    for concat in concat_list:
        for element in element_list:
            if list(concat.args) == element:
                result[concat] = ExprMem(element[0].ptr, 128)
                break
    return result

# Concat(mem32[130+EBP],mem32[129+EBP],mem32[128+EBP],mem32[127+EBP])^106+EBP
# num = 130
# reg = ExprId("EBP", 32)
# mem_list = make_mem(num, reg)
# concat = ExprCompose(*mem_list)
# op1 = ExprOp('^', concat, ExprInt(106, 128))
# op2 = ExprOp('+', op1, ExprId("EBP", 128))

# Concat(mem32[82+EBP],mem32[81+EBP],mem32[80+EBP],mem32[79+EBP])
# reg = ExprId("EBP", 8)
# num = 82
# mem_list = make_mem(num, reg)
# concat = ExprCompose(*mem_list)

# Concat(mem32[4294967295+ESP],mem32[4294967294+ESP],mem32[4294967293+ESP],mem32[4294967292+ESP])
# reg = ExprId("ESP", 32)
# num = 4294967295
# mem_list = make_mem(num, reg)
# concat = ExprCompose(*mem_list)

# Concat(mem32[3+ESP],mem32[2+ESP],mem32[1+ESP],mem32[ESP]) + Concat(mem32[82+EBP],mem32[81+EBP],mem32[80+EBP],mem32[79+EBP]
reg1 = ExprId("ESP", 32)
reg2 = ExprId("EBP", 32)
num1 = 3
num2 = 82
num3 = 140
mem_list1 = make_mem(num1, reg1)
concat1 = ExprCompose(*mem_list1)
mem_list2 = make_mem(num2, reg2)
concat2 = ExprCompose(*mem_list2)
mem_list3 = make_mem(num3, reg2)
concat3 = ExprCompose(*mem_list3)
concat_lst = [concat1, concat2, concat3]
op = ExprOp('+', concat1, concat2, concat3)

zero = ExprInt(0, 128)
assign_zero = ExprAssign(op, zero)
print(assign_zero)
op_dict = assign_zero.args2expr
first_mem = concat_slicing(op_dict)

result = assign_zero
replace_dict = replace_dictionary(concat_lst, concat_slicing(op_dict))
if is_concat(op_dict):
    result = assign_zero.replace_expr(replace_dict)
else:
    result = assign_zero
print(result)

g = result.graph()
open('a_8.dot', 'w').write(g.dot())
with open('a_8.dot') as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

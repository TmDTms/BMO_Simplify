from miasm.expression.expression import *
from miasm.expression.parser import *
from miasm.expression.expression_helper import *
import graphviz

def make_mem(num, reg):
    result = []
    for i in range(4):
        offset = ExprInt(num + i, 8)
        mem = ExprMem(offset + reg, 8)
        result.append(mem)
    return result

def is_equal(dict1, dict2):
    if len(dict1) != len(dict2):
        return False
    for key, value in dict1.items():
        if key not in dict2 or dict2[key] != value:
            return False
    return True


reg = ExprId('EBP', 8)

num1 = 144
num2 = 82
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

lst = merge_sliceto_slice(mem_in_concat)
print(lst)
for i in lst:
    print(i)

sol = possible_values(mem_in_concat)
for consval in sol:
    print("For value %s" % consval.value)
    for constraint in consval.constraints:
        print("\t%s" % constraint.to_constraint())
import pandas as pd
import re
from miasm.expression.expression import *
from miasm.expression.parser import *


def big_tokenizer(expression):
    tokens = re.findall(r'\w+|\S', expression)
    p_stack = []
    b_stack = []
    op_stack = []
    etc_stack = []
    expr_len = len(tokens)
    for i in range(expr_len):
        if tokens[i] in ['Concat', 'Extract']:
            p_stack.append((tokens[i] + '(', i))
        elif tokens[i] in [')']:
            p_stack.append((tokens[i], i))
        elif tokens[i] in ['[']:
            b_stack.append(('mem32' + tokens[i], i))
        elif tokens[i] in [']']:
            b_stack.append((tokens[i], i))
        elif tokens[i] in ['-', '+', '*', '/', '&', '|', '^', '<', '>', '%', '~']:
            op_stack.append((tokens[i], i))
        else:
            etc_stack.append((tokens[i], i))
    result = []
    end_flag = False
    p_save_index = []
    b_save_index = []
    open_index = 0
    open_p = None
    open_b = None



def parentheses_list(parenthese_lst, tokens):
    # parenthese_lst = []
    # result = []
    # token_len = len(tokens)
    # for i in range(token_len):
    #     if tokens[i] in ['Concat', 'Extract']:
    #         parenthese_lst.append((tokens[i] + '(', i))
    #     elif tokens[i] in [')']:
    #         parenthese_lst.append((tokens[i], i))
    result = []
    end_flag = False
    save_indexs = []
    open_index = 0
    open_parenthese = None
    for parenthese, index in parenthese_lst:
        if parenthese == ')' and save_indexs and not end_flag:
            pop_idx = save_indexs.pop()
            result.append(''.join(tokens[pop_idx:index]))
        elif open_parenthese is None:
            open_parenthese = parenthese
            open_index = index
            end_flag = True
        elif parenthese in ['Concat(', 'Extract('] and end_flag:
            save_indexs.append(open_index)
            open_parenthese = parenthese
            open_index = index
        elif parenthese == ')' and end_flag:
            end_flag = False
            open_parenthese = None
            result.append(''.join(tokens[open_index:index]))
    return result

def brackets_list(bracket_lst, tokens):
    # bracket_lst = []
    # token_len = len(tokens)
    # for i in range(token_len):
    #     if tokens[i] in ['[']:
    #        bracket_lst.append(('mem32' + tokens[i], i))
    #     elif tokens[i] in [']']:
    #        bracket_lst.append((tokens[i], i))
    # if cur_bracket == '[' -> True
    # But, meet ']' -> flag is False
    result = []
    end_flag = False
    save_indexs = []
    open_index = 0
    open_bracket = None
    for bracket, index in bracket_lst:
        if bracket == ']' and save_indexs and not end_flag:
            pop_idx = save_indexs.pop()
            result.append(''.join(tokens[pop_idx + 1:index]))
        elif open_bracket is None:
            open_bracket = bracket
            open_index = index
            end_flag = True
        elif bracket == 'mem32[' and end_flag:
            save_indexs.append(open_index)
            open_bracket = bracket
            open_index = index
        elif bracket == ']' and end_flag:
            end_flag = False
            open_bracket = None
            result.append(''.join(tokens[open_index + 1:index]))
    return result

def end_list(lst, start, end_char):
    lst_len = len(lst)
    for i in range(start, lst_len):
        if lst[i] == end_char:
            return i

def token2mem(token):
    # ex) mem32[80 + EBP] -> ExprMem(ExprOp('+', ExprInt(0x50, 32), ExprId('EBP', 32)))
    number = re.search(r'\d+', token).group()
    reg = re.search(r'[A-Z]+', token).group()
    op = re.search(r'[-+*/]', token).group()
    expr_op = ExprOp(op, ExprInt(int(number), 32), ExprId(reg, 32))
    return ExprMem(expr_op, 32)

def token2expr(token_lst):
    result_list = []
    for token in token_lst:
        # ex) mem32[80 + EBP] -> ExprMem(ExprOp('+', ExprInt(0x50, 32), ExprId('EBP', 32)))
        if 'mem32' in token:
            result_list.append(token2mem(token[6:-1]))
        # ExprInt
        elif token.isdigit():
            result_list.append(ExprInt(token, 32))
        # ExprId
        else:
            result_list.append(ExprId(token, 32))
    return result_list

def delete_square(expr):
    pattern = r'\([^()]+\)|\[[^\[\]]+\]'
    matches = re.findall(pattern, expr)
    result = expr
    for match in matches:
        result = result.replace(match, '')
    return result

def find_op(expr):
    result = delete_square(expr)
    op = re.findall(r'[-+*/]', result)
    print("find_op")
    print(op)
    return op

def find_etc(expr):
    pattern = r'\b(?!(?:mem32|Concat|Extract|\+|-|\*|/)\b)[A-Za-z0-9]+\b'
    result = delete_square(expr)
    etc = re.findall(pattern, result)
    print("find_etc")
    print(etc)
    return etc

expression = "1 + Concat(mem32[130+EBP],mem32[129+EBP],mem32[128+EBP],mem32[127+EBP])"
tokens = re.findall(r'\w+|\S', expression)
print(tokens)
expr_list = []
for token in tokens:
    if isinstance(token, int):
        expr_list.append(ExprInt(int(token), 32))
    elif token in ['EBP', ['ESP']]:
        expr_list.append(ExprId(token, 32))
    elif token in ['+', '-', '*', '/']:
        expr_list.append(token)
    elif token == 'Concat':
        expr_list.append("")



# df = pd.read_excel("../example/samples/handler_code.xlsx")
# handle = df.groupby(df.columns[0])
#
# for name, group in handle:
#     print(f"Group: {name}")
#     expression = group.iloc[1, 4]
#     print(expression)
#     # z3 Code Tokenizer
#     tokens = re.findall(r'\w+|\S', expression)
#     print(tokens)
    # print(tokens)
    # op_tokens = find_op(expression)
    # etc_tokens = find_etc(expression)
    # del_op = expression
    # for op in op_tokens:
    #     del_op = del_op.replace(op, ' ')
    # print(del_op)
    # # Concat or Extract the opcode behind parnethese -> () to extract
    # concat_extract_list = parentheses_list(tokens)
    # # Concat or Extract in mem32's split == concat_in_list
    # print(concat_extract_list)
    # concat_in_list = []
    # for element in concat_extract_list:
    #     concat_in_list.append(element.split(','))
    # print(concat_in_list)
    #
    # # mem32's split -> ExprId -> ExprMem == in_mem_list
    # new_concat_list = []
    # for lst in concat_in_list:
    #     new_concat_list.append(ExprCompose(*token2expr(lst)))
    #
    # # mem32 the memory behind square brackets -> [] to extract
    # mem_list = brackets_list(tokens)
    # new_mem_list = []
    # if mem_list:
    #     count = 0
    #     for mem in mem_list:
    #         if mem in concat_extract_list:
    #             continue
    #         elif 'Concat' in mem or 'Extract' in mem:
    #             new_mem_list.append(ExprMem(new_concat_list[count], 32))
    #             count += 1
    #         else:
    #             new_mem_list.append(token2mem(mem))
    # print(new_concat_list)
    # print('-' * 20)
    # print(new_mem_list)
    # print('=' * 30)

from miasm.expression.expression import *
from miasm.expression.parser import *
from miasm.expression.expression_helper import *
from miasm.expression.simplifications import *

class ConcatTransformer():
    # expr = None
    def __init__(self, expr):
        self.expr = expr
        self.args_dict = expr.args2expr
        self.expr_in_concat_list = self.concat_sliceto_slice_list()
        self.expr_in_concat_dict = self.concat_sliceto_slice_dict()

    def concat_sliceto_slice_list(self):
        '''
        입력받은 Expr 표현식에서 ExprCompose를 찾은 뒤
        merge_sliceto_slice 함수를 이용하여 ExprCompose를 구성하는 원소들을
        List에 저장하여 return 한다.
        Concat(== ExprCompose)가 위험한 Concat인지 확인하기 위한 List
        '''
        result_list = []
        for key, value in self.args_dict.items():
            if isinstance(value, ExprCompose):
                result_list.append(merge_sliceto_slice(value))
        return result_list

    def concat_sliceto_slice_dict(self):
        '''
        입력받은 Expr 표현식에서 ExprCompose를 찾은 뒤
        merge_sliceto_slice 함수를 이용하여 ExprCompose를 구성하는 원소들을
        Dictionary에 저장하여 return 한다.
        해당 ExprCompose에 대응되는 ExprMem으로 교체하기 위한 Dictionary
        '''
        result_dict = {}
        for key, value in self.args_dict.items():
            if isinstance(value, ExprCompose):
                result_dict[value] = merge_sliceto_slice(value)
        return result_dict

    def in_expr_EBP(self, lst):
        '''
        ExprMem의 ExprId가 EBP인지 확인한다.
        '''
        for expr in lst:
            if (isinstance(expr, ExprMem) and
                    expr.ptr.args[1].name == 'EBP'):
                return False
        return True

    def in_expr_ESP(self, lst):
        '''
        ExprMem의 ExprId가 ESP인지 확인한다.
        '''
        for expr in lst:
            if (isinstance(expr, ExprMem) and
                    expr.ptr.args[1].name == 'ESP'):
                return False
        return True

    def exprs_sub_result1(self, lst):
        '''
        4개의 ExprMem의 offset들의 차이가 1씩 차이가 나는지 확인하는 함수
        '''
        for i in range(3):
            if not lst[0].ptr.args[0].arg - lst[1].ptr.args[0].arg == 1:
                return False
        return True

    def is_4expr_in_concat(self, lst):
        '''
        Concat(ExprCompose)를 구성하고 있던 원소가 4개인지 확인.
        '''
        if len(lst) != 4:
            return False
        return True

    def is_unsafe_concat(self):
        '''
        위험한 Concat(ExprCompose)인지 확인하는 함수
        '''
        for expr_list in self.expr_in_concat_list:
            if ((self.in_expr_ESP(expr_list) or self.in_expr_EBP(expr_list)) and self.is_4expr_in_concat(expr_list)
                    and self.exprs_sub_result1(expr_list)):
                return True
        return False

    def replace_unsafe_concat_to_mem(self):
        '''
        unsafe Concat를 ExprMem으로 바꿔주는 함수
        '''
        target_expr = {}
        for concat, expr_in_concat in self.expr_in_concat_dict.items():
            target_expr[concat] = ExprMem(expr_in_concat[0].ptr, 128)
        after_replace_expr = self.expr.replace_expr(target_expr)
        return after_replace_expr

class ExtractTransformer():
    def __init__(self, end, start, mem32):
        assert end >= start
        self.end = end
        self.start = start
        self.mem32 = mem32

    def get_slice_expr_register(self, slice_expr):
        return slice_expr.arg.ptr.args[1]

    def get_slice_expr_offset(self, slice_expr):
        return slice_expr.arg.ptr.args[0]

    def make_extract_to_exprmem(self):
        extract = ExprSlice(self.mem32, self.start, self.end+1)
        register = self.get_slice_expr_register(extract)
        offset = self.get_slice_expr_offset(extract)
        return ExprMem(offset + register, self.end + 1 - self.start)

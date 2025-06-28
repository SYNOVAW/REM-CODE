# rem-code/engine/rem_transformer.py

from lark import Transformer, v_args

@v_args(inline=True)
class REMTransformer(Transformer):
    def __init__(self, sr_value=0.0):
        super().__init__()
        self.sr_value = sr_value
        self.env = {}

    def start(self, *statements):
        return list(statements)

    def assignment(self, name, value):
        self.env[name] = value
        return ('assign', str(name), value)

    def function_call(self, name, *args):
        return ('call', str(name), list(args))

    def args(self, *args):
        return list(args)

    def expr(self, value):
        return value

    def STRING(self, token):
        return str(token)[1:-1]

    def SIGNED_NUMBER(self, token):
        return float(token)

    def NAME(self, token):
        return str(token)

    def if_collapse(self, *args):
        # args = [op, threshold, if_block, collapse_block]
        # "else" のキーワードは literal 扱いなので飛ばして良い
        op, threshold, if_block, collapse_block = args
        return ('if_collapse', str(op), float(threshold), if_block, collapse_block)
   
    def statement_block(self, *statements):
        return list(statements)

    def COMPARATOR(self, token):
        return str(token)

    def COMMENT(self, token):
        return ('comment', str(token))

    # ✅ command: verb + (string_arg or condition)
    def command(self, verb, arg_or_condition):
        return ('call', str(verb), [arg_or_condition])

    def verb(self, token):
        return str(token)

    def string_arg(self, token):
        return str(token)[1:-1]

    def sr_condition(self, token):
        # 例: > 0.5 などの比較条件 → 文字列として評価
        return str(token)

    def phase_block(self, name, *stmts):
        return ('phase', str(name), list(stmts))

    def invoke_block(self, name, *stmts):
        return ('invoke', str(name), list(stmts))

    def statement(self, item):
        return item

    def assignment(self, name, value):
         return ('assign', str(name), value)

    def expr(self, value):
          return value

    def comparator(self, token):
          return str(token)

    def function_def(self, name, *statements):
           return ('function_def', str(name), list(statements))

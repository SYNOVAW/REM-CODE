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

    def if_collapse(self, op, threshold, if_block, collapse_block):
        return ('if_collapse', str(op), float(threshold), if_block, collapse_block)

    def statement_block(self, *statements):
        return list(statements)

    def comparator(self, token):
        return str(token)

    def COMMENT(self, token):
        return ('comment', str(token))


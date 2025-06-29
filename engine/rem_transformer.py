# rem-code/engine/rem_transformer.py

from lark import Transformer, v_args, Tree

@v_args(inline=True)
class REMTransformer(Transformer):
    def __init__(self, sr_value=0.0):
        super().__init__()
        self.sr_value = sr_value
        self.env = {}

    def start(self, *statements):
        print(f">>> Start with {len(statements)} statements")
        return list(statements)

    def statement(self, item):
        print(f">>> Processing statement: {item}")
        return item

    def function_def(self, name, body):
        print(f">>> Function_def called with name: {name}, body: {body}")
        return ('function', str(name), body)
    
    def function_body(self, *commands):
        print(f">>> Function_body with commands: {commands}")
        return list(commands)

    def command(self, verb, arg):
        print(f">>> Command: {verb} with arg: {arg}")
        return ('call', str(verb), [arg] if not isinstance(arg, list) else arg)

    def verb(self, token):
        return str(token)

    def string_arg(self, token):
        # 引用符を除去
        return str(token)[1:-1] if str(token).startswith('"') else str(token)

    def invoke_block(self, name, *stmts):
        print(f">>> Invoke block '{name}' with statements: {stmts}")
        return ('invoke', str(name), list(stmts))

    def phase_block(self, name, *stmts):
        print(f">>> Phase block '{name}' with statements: {stmts}")
        return ('phase', str(name), list(stmts))

    def collapse_sync_chain(self, comparator, number, collapse_block, elapse_list, sync_block):
        print(f">>> Collapse-sync chain: {comparator} {number}")
        return ('collapse_sync', str(comparator), float(number), collapse_block, sync_block)

    def elapse_list(self, *elapse_blocks):
        return list(elapse_blocks)

    def elapse_block(self, comparator, number, block):
        return ('elapse', str(comparator), float(number), block)

    def statement_block(self, *statements):
        return list(statements)

    def sr_condition(self, comparator, number):
        return f"{comparator} {number}"

    # Terminal handlers
    def NAME(self, token):
        return str(token)

    def NUMBER(self, token):
        return float(token)

    def ESCAPED_STRING(self, token):
        return str(token)[1:-1]  # 引用符を除去

    def LATIN_VERB(self, token):
        return str(token)

    def COMPARATOR(self, token):
        return str(token)
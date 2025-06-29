# rem-code/engine/rem_executor.py

from lark import Tree, Token

# ✅ 関数保存用のグローバルレジストリ
function_registry = {}

def execute(statements, env=None, sr_value=0.0):
    if env is None:
        env = {}

    output = []
    
    print(f">>> 🎯 execute() called with {len(statements)} statements:")
    for i, stmt in enumerate(statements):
        print(f"    [{i}] {stmt}")

    for stmt in statements:
        print(f">>> 🔄 Executing: {stmt} (type: {type(stmt)})")

        # ✅ Tuple処理（メイン）
        if isinstance(stmt, tuple):
            kind = stmt[0]
            print(f">>> Tuple kind: {kind}")

            if kind == 'function':
                # 関数定義: ('function', name, body)
                _, name, body = stmt
                env[name] = body
                function_registry[name] = body
                output.append(f"✅ Function '{name}' defined")
                print(f">>> Function '{name}' stored in env")

            elif kind == 'call':
                # コマンド実行: ('call', verb, args)
                _, name, args = stmt
                resolved_args = [env.get(arg, arg) for arg in args]
                print(f">>> Executing command: {name} with args: {resolved_args}")

                if name == "Acta":
                    message = str(resolved_args[0]) if resolved_args else "[No Acta arg]"
                    output.append(message)
                    print(f">>> Acta output: {message}")
                elif name == "Causa":
                    message = str(resolved_args[0]) if resolved_args else "[No Causa arg]"
                    output.append(message)
                    print(f">>> Causa output: {message}")
                else:
                    result = f"Function {name} called with args {resolved_args}"
                    output.append(result)
                    print(f">>> Generic call output: {result}")

            elif kind == 'invoke':
                # 関数呼び出し: ('invoke', name, body)
                _, name, body = stmt
                print(f">>> 🚀 Invoking function: {name}")
                
                # 登録された関数を探す
                if name in env:
                    print(f">>> Found function '{name}' in env: {env[name]}")
                    flat_body = flatten_statements(env[name])
                    print(f">>> Executing function body: {flat_body}")
                    invoke_output = execute(flat_body, env, sr_value)
                    output.append(f"🚀 Invoked '{name}':")
                    output.extend(invoke_output)
                    print(f">>> Invoke result: {invoke_output}")
                elif name in function_registry:
                    print(f">>> Found function '{name}' in registry: {function_registry[name]}")
                    flat_body = flatten_statements(function_registry[name])
                    print(f">>> Executing function body: {flat_body}")
                    invoke_output = execute(flat_body, env, sr_value)
                    output.append(f"🚀 Invoked '{name}':")
                    output.extend(invoke_output)
                    print(f">>> Invoke result: {invoke_output}")
                else:
                    error_msg = f"❌ Function '{name}' not found in env or registry"
                    print(f">>> Available functions in env: {list(env.keys())}")
                    print(f">>> Available functions in registry: {list(function_registry.keys())}")
                    output.append(error_msg)
                    print(error_msg)

                # 直接本文付きの場合（即時invoke）
                if body:
                    print(f">>> Executing immediate invoke body: {body}")
                    flat_body = flatten_statements(body)
                    invoke_output = execute(flat_body, env, sr_value)
                    output.extend(invoke_output)

            elif kind == 'phase':
                _, name, body = stmt
                output.append(f"🌐 Phase: {name}")
                flat = flatten_statements(body)
                output.extend(execute(flat, env, sr_value))

            elif kind == 'collapse_sync':
                _, op, threshold, collapse_block, sync_block = stmt
                condition = compare(sr_value, op, threshold)
                output.append(f"🌀 Collapse: SR {sr_value} {op} {threshold} → {'Sync' if condition else 'Collapse'} block")
                block = sync_block if condition else collapse_block
                output.extend(execute(block, env, sr_value))

            elif kind == 'collapse_chain':
                _, branches, sync_block = stmt
                matched = False
                for branch_type, op, threshold, block in branches:
                    if compare(sr_value, op, threshold):
                        output.append(f"↪ SR {sr_value} {op} {threshold} → {branch_type} block")
                        output.extend(execute(flatten_statements(block), env, sr_value))
                        matched = True
                        break
                if not matched:
                    output.append("↪ No collapse/elapse matched → Sync block")
                    output.extend(execute(flatten_statements(sync_block), env, sr_value))

            elif kind == 'assign':
                _, name, value = stmt
                env[name] = value
                output.append(f"{name} = {value}")

            elif kind == 'comment':
                _, comment_text = stmt
                output.append(f"# {comment_text}")

            else:
                print(f">>> Unknown tuple kind: {kind}")
                output.append(f"⚠️ Unknown command: {kind}")

        # ⚠️ Tree処理（レガシー対応、できれば避ける）
        elif isinstance(stmt, Tree):
            print(f">>> Warning: Processing Tree object: {stmt.data}")
            if stmt.data == 'function_def':
                func_name = stmt.children[0]
                body = [child for child in stmt.children[1:] 
                       if not (isinstance(child, Token) and child.type in ('LPAR', 'RPAR'))]
                env[func_name] = body
                function_registry[func_name] = body
                output.append(f"✅ Function '{func_name}' defined (from Tree)")
            else:
                output.append(f"⚠️ Unhandled Tree: {stmt.data}")

        else:
            print(f">>> Unknown statement type: {type(stmt)}")
            output.append(f"⚠️ Unknown statement: {stmt}")

    return output


def compare(sr, op, threshold):
    return {
        ">": sr > threshold,
        ">=": sr >= threshold,
        "<": sr < threshold,
        "<=": sr <= threshold,
        "==": sr == threshold,
        "!=": sr != threshold,
    }.get(op, False)


def execute_function(lines, sr_value=0.0):
    from parser.grammar_transformer import parse_lines
    statements = parse_lines(lines, sr_value)
    print(f">>> execute_function called with {len(statements)} statements")
    result = execute(statements, sr_value=sr_value)
    print(f">>> execute_function result: {result}")
    return result


def flatten_statements(stmts):
    flat = []
    for stmt in stmts:
        if isinstance(stmt, list):
            flat.extend(flatten_statements(stmt))
        else:
            flat.append(stmt)
    return flat
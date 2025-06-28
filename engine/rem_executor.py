# rem-code/engine/rem_executor.py

# ✅ 関数保存用のグローバルレジストリ
function_registry = {}

def execute(statements, env=None, sr_value=0.0):
    if env is None:
        env = {}

    output = []

    for stmt in statements:
        print(">>> Executing:", stmt)  # デバッグログ

        if isinstance(stmt, tuple):
            kind = stmt[0]

            if kind == 'assign':
                _, name, value = stmt
                env[name] = value
                output.append(f"{name} = {value}")

            elif kind == 'call':
                _, name, args = stmt
                resolved_args = [env.get(arg, arg) for arg in args]

                if name == "Acta":
                    output.append(str(resolved_args[0]) if resolved_args else "[No Acta arg]")
                elif name == "Causa":
                    output.append(str(resolved_args[0]) if resolved_args else "[No Causa arg]")
                else:
                    output.append(f"Function {name} called with args {resolved_args}")

            elif kind == 'if_collapse':
                _, op, threshold, if_block, collapse_block = stmt
                condition = compare(sr_value, op, threshold)
                chosen_block = if_block if condition else collapse_block
                output.append(f"↪ SR {sr_value} {op} {threshold} → {'if' if condition else 'collapse'} block")
                block_output = execute(chosen_block, env, sr_value)
                output.extend(block_output)

            elif kind == 'comment':
                _, comment_text = stmt
                output.append(f"# {comment_text}")

            elif kind == 'phase':
                _, name, body = stmt
                output.append(f"🌐 Phase: {name}")
                flat = flatten_statements(body)
                output.extend(execute(flat, env, sr_value))

            elif kind == 'invoke':
                _, name, body = stmt
                output.append(f"🚀 Invoke: {name}")

                # ✅ 定義済み関数を呼び出す
                if name in function_registry:
                    output.extend(execute(function_registry[name], env, sr_value))
                else:
                    output.append(f"⚠️ Undefined function '{name}'")

                # ✅ invokeブロックの追加命令も実行
                flat = flatten_statements(body)
                output.extend(execute(flat, env, sr_value))

            elif kind == 'function_def':
                _, name, *body = stmt
                function_registry[name] = body
                output.append(f"✅ Function '{name}' defined.")

    return output


def compare(sr, op, threshold):
    if op == ">=":
        return sr >= threshold
    elif op == "<=":
        return sr <= threshold
    elif op == ">":
        return sr > threshold
    elif op == "<":
        return sr < threshold
    elif op == "==":
        return sr == threshold
    elif op == "!=":
        return sr != threshold
    else:
        raise ValueError(f"Unknown comparator: {op}")


# 🔁 REM関数の統合実行
def execute_function(lines, sr_value=0.0):
    from parser.grammar_transformer import parse_lines
    statements = parse_lines(lines, sr_value)
    return execute(statements, sr_value=sr_value)


def flatten_statements(stmts):
    flat = []
    for stmt in stmts:
        if isinstance(stmt, list):
            flat.extend(flatten_statements(stmt))
        else:
            flat.append(stmt)
    return flat


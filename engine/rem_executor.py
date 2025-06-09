# rem-code/engine/rem_executor.py

def execute(statements, env=None, sr_value=0.0):
    if env is None:
        env = {}

    output = []
    for stmt in statements:
        if isinstance(stmt, tuple):
            if stmt[0] == 'assign':
                _, name, value = stmt
                env[name] = value
                output.append(f"{name} = {value}")

            elif stmt[0] == 'call':
                _, name, args = stmt
                resolved_args = [env.get(arg, arg) for arg in args]
                output.append(f"Function {name} called with args {resolved_args}")

            elif stmt[0] == 'if_collapse':
                _, op, threshold, if_block, collapse_block = stmt
                condition = compare(sr_value, op, threshold)
                chosen_block = if_block if condition else collapse_block
                output.append(f"↪ SR {sr_value} {op} {threshold} → {'if' if condition else 'collapse'} block")
                block_output = execute(chosen_block, env, sr_value)
                output.extend(block_output)

            elif stmt[0] == 'comment':
                output.append(f"# {stmt[1]}")

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

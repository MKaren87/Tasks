def flatten_list(lst):
    result = []
    stack = [lst]
    while stack:
        current = stack.pop()
        if isinstance(current, list):
            stack.extend(reversed(current))
        else:
            result.append(current)
    return result
nl = [1, 2, [3, [4, 5], 6]]
print(flatten_list(nl))  # Output: [1, 2, 3, 4, 5, 6]
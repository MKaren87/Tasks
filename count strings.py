def count_strings(*args):
    return sum(1 for arg in args if isinstance(arg, str))

print(count_strings("hello", 42, "world", [1, 2, 3], "Python"))



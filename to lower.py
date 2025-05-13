def to_lower_custom(s):
    return ''.join(chr(ord(c) + 32) if 'A' <= c <= 'Z' else c for c in s)

print(to_lower_custom("HELLO WORLD!"))


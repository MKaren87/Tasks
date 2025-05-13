def to_upper_custom(s):
    return ''.join(chr(ord(c) - 32) if 'a' <= c <= 'z' else c for c in s)

print(to_upper_custom("hello world!"))


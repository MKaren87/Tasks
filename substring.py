def substring(s, start, end):
    start, end = max(0, start), min(len(s), end)
    return s[start:end] if start < end else ""

print(substring("hello world!", 6, 12))

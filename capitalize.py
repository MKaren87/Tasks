def capitalize_words_ascii(s):
    return ' '.join(chr(ord(word[0]) - 32) + word[1:] if 'a' <= word[0] <= 'z' else word for word in s.split())

print(capitalize_words_ascii("hello world! python is awesome"))


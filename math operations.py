def math_operations(a, b):
    return {
        "Сумма": a + b,
        "Разность": a - b,
        "Произведение": a * b,
        "Частное": a / b if b != 0 else "Деление на ноль невозможно",
        "Целочисленное деление": a // b if b != 0 else "Деление на ноль невозможно",
        "Остаток от деления": a % b if b != 0 else "Деление на ноль невозможно",
        "Возведение в степень": a ** b
    }

result = math_operations(10, 3)
for operation, value in result.items():
    print(f"{operation}: {value}")


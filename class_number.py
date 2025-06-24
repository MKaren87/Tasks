class Number:
    def __init__(self, v):
        self.value = v
    def __str__(self):
        return f'Number({self.value})'
    def __add__(self, other):
        value = self.value + other.value
        return Number(value)
    def __sub__(self, other):
        value = self.value - other.value
        return Number(value)
    def __mul__(self, other):
        value = self.value * other.value
        return Number(value)
    def __truediv__(self, other):
        if other.value == 0:
            raise ValueError("Cannot divide by zero")
        value = self.value / other.value
        return Number(value)
n1 = Number(10)
n2 = Number(5)
print(n1 + n2) 
print(n1 - n2) 
print(n1 * n2)
print(n1 / n2)

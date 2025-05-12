def average(*args):
    numbers = [arg for arg in args if isinstance(arg, (int, float))]  
    return sum(numbers) / len(numbers) if numbers else None  

print(average(10, 20, 30))  
print(average(4, "Python", 8, 12))  
print(average())


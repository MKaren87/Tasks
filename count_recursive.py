def count_recursive(arr):
    if not arr:  
        return 0
    return 1 + count_recursive(arr[1:])  

numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(count_recursive(numbers))  


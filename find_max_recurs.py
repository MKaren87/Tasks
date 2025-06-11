def find_max_recursive(arr):
    if len(arr) == 1:  
        return arr[0]
    max_of_rest = find_max_recursive(arr[1:])  
    return arr[0] if arr[0] > max_of_rest else max_of_rest  

numbers = [3, 7, 2, 9, 5, 10, 6]
print(find_max_recursive(numbers))  


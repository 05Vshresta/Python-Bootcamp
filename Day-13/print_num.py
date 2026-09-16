def print_num(num):
    if num==0:
        return 
    print_num(num-1)
    print(num, end=" ")

print_num(10)
def multiplication_table(n, i=1):
    if i > 10:
        return 
    print(f"{n} * {i} = {n*i}")
    multiplication_table(n, i+1)
number = int(input("Enter a number: "))
multiplication_table(number)
def multiplication_table(n, i=1):
    if i > 10:
        return "Input should be less than or equal to 10"
    print(f"{n} * {i} = {n*i}")
    multiplication_table(n, i+1)
number = int(input("Enter a number: "))
multiplication_table(number)
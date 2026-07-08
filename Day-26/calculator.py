num1 = int(input("Enter the first number : "))
operator = input("Enter operator : ")
num2 = int(input("Enter the second number : "))

if operator == "+":
    print("Result = " ,num1 + num2)
elif operator == "-":
    print("Result = " ,num1 - num2)
elif operator == "*":
    print("Result = " ,num1 * num2)
elif operator == "/":
    if num2 != 0:
        print("Result = " ,num1 / num2)
    else:
        print("Error! cannot divide by zero")
else:
    print("Invalid operator!")
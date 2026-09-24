try:
    num=int(input("Enter a number: "))
    print("You entered:", num)
except ValueError:
    print("Invalid input! Please enter a valid number.")
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
else:
    print("No errors occurred. You entered a valid number.") #runs only if no errors occur
finally:
    print("Execution completed.") #always runs regardless of whether an exception occurred or not
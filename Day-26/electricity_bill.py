# Electricity Bill Using All Operators

# Input
customer = input("Enter Customer Name: ")
units = int(input("Enter Units Consumed: "))
rate = int(input("Enter Rate per Unit: "))

# Arithmetic Operators
bill = units * rate
gst = bill * 18 / 100
total_bill = bill + gst

print("\n----- Electricity Bill -----")
print("Customer:", customer)
print("Bill Amount:", bill)
print("GST:", gst)
print("Total Bill:", total_bill)

print("Floor Division:", bill // 100)
print("Remainder:", bill % 100)
print("Square of Units:", units ** 2)

# Assignment Operators
balance = total_bill
balance += 100      # Late fee
balance -= 50       # Discount
balance *= 1
balance /= 1

print("Final Payable Amount:", balance)

# Comparison Operators
print("Bill > 1000:", bill > 1000)
print("Bill < 1000:", bill < 1000)
print("Bill == 1000:", bill == 1000)
print("Bill != 1000:", bill != 1000)
print("Bill >= 1000:", bill >= 1000)
print("Bill <= 1000:", bill <= 1000)

# Logical Operators
subsidy = True
online_payment = True

print("Eligible for Extra Discount:", subsidy and online_payment)
print("Any Benefit:", subsidy or online_payment)
print("No Subsidy:", not subsidy)

# Membership Operators
services = ["Electricity", "Water", "Gas"]

print("Electricity" in services)
print("Internet" not in services)

# Identity Operators
bill1 = services
bill2 = ["Electricity", "Water", "Gas"]

print("bill1 is services:", bill1 is services)
print("bill1 is not bill2:", bill1 is not bill2)

# Bitwise Operators
read = 1
write = 2

print("AND (&):", read & write)
print("OR (|):", read | write)
print("XOR (^):", read ^ write)
print("Left Shift:", read << 1)
print("Right Shift:", write >> 1)
print("NOT (~):", ~read)
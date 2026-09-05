# ============================================================
# 🐍 DAY 2 — PYTHON OPERATORS
# ============================================================

print("🐍" + "=" * 45)
print("          PYTHON OPERATORS — DAY 2")
print("=" * 47)

# Taking input
num1 = float(input("🔢 Enter first number: "))
num2 = float(input("🔢 Enter second number: "))

print("\n" + "=" * 47)
print("          🧮 ARITHMETIC OPERATIONS")
print("=" * 47)

print(f"➕ Addition       : {num1 + num2}")
print(f"➖ Subtraction    : {num1 - num2}")
print(f"✖️ Multiplication : {num1 * num2}")

if num2 != 0:
    print(f"➗ Division       : {num1 / num2}")
    print(f"🔢 Floor Division : {num1 // num2}")
    print(f"📌 Remainder      : {num1 % num2}")
else:
    print("⚠️ Division by zero is not allowed.")

print(f"⚡ Power           : {num1 ** num2}")

print("\n" + "=" * 47)
print("          🔍 COMPARISON OPERATIONS")
print("=" * 47)

print(f"num1 == num2 : {num1 == num2}")
print(f"num1 != num2 : {num1 != num2}")
print(f"num1 > num2  : {num1 > num2}")
print(f"num1 < num2  : {num1 < num2}")
print(f"num1 >= num2 : {num1 >= num2}")
print(f"num1 <= num2 : {num1 <= num2}")

print("\n" + "=" * 47)
print("          🧠 LOGICAL OPERATIONS")
print("=" * 47)

print(f"Both positive : {num1 > 0 and num2 > 0}")
print(f"Any positive  : {num1 > 0 or num2 > 0}")
print(f"num1 is not 0 : {not num1 == 0}")

print("\n" + "=" * 47)
print("🚀 Day 2 Completed — Operators Practiced!")
print("💡 Learn → Practice → Solve")
print("=" * 47)
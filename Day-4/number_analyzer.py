print("="*45)
print("     Number Analyzer")
print("="*45)
n = int(input("How many numbers want to enter?: "))

total=0
largest=None
smallest=None
even_count=0
odd_count=0

for i in range(1,n+1):
  num = int(input(f"Enter number {i}: "))
  total += num
  if largest is None or num > largest:
    largest = num
  if smallest is None or num < smallest:
    smallest = num
  if num % 2 == 0:
    even_count += 1
  else:
    odd_count += 1
average = total / n

print("\n" + "=" *45)
print("       Result")
print("=" * 45)

print("Total numbers: ",n)
print("Sum          : ",total)
print("Average      : ",average)
print("Largest      : ",largest)
print("Smallest     : ",smallest)
print("Even Numbers : ",even_count)
print("Odd Numbers  : ",odd_count)
print("=" * 45)
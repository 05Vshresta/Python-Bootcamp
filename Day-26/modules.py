import random
import math

# Fruit Shop
fruits = ["Mango", "Apple", "Banana", "Grapes", "Guava"]

print("🍎 Welcome to Lucky Fruit Shop 🍎")

# Random fruit suggestion
fruit = random.choice(fruits)
print("Today's Recommended Fruit:", fruit)

# Shuffle display
random.shuffle(fruits)
print("Available Fruits:", fruits)

# Lucky Discount
discount = random.randint(5, 30)
print("Lucky Discount:", discount, "%")

# Bill Calculation
price = 256.75
discount_amount = (price * discount) / 100
final_bill = price - discount_amount

print("Original Price:", price)
print("Final Bill:", math.floor(final_bill))

# Bonus Reward Points
reward = math.sqrt(144)
print("Reward Points Earned:", reward)

print("Absolute Balance:", math.fabs(-125.50))
print("Value of Pi:", math.pi)
print("Power Bonus:", math.pow(2, 5))

print("Random Number:", random.random())
 
#import datetime
from datetime import datetime
now = datetime.now()
print("Current Date and Time:", now)

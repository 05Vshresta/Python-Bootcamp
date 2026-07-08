#Row pattern
for i in range(1):
    for j in range(5):
        print("*", end=" ")
print("\n=====================")

#Column pattern
for i in range(5):
    for j in range(1):
        print("*", end=" ")
    print()
print("\n=====================")

#Square pattern
for i in range(5):
    for j in range(5):
        print("*", end=" ")
    print()
print("\n=====================")

#triangle pattern
for i in range(1, 5 + 1):
    #print spaces before *
    for j in range(5 - i):
        print(" " ,end="")
    #print * in each row
    for k in range(i):
        print("*", end=" ")
    print()
print("\n=====================")

#Pyramid pattern
n = 5
#Upper boundary
for i in range(1,n+1):
    #print spaces
    for j in range(n-i):
        print(" ", end=" ")
    #print stars
    for k in range(1,2*i):
        print("*", end=" ")
    print()
#Lower boundary
for i in range(n-1,0,-1):
    #print spaces
    for j in range(n-i):
        print(" ",end=" ")
    #print stars
    for k in range(1,2*i):
        print("*",end=" ")
    print()
print("\n=====================")

#Continous pattern
num = 1
for i in range(1,6):
    for j in range(i):
        print(num, end=" ")
        num += 1
    print()
print("="*45)
print("          STUDENT GRADE & RESULT CHECKER")
print("="*45)

name = input("Enter Student Name: ")
marks = int(input("Enter Marks (0-100): "))

if marks < 0 or marks > 100:
    print("⚠️ Invalid marks entered. Please enter marks between 0 and 100.")    

else:
    if marks >= 90:
        grade = "A+"
        result = "Pass"
    elif marks >= 80:
        grade = "A"
        result = "Pass"
    elif marks >= 70:
        grade = "B"
        result = "Pass"
    elif marks >= 60:
        grade = "C"
        result = "Pass"
    elif marks >= 50:
        grade = "D"
        result = "Pass"
    else:
        grade = "F"
        result = "Fail"

    print("\n" + "="*45)
    print(f"Student Name: {name}")
    print(f"Marks       : {marks}")
    print(f"Grade       : {grade}")
    print(f"Result      : {result}")
    print("="*45)
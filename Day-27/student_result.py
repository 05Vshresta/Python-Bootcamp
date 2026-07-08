
def calculate_grade(marks):
    """
    Calculate and return grade based on marks.
    Returns: A, B, C or Fail
    """
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    else:
        return 'Fail'
def display_result(student_name, marks, grade):
    #Display the formatted student result.
    print("\n" + "=" *30)
    print(f" Student : {student_name}")
    print(f" Marks : {marks}")
    print(f" Grade : {grade}")
    print( "="*30 )
    
# Main program
student_name = input("Enter Student Name : ")
marks = int(input("Enter Marks (0-100) : "))

grade = calculate_grade(marks)
display_result(student_name, marks, grade)



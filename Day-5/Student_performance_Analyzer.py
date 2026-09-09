def calculate_total(marks):
    return sum(marks)


def calculate_average(marks):
    return sum(marks) / len(marks)


def calculate_percentage(marks):
    return (sum(marks) / (len(marks) * 100)) * 100


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C+"
    elif percentage >= 40:
        return "C"
    else:
        return "F"


def get_status(percentage):
    if percentage >= 75:
        return "Excellent Performance!"
    elif percentage >= 60:
        return "Good Performance!"
    elif percentage >= 40:
        return "Average Performance!"
    else:
        return "Needs Improvement!"


def show_result(name, marks):
    total = calculate_total(marks)
    average = calculate_average(marks)
    percentage = calculate_percentage(marks)
    grade = calculate_grade(percentage)
    status = get_status(percentage)

    print("\n========== STUDENT PERFORMANCE ==========")
    print("Student Name:", name)
    print("-----------------------------------------")
    print("Marks:", marks)
    print("Total Marks:", total)
    print("Average:", round(average, 2))
    print("Percentage:", round(percentage, 2), "%")
    print("Grade:", grade)
    print("Status:", status)
    print("=========================================")


# Main Program

name = input("Enter student name: ")

number_of_subjects = int(input("Enter number of subjects: "))

marks = []

for i in range(number_of_subjects):
    mark = float(input(f"Enter marks for Subject {i + 1}: "))

    if 0 <= mark <= 100:
        marks.append(mark)
    else:
        print("Invalid marks! Enter marks between 0 and 100.")
        break

if len(marks) == number_of_subjects:
    show_result(name, marks)
else:
    print("Unable to generate result.")
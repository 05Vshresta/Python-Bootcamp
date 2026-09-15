def employee(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

id =int(input("Enter Employee ID: "))
name = input("Enter Employee Name: ")   
department = input("Enter Employee Department: ")
salary = float(input("Enter Employee Salary: "))

employee(id=id, name=name, department=department, salary=salary)
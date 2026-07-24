import csv
#open a CSV file in write mode
with open('students.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['Id', 'Name', 'Course'])
    writer.writerow(['1', 'Srijayalaxmi', 'AIML'])
    writer.writerow(['2', 'Shloka', 'CSE'])
    writer.writerow(['3', 'Kalasri', 'AIDS'])

    print("CSV file created successfully.")
    print("================================")

import csv
#open the CSV file in read mode
with open('students.csv', mode='r') as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)

    print("Data read from CSV file successfully.")
    print("================================")
    
import csv
#open the CSV file in append mode
with open('students.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['4', 'Swaroopa', 'EEE'])
    writer.writerow(['5', 'Meenakshi', 'ECE'])

    print("Data append to CSV file successfully.")
    print("================================")

import csv
#open the CSV file in read mode
with open('students.csv', mode='r') as file:

    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
       print(f"Id: {row[0]}, Name: {row[1]}, Course: {row[2]}")

    print("================================")
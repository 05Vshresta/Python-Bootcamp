#LIST OF PLACES TO VISIT
places = []
print("Enter 3 places you want to visit")
place1 = input("Place 1: ")
place2 = input("Place 2: ")
place3 = input("Place 3: ")
places.append(place1)
places.append(place2)
places.append(place3)
print("\nPlaces to visit:")
print(places)

#Add another place if the user wants to visit more places
more_place = input("Do you want to add more places? (yes/no): ")

if more_place.lower() == "yes":
   place4 = input("Enter Another place: ")
   places.append(place4)

#Tuple fixed travelled dates

start_date = input("Enter the start date of your travel (YYYY-MM-DD): ")
end_date = input("Enter the end date of your travel (YYYY-MM-DD): ")

travel_dates = (start_date, end_date)
print("\nTravel Dates:")
print("Start:",travel_dates[0])
print("END:",travel_dates[1])

#SET OF UNIQUE ACTIVITIES

activities = set()
print("\nEnter unique activities you want to do during your travel:")
activity1 = input("Activity 1: ")
activity2 = input("Activity 2: ")
activity3 = input("Activity 3: ")
activities.add(activity1)
activities.add(activity2)
activities.add(activity3)

print("\nUnique Activities:")
for activity in activities:
    print(activity)

#Add another activity if the user wants to do more activities
more_activity = input("Do you want to add more activities? (yes/no): ") 
if more_activity.lower() == "yes":
    activity4 = input("Enter Another activity: ")
    activities.add(activity4)

#Dictionary of travel details
name = input("Enter your name: ")
destination = input("Enter your travel destination: ")
budget = float(input("Enter your budget for the travel: "))
transportation = input("Enter your mode of transportation: ")

travel_details = {
    "Name": name,
    "Destination": destination,
    "Budget": budget,
    "Transportation": transportation
}
#Display the travel details
print("\n===== FINAL TRAVEL PLAN ======")

print("\nPlaces to visit:",places)

print("\nTravel Dates:")
print("Start:",travel_dates[0])
print("End:",travel_dates[1])
print("\nActivities:", activities)
print("\nTraveller Information:")

print("Name:",travel_details["Name"])
print("Destination:",travel_details["Destination"])
print("Budget:",travel_details["Budget"])
print("Transportation:",travel_details["Transportation"])
print("\n=====================================")

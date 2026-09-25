#parent class
class Vehicle:
    def __init__(self,name):#constructor
        self.name = name 
    def start(self):       
        print(f"{self.name} is starting.")
    def stop(self):
        print(f"{self.name} is stopped.")
#child class
class Car(Vehicle):
    def drive(self):
        print(f"{self.name} is driving on the road.")

my_car = Car("Toyota") #object of the child class
my_car.start()         # calling the start method
my_car.drive()         # calling the drive method
my_car.stop()          # calling the stop method
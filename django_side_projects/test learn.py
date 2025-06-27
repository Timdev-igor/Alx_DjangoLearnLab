class Vehicle:
    def __init__(self, category, means, price):
        self.category = category
        self.means = means
        self.price = price

    def increment_price(self, price):
        if price > 0:
            self.price += price
            return f"The new price is: ${self.price}"
        else:
            return "Price must be positive."
    @classmethod
    def count_vehicles(cls):
              # Class method to return the current count of dogs
            print(f"Total number of vehicles owned: {cls.count_vehicles}")
      

class Car(Vehicle): 
    def __init__(self, category, means, brand, price):
        super().__init__(category, means, price)
        self.brand = brand

class Plane(Car):
    def __init__(self, category, means, brand, price, airline, capacity):
        super().__init__(category, means, brand, price)
        self.airline = airline
        self.capacity = capacity

class Boat(Car):
    def __init__(self, category, means, brand, price):
        super().__init__(category, means, brand, price)

    

# Example usage
my_car = Car("Sedan", "Land", "Toyota", 20000)
print(f"Original car price: ${my_car.price}")
print(my_car.increment_price(1500))  # Increase price by 1500
my_boat = Boat("reeve", "water", " orefu", 2005666)
print(f"Original boat price: ${my_boat.price}")
print(my_boat.increment_price(1500))  # Increase price by 1500
print(Vehicle.count_vehicles())  
   
  
            


            
           


          
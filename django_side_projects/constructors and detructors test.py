class Person:
    def __init__(self, name):
        self.name = name
        print(f"Person object with name '{self.name}' is created.")

    def __del__(self):
        print(f"Person object with name '{self.name}' is destroyed.")

# Create an instance of Person
person1 = Person("Alice")

# Delete the instance to invoke the destructor
del person1

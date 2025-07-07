class Manager:
    def __init__(self, max_employees=3):  
        self.team = []
        self.max_employees = max_employees

    def hire(self, employee):
        if employee in self.team:
            print(f"{employee.name} is already hired!")
        elif len(self.team) >= self.max_employees:
            print(f"Cannot hire {employee.name}: team is full ({self.max_employees} members).")
        else:
            self.team.append(employee)
            print(f"{employee.name} has been hired.")

    def fire(self, employee):
        if employee in self.team:
            self.team.remove(employee)
            print(f"{employee.name} has been fired.")
        else:
            print(f"{employee.name} is not on the team.")

class Employee(Manager):
    def __init__(self, position, max_employees=3):
        super().__init__(max_employees)
        self.position = position

class Human(Employee):
    def __init__(self, name, age, position, max_employees=3):
        super().__init__(position, max_employees)
        self.name = name
        self.age = age

    def __repr__(self):
        return f"{self.name} ({self.position}, {self.age} y/o)"

manager = Manager(max_employees=2)

karen = Human("Karen", 30, "Developer")
anna = Human("Anna", 27, "Designer")
john = Human("John", 35, "Tester")

manager.hire(karen)  
manager.hire(anna)   
manager.hire(john)   

manager.fire(karen)  
manager.hire(john)   


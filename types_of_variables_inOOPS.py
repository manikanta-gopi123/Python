class car:
    wheels=4 #static variables
    def __init__(self):
        self.color='red'#instance variables
        self.width=3.4
c=car()
print(c.wheels)
print(c.color)
print(c.width)
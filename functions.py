def add():
    a=int(input(print("Enter 1st value")))
    b=int(input(print("Enter 2nd value")))
    c=a+b
    print(c)
add()


def sub(a,b):
    #a=int(input(print("Enter 1st value")))
    #b=int(input(print("Enter 2nd value")))
    c=a-b
    print(c)
sub(a=int(input(print("Enter 1st value"))),b=int(input(print("Enter 2nd value"))))



#Function with No Arguments
def greet():
    print("Hello")
greet()
#Function with Arguments
def greet(name):
    print("Hello",name)
greet("Gopi")

#Keyword Argument Functions
def sub(a,b):
    c=a-b
    print(c)
sub(a=int(input(print("Enter 1st value"))),b=int(input(print("Enter 2nd value"))))
#Keyword variable arguments
def info(**data):
    print(data)

info(name="Gopi", age=24)

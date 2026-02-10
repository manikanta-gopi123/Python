from exceptionhandling import*
try:
    num1=int(input("Enter a number"))
    num2=int(input("Enter a number"))
    print(num1/num2)
except ZeroDivisionError as e:
    print("Can not divide value by Zero",e)
except ValueError as e:
    print("Please enter valid input",e)
except Exception as e:
    print("Something went wrong")
finally:
    print("I am from Finally Block")
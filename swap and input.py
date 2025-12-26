# swapping for two variables using third variable
a=10
b=20
temp=a
a=b
b=temp
print('a=',a)
print('b=',b)
# without using third variable
x=25
y=30
x=x+y#now x=55
y=x-y# now y=25
x=x-y# now x=30
print('x=', x)
print('y=', y)

# Taking input from the user

# by default the user input will take as  a string
name=input("enter a name")
print('name = ', name)
char=int(input("Enter the index value of a character in which you want to extract from the string"))

print('particular character in a sting',name[char])
# if you need to convert by default input into a number or floating value you need to use functions
number1 =int(input('Enter a number'))
print(int(number1))
print(float(number1))

# Suppose if user want to know the output of a particular expression ex:2+5*4 then if the enter in the same format it will treat it as a string
# in order to avoid that we have an function called eval

# Eval
expression=eval(input("Enter an expression"))
print('output is :', expression)
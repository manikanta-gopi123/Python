num=int(input("Enter a number"))
if(num>=0 and num<=10):
    print("Number")
    if(num%2==0):
        print("Even")
elif(num==-1):
    print("Negative Number")
else:
    print("Number is greater than 10")

#While loop
i=0
while i<=num:
    print("whileloop executed",i,"time")
    i=i+1
# For Loop
size = int(input("Enter size of the list: "))
my_list = []   # create empty list
for j in range(size):
    value = input("Enter value: ")
    my_list.append(value)
print(my_list)
for k in my_list:
    print(k)
        
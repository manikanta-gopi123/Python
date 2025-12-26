num=int(input("Enter a number"))
for i in range(2,num):
    if num % i != 0:
        print("Prime Number")
        break
else:
        print("Not Prime")
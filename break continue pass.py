# Break Statement
for i in range(1,101):
    print(i)
    if(i % 5==0):
        break
# Continue Statement
print("Continue Statement")
for i in range(1,101):
    if(i % 5!=0):
        print(i)
        continue
def func():
    pass
print("After the Function")
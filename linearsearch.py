size=int(input("Enter size of the list"))
list=[]
for i in range(0,size):
    elements=int(input("Enter elements into the list"))
    list.append(elements)
num=int(input("Enter a number to search"))
def search(list,num):
    for j in range(0,len(list)):
        if list[j] == num:
            print("Found")
            break
    else:
        print("Not Found")
search(list,num)
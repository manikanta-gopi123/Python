from array import *
arr=array('i',[1,2,3,4])
print(arr)
j=0
print("While For loop")
while(j<len(arr)):
    print(arr[j])
    j=j+1
    
print("Using For loop")
for k in range(0,len(arr)):
    print(arr[k])
print("Reverse of an array",arr.reverse)
print("Min Vlaue is",min(arr))
print("Max Vlaue is",max(arr))
print(arr.append(5))
print(arr)
arr1=array('i',[25,30,9,3,48])
arr2=arr1
print(arr1)
#arr2=arr1.copy()
print(arr2)
print(id(arr1))
print(id(arr2))
print("Creating Array Using Dynamic Input")


size=int(input("Enter size of the array"))
a=array('i',[])
for i in range(0,int(size)):
    values=int(input("Enter values in to array"))
    a.append(values)
print("Values entered in Dynamic Array is")
for z in range(0,len(a)):
    print(a[z])
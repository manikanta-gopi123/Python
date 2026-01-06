size = int(input("Enter size of the list: "))
arr = []
for i in range(size):
    elements = int(input("Enter elements into the list: "))
    arr.append(elements)
num = int(input("Enter a number to search: "))
def search(arr, num):
    lower_boundary = 0
    upper_boundary = len(arr) - 1
    while lower_boundary <= upper_boundary:
        mid = (lower_boundary + upper_boundary) // 2
        if arr[mid] == num:
            print("Found")
            return   
        elif num < arr[mid]:
            upper_boundary = mid - 1
        else:
            lower_boundary = mid + 1
    print("Not Found")
search(arr, num)

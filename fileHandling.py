#To wtite content into the file
file1=open('file1.txt','w')
content=input("Enter content to your file")
file1.write(content)
print("You have been successfully save your content into the file")

#To Read the content from the File
file2=open("file2.txt",'r')
print("The Content in your file is")
print(file2.read())

#To append content into the existing file

file3=open("file2.txt",'a')
new_content=input("Enter content to append the existing file")
file3.write(new_content)
print("The File has been now updated.")

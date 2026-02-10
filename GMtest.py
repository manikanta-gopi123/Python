data=[{"Brand":"APT Services","MobileNumber":"916303768348","Name":"~gopi"},
      {"Brand":"APT Services","MobileNumber":"916303768348","Name":"~gopi"}
      ,{"Brand":"APT Services","MobileNumber":"916303768348","Name":"~gopi"},
      {"Brand":"APT Services","MobileNumber":"917780473899","Name":"~gopi"},
      {"Brand":"APT Services","MobileNumber":"917780473899","Name":"~gopi"}]
num=input("Enter a number")
c=0
for i in data:
    mob=i['MobileNumber']
    if(num==mob):
     c=c+1
if c==1:
    print("Hey there! 👋 Thanks for reaching out to us. While this channel is automated, we've got you covered! Want to connect with our team right now? ")
elif c==2:
    print("We appreciate your patience! Our team will respond shortly. In the meantime, for faster support you can: ")
elif (c>=3):
    print("Thank you for your continued interest in [Brand Name]. For the quickest response, we recommend: ")

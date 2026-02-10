data=[{"EmiratedID":"123456","MobileNumber":"916303768348","Doctor":"~gopi"}]
num=input("Enter a number")
c=0
for i in data:
    if(num==i['EmiratedID']):

        print("Mobile",i['MobileNumber'])
        print("Doctor",i['Doctor'])
        print("EmiratedID",i['EmiratedID'])
    else:
        print("Emirates Id not Found")
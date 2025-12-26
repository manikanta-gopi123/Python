class A:
    @staticmethod
    def get_classA():
        print("Getting the data from Class A")
class B(A):
    @staticmethod
    def get_classB():
        print("Getting the data from Class B")
class C(B):
    @staticmethod
    def get_classC():
        print("Getting the data from Class C")

c=C()
c.get_classB()
c.get_classC()
c.get_classA()

class Calc:
    @staticmethod
    def avg():
        n = int(input("Enter count: "))
        a = []
        for i in range(n):
            nums = int(input("Enter value: "))
            a.append(nums)
        average = sum(a) / len(a)
        print("Values:", a)
        print("Average:", average)


# Call static method
Calc.avg()

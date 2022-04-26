
class A(object):
    def __init__(self):
        self.a = 1
    
    def func(self):
        print(self.a)

class B(object):
    def __init__(self,A:A):
        self.a = 2
        self.A = A

    def func1(self):
        A.func()

object1 = A()
object2 = B(object1)

object1.func()
object2.func1()
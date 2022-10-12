class A(object):
    a = [1, 2]

    def get_a(self):
        return self.a

b = A()
a = b.get_a()

b.a.remove(1)
print(b.a)
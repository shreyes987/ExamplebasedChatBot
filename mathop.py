from math import sqrt; from itertools import count, islice
import math,random

class mathop:
    def square(self,a) :
        return a * a

    def factorial(self,a) :
        if a == 0 :
            return a + 1
        if a==1 :
            return a
        else :
             return a*self.factorial(a-1)

    def evenodd(self,a):
        if a % 2 ==0 :
            return "even"
        else:
            return "odd"

    def addition(self,a,b):
        return a + b

    def substraction(self,a,b):
        return a - b

    def multiplication(self,a,b):
        return a * b

    def prime(self,n):
        if n < 2: return "number is not a prime number"
        for number in islice(count(2), int(sqrt(n)-1)):
            if not n%number:
                return "number is not a prime number"
        return "number is a prime number"

    def inttoBinary(self,n):
        return ''.join(str(1 & int(n) >> i) for i in range(5)[::-1])


    def binarytoint(self,b): # string input needed
        return int(str(b), 2)

    def hextoint(self,b): # string input needed
        return int(str(b), 16)

    def octoint(self,b): # string input needed
        return int(str(b), 8)

    def inttohex(self,b):
        return  '0x{:02x}'.format(b)

    def inttooct(self,decimal):
        return oct(decimal)


    def lcm(self,x, y):
            if x > y:
                greater = x
            else:
                greater = y
            while (True):
                if ((greater % x == 0) and (greater % y == 0)):
                    lcm = greater
                    break
                greater += 1

            return lcm

    def negativedetector(self,a):
        if a < 0 :
            return "this is a negative number"
        else:
            return "this is a positive number"
    def kilotomiles(self,a) :
        con = 0.621371
        return a * con

    def milestokilo(self,a) :
        conf = 1.609
        return a * conf

    def metertocentimeter(self,a):
        return a * 100

    def centimetertometer(self,a):
        return a / 100

    def reverse(self,a):
        Reverse = 0
        while (a > 0):
            Reminder = a % 10
            Reverse = (Reverse * 10) + Reminder
            a = a // 10
        return Reverse

    def metertoinch(self,a):
        return a * 39.3701

    def metertofoot(self,a):
        return a * 3.28084

    def inchtometer(s,a):
        return a / 39.3701

    def foottometer(s,a):
        return a / 3.28084

    def log(s,a):
        return math.log10(a)

    def strong(s,inp):
        sum = 0
        if inp > 0:
            for i in str(inp):
                fact = 1
                if int(i) != 0:
                    for j in range(1, int(i) + 1):
                        fact = fact * j
                sum = sum + fact
            if sum == inp:
                return "Given number is strong number"
            else:
                return "Given number is not strong number"
        else:
            return "Given number is not strong number"

    def armstrong(s,num):
        sum = 0
        temp = num
        while temp > 0:
            digit = temp % 10
            sum += digit ** 3
            temp //= 10
        if num == sum:
            return "number is an Armstrong number"
        else:
            return "number is not an Armstrong number"

    def rdm(s,a, b):
        return (random.randint(a, b))

    def count1(s,n):
        if n > 0:
            digits = int(math.log10(n)) + 1
        elif n == 0:
            digits = 1
        else:
            digits = int(math.log10(-n)) + 2
        return digits

    def computeHCF(s,x, y):
        if x > y:
            smaller = y
        else:
            smaller = x
        for i in range(1, smaller + 1):
            if ((x % i == 0) and (y % i == 0)):
                hcf = i

        return hcf

    def areaofcir(s,a):
        return 3.141 * a * a

    def areaofsqu(s,a):
        return a * a

    def areaofrec(s,a, b):
        return a * b

    def equilateral(s,a):
        return (1.73205080757 / 4) * a * a

    def cylinder(s,r, h):
        return (2 * 3.141 * r * h) + (2 * 3.141 * r * r)

    def hexagon(s,a):
        return (3 * 1.73205080757 / 2) * a * a

    def kite(s,a, b):
        return (a * b) / 2

    def rombus(s,a, b):
        return (a * b) / 2

    def simpleint(s,p, n, r):
        return (p * n * r) / 100

    def avg(s,a, b):
        return (a + b) / 2

    def mean1(s,a, b):
        return (a + b) / 2

    def harmonic(s,a, b):
        return (2 / ((1 / a) + (1 / b)))

    def pm(s,lower, upper):
        a = []
        for num in range(lower, upper + 1):
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        break
                else:
                    a.append(str(num))
        return ",".join(a)

    def pn(s,num):
        rev_num = math.reversed(num)
        if list(num) == list(rev_num):
            return "Palindrome number"
        else:
            return "Not Palindrome number"

    def centitokilo(s,a):
        return a / 1000

    def sphere1(s,a):
        return (4 / 3) * 3.14 * a * a * a

    def cube(s,a):
        return (a*a*a)
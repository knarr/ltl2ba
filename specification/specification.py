#file: specification.py
import math

#Make a vector valued RF from a list of scalar valued RFs
class combineReward:
    def __init__(self, *rfs):
        self.rfs = rfs
    def __call__(self, st):
        return tuple(rf(st) for rf in self.rfs)
    def __len__(self):
        return len(self.rfs)

class Specification:
    truncate = False
    def __init__(self):
        pass
    #Evaluate a vector to produce a value in the ordering
    def __call__(self,vec):
        pass

    #Sugaring
    def __neg__(self):
        return Negate(self)
    def __add__(self, other):
        return Add(self, other)
    def __sub__(self, other):
        return Add(self, Negate(other))
    def __mul__(self, other):
        return Mult(self, other)
    def __gt__(self, other):
        return Gt(self, other)
    def __ge__(self, other):
        return Gte(self, other)
    def __lt__(self, other):
        return Gt(other, self)
    def __le__(self, other):
        return Gte(other, self)
    def __or__(self, other):
        return Add(Gte(other,self), Gte(self, other))

class Trunc(Specification):
    #Truncate the results before we calculate the policy
    def __init__(self, spec):
        self.spec = spec
        self.truncate = True
    def __call__(self, vec):
        return self.spec(vec)

class Lex(Specification):
    #Impose lexicographic ordering on a bunch of specs
    def __init__(self, *specs):
        self.specs = specs
    def __call__(self, vec):
        return tuple(spec(vec) for spec in self.specs)

class ID(Specification):
    #Reference the kth identifier
    def __init__(self, k):
        self.k = k
    def __call__(self, vec):
        return vec[self.k]

class Num(Specification):
    #Constant
    def __init__(self, n):
        self.n = n
    def __call__(self, vec):
        return self.n

class Negate(Specification):
    #Negate the value
    def __init__(self, spec):
        self.spec = spec
    def __call__(self, vec):
        return -self.spec(vec)

class Binop(Specification):
    #Binary operation on specifications
    def __init__(self, left, right):
        if isinstance(left, (int, long, float)): #More sugar to allow numbers to be used
            left = Num(left)
        if isinstance(right, (int, long, float)):
            right = Num(right)
        self.left = left
        self.right = right

class Add(Binop):
    #Add two specifications
    def __call__(self, vec):
        return self.left(vec) + self.right(vec)

class Mult(Binop):
    #Multiply two specifications
    def __call__(self, vec):
        return self.left(vec) * self.right(vec)

class Gte(Binop):
    #Greater than or equal to specification
    def __call__(self, vec):
        if self.left(vec) >= self.right(vec):
            return 0
        else:
            lw = self.left(vec)
            rw = self.right(vec)
            return -abs(lw - rw)/math.sqrt(2) #distance to lw > rw

class Gt(Binop):
    #Greater than
    def __call__(self, vec):
        if self.left(vec) > self.right(vec):
            return 0
        else:
            lw = self.left(vec)
            rw = self.right(vec)
            return -abs(lw - rw)/math.sqrt(2) - .1
            

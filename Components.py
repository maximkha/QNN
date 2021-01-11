class Component:
    def eval(self) -> bool:
        raise NotImplementedError("eval was not implemented")

    def simplify(self) -> object:
        raise NotImplementedError("simplify was not implemented")

    #make sure to call simplify on both arguments!
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Not):
            return isinstance(type(self), Not) and (o.A == self.A)
        elif isinstance(o, type(self)):
            return (o.A == self.A and o.B == self.B) or (o.B == self.A and o.A == self.B)
        else:
            return False

    def qcompat(self) -> object:
        raise NotImplementedError("qcompat was not implemented")

class Variable(Component):
    def __init__(self, name, val = None) -> None:
        self.val = val
        self.name = name
   
    def __str__(self) -> str:
        if self.val != None:
            return str(self.val)
        return self.name

    def define(self, val):
        self.val = val

    def eval(self):
        if self.val == None:
            raise ValueError("Tried to eval undefined variable!")
        return self.val

    def simplify(self) -> object:
        if self.val != None:
            return self.val
        return self

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Variable):
            return self.name == o.name
        else: 
            return False

    def qcompat(self) -> object:
        return self

class And(Component):
    def __init__(self, A:Component, B:Component) -> None:
        self.A = A
        self.B = B
    
    def __str__(self) -> str:
        return "And(" + str(self.A) + "," + str(self.B) + ")"
    
    def eval(self) -> bool:
        return self.A.eval() and self.B.eval()

    def simplify(self) -> object:
        simplifyA = self.A.simplify()
        simplifyB = self.B.simplify()

        if simplifyA == False or simplifyB == False:
            return False
        elif simplifyA == True:
            return simplifyB
        elif simplifyB == True:
            return simplifyA
        elif simplifyA == simplifyB: 
            return True
        elif simplifyA == Not(simplifyB).simplify(): 
            return False
        elif simplifyB == Not(simplifyA).simplify(): 
            return False
        else:
            return And(simplifyA, simplifyB)

    def qcompat(self) -> object:
        return And(self.A.qcompat(), self.B.qcompat())

class Or(Component):
    def __init__(self, A:Component, B:Component) -> None:
        self.A = A
        self.B = B
    
    def __str__(self) -> str:
        return "Or(" + str(self.A) + "," + str(self.B) + ")"
    
    def eval(self) -> bool:
        return self.A.eval() or self.B.eval()

    def simplify(self) -> object:
        simplifyA = self.A.simplify()
        simplifyB = self.B.simplify()

        if simplifyA == True or simplifyB == True:
            return True
        elif simplifyA == False:
            return simplifyB
        elif simplifyB == False:
            return simplifyA
        elif simplifyA == simplifyB: 
            return True
        elif simplifyA == Not(simplifyB).simplify(): 
            return True
        elif simplifyB == Not(simplifyA).simplify(): 
            return True
        else:
            return Or(simplifyA, simplifyB)

    def qcompat(self) -> object:
        return Not(And(Not(self.A.qcompat()), Not(self.B.qcompat())))

class Not(Component):
    def __init__(self, A:Component) -> None:
        self.A = A
    
    def __str__(self) -> str:
        return "Not(" + str(self.A) + ")"
    
    def eval(self) -> bool:
        return not self.A.eval()

    def simplify(self) -> object:
        simplifyA = self.A.simplify()
        if isinstance(simplifyA, Not):
            return simplifyA.A.simplify()
        elif simplifyA == True or simplifyA == False:
            return not simplifyA
        else:
            return Not(simplifyA)

    def qcompat(self) -> object:
        return Not(self.A.qcompat())

class Xor(Component):
    def __init__(self, A:Component, B:Component) -> None:
        self.A = A
        self.B = B
    
    def __str__(self) -> str:
        return "Xor(" + str(self.A) + "," + str(self.B) + ")"
    
    def eval(self) -> bool:
        return self.A.eval() ^ self.B.eval()

    def simplify(self) -> object:
        simplifyA = self.A.simplify()
        simplifyB = self.B.simplify()

        if simplifyA == True:
            return Not(simplifyB).simplify()
        elif simplifyB == True:
            return Not(simplifyA).simplify()
        elif simplifyA == False:
            return simplifyB
        elif simplifyB == False:
            return simplifyA
        elif simplifyA == simplifyB: 
            return False
        elif simplifyA == Not(simplifyB).simplify(): 
            return True
        elif simplifyB == Not(simplifyA).simplify(): 
            return True
        else:
            return Xor(simplifyA, simplifyB)
        
    def qcompat(self) -> object:
        return Xor(self.A.qcompat(), self.B.qcompat())

class PassThrough(Component):
    def __init__(self, A:Component) -> None:
        self.A = A
    
    def __str__(self) -> str:
        return "Pass(" + str(self.A) + ")"
    
    def eval(self) -> bool:
        return self.A.eval()

    def simplify(self) -> object:
        return self.A.simplify()
    
    def qcompat(self) -> object:
        return self.A.qcompat()

def Reg(name, nbit, v=None):
    bitVars = []
    for i in range(nbit):
        bitVars.append(Variable(name + str(i)))
    return bitVars

#cnot is actually xor
#We can use not as well
#def ToCNOT(gate):
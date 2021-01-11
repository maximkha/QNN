from Components import And, Xor, Not, Or

def HalfAdder(A, B):
    #sum, carry
    return (Xor(A, B), And(A, B))

def FullAdder(A, B, C):
    #sum, carry
    aXorb = Xor(A, B)
    tsum = Xor(aXorb, C)
    cout = Or(And(aXorb, C), And(A, B))
    return (tsum, cout)

def NBitAdder(Abitvars, Bbitvars, nbit=None):
    if nbit == None:
        nbit = len(Abitvars)
    if len(Abitvars) != nbit or len(Bbitvars) != nbit:
        raise ValueError("Abitvars and Bbitvars should contain nbit number of variables")
    if nbit < 1:
        raise Exception("Nbit should be > 1")

    sumBits = []
    carryBit = None

    halfSum, halfCarry = HalfAdder(Abitvars[0], Bbitvars[0])
    sumBits.append(halfSum)
    carryBit = halfCarry

    for i in range(nbit - 1):
        fullSum, fullCarry = FullAdder(Abitvars[i + 1], Bbitvars[i + 1], carryBit)
        carryBit = fullCarry
        sumBits.append(fullSum)
    
    return (sumBits, carryBit)
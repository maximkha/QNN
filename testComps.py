from Components import *
from Circuits import FullAdder, NBitAdder

print(Or(Variable("a"), Variable("b", False)).simplify())
print(FullAdder(Variable("a"), Variable("b"), Variable("c", True))[0].simplify())
print([str(x.simplify()) for x in NBitAdder([Variable("a", True), Variable("b")], [Variable("c"), Variable("d")])[0]])
print(NBitAdder([Variable("a", True), Variable("b")], [Variable("c"), Variable("d")])[1].qcompat())
print(NBitAdder([Variable("a", True), Variable("b")], [Variable("c"), Variable("d")])[1].qcompat().simplify())

# print(Xor(Not(Variable("a")),Variable("b", True)).simplify())
# print(And(Variable("a"), Not(Variable("a"))).simplify())
# print(And(Variable("a"), Not(Not(Variable("a")))).simplify())
# print(Xor(Variable("a"), Not(Variable("a"))).simplify())
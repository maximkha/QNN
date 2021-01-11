from Circuits import NBitAdder
from Components import Reg

print(str(NBitAdder(Reg("a", 2),Reg("b", 2))[1].simplify()))
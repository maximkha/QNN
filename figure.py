from Components import *
from tqdm import tqdm
from timeit import default_timer as timer

def generateLevel(sources, gates1, gates2):
    outputs = []
    for sourceA in tqdm(sources):
        # for singleGate in gates1:
        #     outputs.append(singleGate(sourceA).simplify())
        for singleGate in gates1:
            outputs.append(singleGate(sourceA))
        for sourceB in sources:
            # if sourceA in [True, False]:
            #     if sourceB not in [True, False]:
            #         if sourceA == sourceB.simplify():
            #             continue
            #     else:
            #         continue
            # elif sourceB in [True, False]:
            #     if sourceA not in [True, False]:
            #         if sourceA.simplify() == sourceB:
            #             continue
            #     else:
            #         continue
            # elif sourceA.simplify() == sourceB.simplify():
            #     continue
            for doubleGate in gates2:
                outputs.append(doubleGate(sourceA, sourceB))
    return outputs

def evaluteState(sources, outputs, tablein, tableout):
    candidates = outputs[:] #NO DEEP COPY!!!
    newCandidates = []

    for tabin, tabout in list(zip(tablein, tableout)):
        for i in range(len(sources)):
            sources[i].define(tabin[i])
        for out in tqdm(candidates):
            # if out in [True, False]:
            #     if out == tabout:
            #         newCandidates.append(out)
            # elif tabout == out.eval():
            #     newCandidates.append(out)
            if tabout == out.eval():
                newCandidates.append(out)
        candidates = newCandidates
        newCandidates = []

    for source in sources:
        source.define(None)
    
    return newCandidates

def trySolve(gates1, gates2, depthMax, tablein, tableout):
    currentLevel = [Variable(str(i), None) for i in range(len(tableIn[0]))]
    baseSources = currentLevel[:]
    for i in range(depthMax):
        print("Generating...")
        start = timer()
        currentLevel = generateLevel(currentLevel, gates1, gates2)
        end = timer()
        print("Gen took " + str((end-start)) + "sec")

        print("Evaling...")
        start = timer()
        canditates = evaluteState(baseSources, currentLevel, tablein, tableout)
        end = timer()
        print("Eval took " + str((end-start)) + "sec")

        print("Level = " + str(i))
        print("N     = " + str(len(currentLevel)))
        print("CAND  = " + str(len(canditates)))
        if (len(canditates) > 0):
            return canditates
    return []

tableIn = [
    [False, False],
    [False, True],
    [True, False],
    [True, True]
]

tableOut = [
    False, 
    False, 
    False, 
    True
]

singleGates = [Not, PassThrough]
doubleGates = [Xor]
depth = 1

#take some operations and create a different operation from them.
print(trySolve(singleGates, doubleGates, 5, tableIn, tableOut))
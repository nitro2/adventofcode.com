import sys
import numpy as np

def printarr(data):
    print("\n".join([d for d in data]))


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read()
        result_list = [findmirror(d) for d in data.split("\n\n")]
        print("result_list", result_list)
        x = tuple(map(sum, zip(*result_list)))
        result = x[0]*100 + x[1]
        print("Result:", result)
        return result

def findmirror(block):
    a = np.array(block.split("\n"))
    # a = block.split("\n")
    print("="*100)
    print(a)
    hashrow = [hash(r) for r in a]
    vr = checkmirror(hashrow)

    for c in zip(*a):
        print(c)
    hashcol = [hash(c) for c in zip(*a)]
    vc = checkmirror(hashcol)
    
    print("vr, vc", vr, vc)
    return vr, vc

def checkmirror(hashtable):
    print("hashtable", hashtable)
    v = 0
    for i in range(len(hashtable)-1):
        if hashtable[i] == hashtable[i+1]:
            if checkback(hashtable, i):
                v = i+1
                break
    return v

def checkback(hashtable, i):
    print(i, len(hashtable))
    for j in range(i+1):
        if i+1+j >= len(hashtable): return True
        print(hashtable[i-j] , hashtable[i+1+j])
        if hashtable[i-j] != hashtable[i+1+j]:
            return False
    return True


if __name__ == '__main__':
    assert solution("input13.sample.txt") == 405

    filename = sys.argv[1]
    res = solution(filename)


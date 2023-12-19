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

# This function takes '##.#####.#####...' as input 
# Then convert it to  '00100000100000111' as output
# Prepare for next xor command
def newhash(str):
    m = "".join(map(lambda x: '1' if x == '.' else '0', str))
    print("m", m)
    return m

class Match:
    EXACT="EXACT"
    NEARLY="NEARLY"
    NO="NO"

def compare(str1, str2):
    x = int(str1, 2)^int(str2, 2)
    if x==0:
        return Match.EXACT
    elif x and not (x & (x-1)):
        return Match.NEARLY
    else:
        return Match.NO


def findmirror(block):
    a = np.array(block.split("\n"))
    # a = block.split("\n")
    print("="*100)
    print(a)
    print("check row")
    hashrow = [newhash(r) for r in a]
    vr = checkmirror(hashrow)

    print("check col")
    hashcol = [newhash("".join(i for i in c)) for c in zip(*a)]
    vc = checkmirror(hashcol)
    
    print("vr, vc", vr, vc)
    return vr, vc

def checkmirror(hashtable):
    print("hashtable", hashtable)
    v = 0
    for i in range(len(hashtable)-1):
        # if hashtable[i] == hashtable[i+1]:
        if compare(hashtable[i], hashtable[i+1]) == Match.EXACT or compare(hashtable[i], hashtable[i+1]) == Match.NEARLY: 
            if checkback(hashtable, i):
                v = i+1
                break
    return v

def checkback(hashtable, i):
    print(i, len(hashtable))
    countnear = 1
    j=0
    for j in range(i+1):
        if i+1+j >= len(hashtable): 
            if countnear == 0:
                return True
            return False
        print(hashtable[i-j] , hashtable[i+1+j])
        # if hashtable[i-j] != hashtable[i+1+j]:
        x = compare(hashtable[i-j], hashtable[i+1+j])
        if x == Match.NO:
            return False
        elif x == Match.NEARLY:
            countnear -= 1
            if countnear < 0:
                return False
    if countnear == 0:
        print("Found mirror", j+1)
        return True
    return False


if __name__ == '__main__':
    assert newhash('##.#####.#####...') == '00100000100000111'
    assert compare('00100000100000111','00100000100000111') == Match.EXACT
    assert compare('00100000110000111','00100000100000111') == Match.NEARLY
    assert compare('00100000100000111','00100000100000110') == Match.NEARLY
    assert compare('00100000100000111','10100000100000110') == Match.NO
    assert compare('010011001','110100101') == Match.NO


    assert solution("input13.sample.txt") == 400

    filename = sys.argv[1]
    res = solution(filename)


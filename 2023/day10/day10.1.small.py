import sys
import math
import numpy

def printarr(arr):
    for a in arr:
        print(a)

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()

        result = 0
        arr = []
        S = (0,0)
        for i, line in enumerate(data):
            arr.append(list(line.rstrip()))
            # Find S position:
            j = line.find('S')
            if j >= 0:
                S = (j,i)

        printarr(arr)
        print('S=', S)
        width =  len(data[0])
        height = len(data)

        searched = set()
        result = findloop(arr, S, S, width, height, searched)

        print("Count =", result)
        return math.ceil(result/2.0)

def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)

def validconnection(direction, symbol):
    ds = getdirection(symbol)
    if ds != None:
        if (direction in ds):
            return True
    return False

def getsymbol(arr, pos):
    try:
        return arr[pos[1]][pos[0]]
    except Exception as e:
        # print(e, pos)
        # raise
        return "."

class Dir:
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)

'''
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
'''
dirdict = {
    '|':(Dir.NORTH, Dir.SOUTH),
    '-':(Dir.EAST,  Dir.WEST ),
    'L':(Dir.NORTH, Dir.EAST ),
    'J':(Dir.NORTH, Dir.WEST ),
    '7':(Dir.SOUTH, Dir.WEST ),
    'F':(Dir.SOUTH, Dir.EAST ),
    '.':(),
    'S':(Dir.NORTH, Dir.SOUTH, Dir.EAST,  Dir.WEST),
}
revertdirdict = {
    '|':(Dir.SOUTH, Dir.NORTH),
    '-':(Dir.WEST,  Dir.EAST ),
    'L':(Dir.SOUTH, Dir.WEST ),
    'J':(Dir.SOUTH, Dir.EAST ),
    '7':(Dir.NORTH, Dir.EAST ),
    'F':(Dir.NORTH, Dir.WEST ),
    '.':(),
    'S':(),
}
def getdirection(c):
    return revertdirdict[c]
    

# We recursively search all nearby node from a position and mark that position as searched
# Stop when we found S again
def findloop(arr, p, init, width, height, searched):
    symbol = getsymbol(arr, p)
    print(p, symbol)
    nextdir = dirdict[symbol]
    for d in nextdir:
        np = tuple(numpy.add(p, d))
        print("dir", d, getsymbol(arr, np))
        if not np in searched:
            if np == init: return 1 # Stop if we went through a full loop
            if validposition(np, width, height) and validconnection(d, getsymbol(arr, np)):
                searched.add(p)
                return 1 + findloop(arr, np, init, width, height, searched)
    return 0





if __name__ == '__main__':
    # Test
    res = solution("input10.sample.1.txt")
    assert res == 4

    res = solution("input10.sample.2.txt")
    assert res == 4

    res = solution("input10.sample.3.txt")
    assert res == 8

    filename = sys.argv[1]
    res = solution(filename)
    print("Result:", res)


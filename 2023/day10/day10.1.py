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
    return (0 <= p[0] < width) and (0 <= p[1] < height)


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
# dirdict = {
#     '|':{Dir.NORTH, Dir.SOUTH},
#     '-':{Dir.EAST,  Dir.WEST},
#     'L':{Dir.NORTH, Dir.EAST},
#     'J':{Dir.NORTH, Dir.WEST},
#     '7':{Dir.SOUTH, Dir.WEST},
#     'F':{Dir.SOUTH, Dir.EAST},
#     '.':{},
#     'S':{Dir.NORTH, Dir.SOUTH, Dir.EAST,  Dir.WEST},
# }

nextdir = {
    '|':{Dir.SOUTH:Dir.SOUTH, Dir.NORTH:Dir.NORTH},
    '-':{Dir.WEST:Dir.WEST, Dir.EAST:Dir.EAST },
    'L':{Dir.SOUTH:Dir.EAST,  Dir.WEST:Dir.NORTH},
    'J':{Dir.SOUTH:Dir.WEST, Dir.EAST:Dir.NORTH},
    '7':{Dir.EAST:Dir.SOUTH, Dir.NORTH:Dir.WEST },
    'F':{Dir.NORTH:Dir.EAST, Dir.WEST:Dir.SOUTH },
    '.':{},
    'S':{},
}

def getnextdir(inputdir, symbol):
    return nextdir.get(symbol).get(inputdir)

# We recursively search all nearby node from a position and mark that position as searched
# Stop when we found S again
def findloop(arr, p, init, width, height, searched):
    np = (-1,-1)
    count = 0
    # init dir
    nextdirlist =  {Dir.NORTH, Dir.SOUTH, Dir.EAST,  Dir.WEST}

    while np != init or count < 3:
        np = p
        for d in nextdirlist:
            np = tuple(numpy.add(p, d))
            if np == init and count > 2: return count # Stop if we went through a full loop
            symbol = getsymbol(arr, np)
            if validposition(np, width, height):
                od = getnextdir(d, symbol) # output direction
                if od:
                    print("nextdir=od{} added={}".format(od, symbol))
                    searched.add(p)
                    count +=1
                    nextdirlist = {od}
                    p = np
                    break

    return count





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


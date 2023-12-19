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

        # printarr(arr)
        # print('S=', S)
        width =  len(data[0])
        height = len(data)

        searched = set()
        marker = dict()
        result = findloop(arr, S, S, width, height, searched, marker)
        
        # Part 2 - we loop through the array and mark I and O based on marker
        currmark = 0
        countI = 0
        countO = 0
        searched.add(S)

        for j, row in enumerate(arr):
            for i, v in enumerate(row):
                symbol = getsymbol(arr,(i,j))
                if not (i,j) in searched:
                    if currmark == 0:
                        symbol = '0'
                        countO += 1
                    else:
                        symbol = 'I'
                        countI += 1
                else:
                    c = marker.get((i,j))
                    if c:
                        currmark = c
                    else:
                        currmark = 0
                # print(transform[symbol],end=' ')
            # print()

        # print("Count =", result)
        # return math.ceil(result/2.0)
        print("CountI=", countI)
        print("CountO=", countO)
        return countI

transform = {
    'F':'┌', '7':'┐', 'L':'└', 'J':'┘', '.':' ', '0':'0', 'I':'I', '-':'─', '|':'|', 'S':'S'
}

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

# nextdir = {
#     '|': {Dir.SOUTH: Dir.SOUTH, Dir.NORTH: Dir.NORTH},
#     '-': {Dir.WEST: Dir.WEST, Dir.EAST: Dir.EAST},
#     'L': {Dir.SOUTH: Dir.EAST,  Dir.WEST: Dir.NORTH},
#     'J': {Dir.SOUTH: Dir.WEST, Dir.EAST: Dir.NORTH},
#     '7': {Dir.EAST: Dir.SOUTH, Dir.NORTH: Dir.WEST},
#     'F': {Dir.WEST: Dir.SOUTH, Dir.NORTH: Dir.EAST, },
#     '.': {},
#     'S': {},
# }


nextdir = {
    '|': ((Dir.SOUTH, Dir.SOUTH),( Dir.NORTH, Dir.NORTH)),
    '-': ((Dir.WEST, Dir.WEST ), ( Dir.EAST, Dir.EAST  )),
    'L': ((Dir.SOUTH, Dir.EAST), ( Dir.WEST, Dir.NORTH )),
    'J': ((Dir.SOUTH, Dir.WEST), ( Dir.EAST, Dir.NORTH )),
    '7': ((Dir.EAST, Dir.SOUTH), ( Dir.NORTH, Dir.WEST )),
    'F': ((Dir.WEST, Dir.SOUTH), ( Dir.NORTH, Dir.EAST )),
    '.': {},
    'S': {},
}

def getnextdir(inputdir, symbol):
    for i, v in enumerate(nextdir.get(symbol)):
        if v[0] == inputdir:
            return v[1], i
    return None, None

# We recursively search all nearby node from a position and mark that position as searched
# Stop when we found S again
def findloop(arr, p, init, width, height, searched, marker):
    np = (-1,-1)
    count = 0
    # init dir
    nextdirlist =  {Dir.NORTH, Dir.SOUTH, Dir.EAST,  Dir.WEST}

    while np != init or count < 3:
        np = p
        for d in nextdirlist:
            np = tuple(numpy.add(p, d))
            if np == init and count > 2:
                searched.add(p)
                # print("searched", searched)
                # print('marker', marker)
                return count # Stop if we went through a full loop
            symbol = getsymbol(arr, np)
            if validposition(np, width, height):
                od, omark = getnextdir(d, symbol) # output direction
                if od:
                    # print("nextdir=od{} added={} {}".format(od, symbol, np))
                    marker[np]=omark

                    searched.add(p)
                    count +=1
                    nextdirlist = {od}
                    p = np
                    break
                
            import time
            time.sleep(1)
            # print("end for d - p={} d={} np={} nextdirlist={}".format(p,d,np, nextdirlist))




if __name__ == '__main__':
    # Test
    # res = solution("input10.sample.1.txt")
    # # assert res == 1

    # res = solution("input10.2.sample.2.txt")
    # assert res == 8

    # res = solution("input10.2.sample.3.txt")
    # assert res == 10

    filename = sys.argv[1]
    res = solution(filename)
    print("Result:", res)


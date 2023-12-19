import sys
import numpy as np
from collections import Counter
import heapq

class Dir:
    #      (y, x)
    #  (up/down, left/right)
    L = (0, -1)
    R = (0, 1)
    U = (-1, 0)
    D = (1, 0)
    O = (0, 0)
    # Debug purpose
    name = {
        L:"L",
        R:"R",
        U:"U",
        D:"D",
        O:"O"
    }
    # Return next position
    def move(pos, dir):
        return tuple(map(sum, zip(pos, dir)))

    def str(dir):
        return Dir.name[dir]
    
def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)

def printarr(data):
    for d in data:
        print(" ".join(map(str,map(int,d))))

def printoutput(dist, data):
    h,w = data.shape
    out = np.empty([w,h], dtype=tuple)
    for k, v in dist.items():
        out[k[0][0]][k[0][1]] = (v,k)
    
    print(out)

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read().rstrip().split('\n')
        data = np.array([list(map(int,d)) for d in data])
        h, w = data.shape
        print(data)
        dist, _ = find_shortest(data, (Dir.O, Dir.O, Dir.O))
        # printoutput(dist, data)

        result = min(dist[((h-1,w-1),Dir.D)], dist[((h-1,w-1),Dir.R)])
        print("Result:", result)
        return result


'''
    Shortest path to f((n,m)) is 
    c(n-1,m)+f(n-1,m,>>v)
    c(n-1,m)+f(n-1,m,>vv)
    c(n-1,m)+f(n-1,m,vvv)
'''
def find_shortest(data, init_dir3):
    h, w = data.shape

    # Implement Dijkstra's
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    # Create the distance dictionary from (0,0) to any node:
    dist = dict() # (v, dir3)
    prev = dict()
    Q = list()
    v = (0,0)
    d = Dir.O
    dist[(v,d)] = 0
    
    heapq.heappush(Q, (dist[(v,d)], v, init_dir3))
    for i in range(h):
        for j in range(w):
            v = (i,j)
            for d in [Dir.U, Dir.D, Dir.R, Dir.L]:
                if v != (0,0):
                    dist[(v,d)] = sys.maxsize
                    prev[(v,d)] = None
                else:
                    dist[(v,d)] = 0
            

    while len(Q) > 0:
        _, u, dir3 = heapq.heappop(Q) # Remove and return best vertex
        # Go through all v neighbors of u
        for d in [Dir.U, Dir.D, Dir.R, Dir.L]:
            v = Dir.move(u, d)
            if validposition(v, w, h) and validdirection(dir3, d):
                alt = dist[(u,dir3[2])]+data[v[0]][v[1]]
                if alt < dist[(v,d)]:
                    dist[(v,d)] = alt
                    prev[(v,d)] = u
                    # if v not in Q:
                    if not check_v_in_Q(Q, v, (dir3[1], dir3[2], d)):
                        heapq.heappush(Q, (dist[(v,d)], v, (dir3[1], dir3[2], d)))
                    else:
                        raise

    print("dist", dist)
    # print("prev", prev)
    return dist, prev

def check_v_in_Q(Q, v, dir3):
    for item in Q:
        if item[1] == v and item[2] == dir3: return True
    return False


def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)

def validdirection(dir3, d):
    if dir3[0] == dir3[1] == dir3[2] == d:
        return False
    return True

if __name__ == '__main__':
    assert solution("input17.test.1.txt") == 4
    assert solution("input17.test.2.txt") == 14
    assert solution("input17.sample.txt") == 102
    # filename = sys.argv[1]
    # res = solution(filename)

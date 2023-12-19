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
        L:"LEFT",
        R:"RIGHT",
        U:"UP",
        D:"DOWN"
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
    out = np.zeros(data.shape)
    for v, k in dist.items():
        out[v[0]][v[1]] = k
    
    print(out)

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read().rstrip().split('\n')
        data = np.array([list(map(int,d)) for d in data])
        h, w = data.shape
        print(data)
        dist, _ = find_shortest(data, (Dir.O, Dir.O, Dir.O))
        printoutput(dist, data)

        result = dist[(w-1,h-1)]
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
    dist = dict()
    prev = dict()
    Q = list()
    dist[(0,0)] = 0
    v = (0,0)
    heapq.heappush(Q, (dist[v], v, init_dir3))
    for i in range(h):
        for j in range(w):
            v = (i,j)
            if v != (0,0):
                dist[v] = sys.maxsize
                prev[v] = None
            

    while len(Q) > 0:
        _, u, dir3 = heapq.heappop(Q) # Remove and return best vertex
        # Go through all v neighbors of u
        for d in [Dir.U, Dir.D, Dir.R, Dir.L]:
            v = Dir.move(u, d)
            if validposition(v, w, h) and validdirection(dir3, d):
                alt = dist[u]+data[v[0]][v[1]]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    if v not in Q:
                        heapq.heappush(Q, (dist[v], v, (dir3[1], dir3[2], d)))
                    else:
                        raise

    print("dist", dist)
    # print("prev", prev)
    return dist, prev


def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)

def validdirection(dir3, d):
    if dir3[0] == dir3[1] == dir3[2] == d:
        return False
    return True

if __name__ == '__main__':
    assert solution("input17.sample.txt") == 102
    filename = sys.argv[1]
    res = solution(filename)

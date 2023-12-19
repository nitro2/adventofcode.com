import sys
import numpy as np

class Dir:
    #      (y, x)
    #  (up/down, left/right)
    L = (0, -1)
    R = (0, 1)
    U = (-1, 0)
    D = (1, 0)
    O = (0, 0)
    # Debug purpose
    name = {L: "L", R: "R", U: "U", D: "D", O: "O"}
    ins = {"L": L, "R": R, "U": U, "D": D, "O": O}
    # Return next position

    def move(pos, dir, step=1):
        return (pos[0]+dir[0]*step, pos[1]+dir[1]*step)

    def str(dir):
        return Dir.name[dir]

    def get(d):
        return Dir.ins[d]


def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)


def printarr(data):
    for d in data:
        print("".join(d))


def solution(filename):
    with open(filename, "r") as fi:
        result = 0
        data = fi.read().rstrip().split('\n')

        data = np.array([d.split() for d in data])
        h, w = data.shape
        # print(data)
        direction = data[:, 0]
        length = np.array(data[:, 1], dtype=int)
        print(direction)
        print(length)
        vector = build_vector(direction, length)
        graph, vector = calibrate(vector) # Find the min edge then minus the whole point to it
        draw_graph(graph, vector, direction, length)
        
        result = count_cubic(graph)

        print("Result:", result)
        return result


def build_vector(direction, length):
    v = (0, 0)
    vector = list()
    vector.append(v)
    for d, l in zip(direction, length):
        print(Dir.get(d), l)
        u = Dir.move(v, Dir.get(d), int(l))
        vector.append(u)
        v = u
    return vector

def calibrate(vector):
    print("Before calibrate: ", vector)
    minx , miny = vector[0]
    maxx , maxy = vector[0]
    # Find min(x,y)
    for x, y in vector:
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)
    # Calibrate the points
    # Create new vector
    newvector = list()
    for x,y in vector:
        x = x-minx
        y = y-miny
        newvector.append((x,y))
    maxx -= minx
    maxy -= miny
    print("After calibrate: ", newvector)
    # Return new graph
    return np.full((maxx+1,maxy+1), '.'), newvector

def draw_graph(graph, vector, direction, length):
    # print(graph)
    v = vector[0]
    graph[v[0]][v[1]] ='#'
    for d, l, v in zip(direction, length, vector):
        if d == 'R':
            for i in range(v[1], v[1]+l, 1):
                graph[v[0]][i] = '#'
        elif d == 'L':
            for i in range(v[1], v[1]-l, -1):
                graph[v[0]][i] = '#'
        elif d == 'U':
            for i in range(v[0], v[0]-l, -1):
                graph[i][v[1]] = '#'
        elif d == 'D':
            for i in range(v[0], v[0]+l, 1):
                graph[i][v[1]] = '#'
    # np.set_printoptions(threshold=sys.maxsize)
    # print(graph)
    printarr(graph)

'''
....out->...########.................
.....in->...#......#.................
............#......#.................
............#......#.................
....#########......###########.......
....#........................#.......
....#........................#.......
....#........................#######.
'''
def count_cubic(graph):
    count = 0
    for i, r in enumerate(graph):
        odd = 0
        inside = False
        prev = '.'
        for j, v in enumerate(r):
            if v == '#':
                count += 1
                if i!= 0 and graph[i-1][j] == '#':
                    inside = not inside
            else: # get '.'
                if inside:
                    count += 1
                    graph[i][j]='$'
                
            prev = v
    print("count", count)
    printarr(graph)
    return count
                



if __name__ == '__main__':
    assert Dir.move((1, 1), Dir.R, 3) == ((1, 4))
    # assert polygon_area([(0,0), (0,3), (1,3), (1,0)]) == 8
    assert solution("input18.sample.txt") == 62
    filename = sys.argv[1]
    res = solution(filename)
    #61865

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
    name = {L: 'L', R: 'R', U: 'U', D: 'D', O: 'O'}
    ins = {'L': L, 'R': R, 'U': U, 'D': D, 'O': O}
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
    with open(filename, 'r') as fi:
        result = 0
        data = fi.read().rstrip().split('\n')

        data = np.array([d.split() for d in data])
        h, w = data.shape
        # print(data)
        # direction = data[:, 0]
        # length = np.array(data[:, 1], dtype=int)
        direction = list()
        length = list()

        convert ={'0':'R', '1':'D', '2':'L', '3':'U'}
        color = (data[:, 2])
        for c in color:
            l = int(c[2:7],16)
            d = convert[c[7:8]]
            # print(d,l)
            direction.append(d)
            length.append(l)

        print("color", color)

        print(direction)
        print(length)

        vector = build_vector(direction, length)

        # Shoelace formular
        A = polygon_area(vector)
        b = sum([l for l in length])
        # Pick's theory
        # A = i + b/2 - 1
        # i = A + 1 - b/2
        i = A + 1 - b/2
        result = int(i + b)
        print(result)

        print("Result:", result)
        return result


def build_vector(direction, length):
    v = (0, 0)
    vector = list()
    vector.append(v)
    for d, l in zip(direction, length):
        print(d, l)
        u = Dir.move(v, Dir.get(d), int(l))
        vector.append(u)
        v = u
    return vector


# Calculate area base on https://en.wikipedia.org/wiki/Shoelace_formula
def polygon_area(V):
    # Initialize area
    area = 0
    # print(V)
    n = len(V)
    j = n - 1
    for i in range(0, n):
        area += (V[j][0] - V[i][0]) * (V[j][1] + V[i][1])
        j = i
    res =  int(abs(area / 2))
    print("polygon_area", res)
    return res


if __name__ == '__main__':
    assert Dir.move((1, 1), Dir.R, 3) == ((1, 4))
    # assert polygon_area([(0,0), (0,3), (1,3), (1,0)]) == 8
    assert solution("input18.sample.txt") == 952408144115
    filename = sys.argv[1]
    res = solution(filename)
    #61865

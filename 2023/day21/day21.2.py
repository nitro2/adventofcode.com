import sys


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
        L: "L",
        R: "R",
        U: "U",
        D: "D",
        O: "O"
    }
    # Return next position

    def move(pos, dir):
        return tuple(map(sum, zip(pos, dir)))

    def str(dir):
        return Dir.name[dir]


def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)


def part1(filename, steps):
    print("="*100)
    with open(filename, "r") as fi:
        result = 0
        data = fi.read().rstrip().split('\n')
        arr = [list(d) for d in data]
        # print(arr)
        S = getS(arr)

        result = count_plots(arr, S, steps)

        print("Result:", result)
        return result

def getS(arr):
    for i, r in enumerate(arr):
        for j in range(len(r)):
            if arr[i][j] == 'S':
                return (i, j)
    raise


def count_plots(arr, S, steps):
    searched = set()
    odd_searched = set()
    even_searched = set()
    searching = [S]
    h = len(arr)
    w = len(arr[0])

    for s in range(steps):
        # print("Step ", s+1, "searching", searching)
        nextsearch = set()
        for v in searching:
            for d in [Dir.U, Dir.D, Dir.R, Dir.L]:
                u = Dir.move(v, d)
                if validposition(u, w, h) and arr[u[0]][u[1]] != '#' and not u in searched:
                    nextsearch.add(u)
        if (s+1) % 2:
            odd_searched |= nextsearch
        else:
            even_searched |= nextsearch
        searching = nextsearch

    # print("even:", even_searched)
    # print("odd", odd_searched)
    return len(odd_searched) if steps % 2 else len(even_searched)

###################################################################

def part2_bruteforce(filename):
    print("="*100)
    with open(filename, "r") as fi:
        result = 0
        data = fi.read().rstrip().split('\n')
        arr = [list(d) for d in data]
        # print(arr)
        S = getS(arr)

        result = count_plots2_bruteforce(arr, S, 500)
        print("Result:", result)
        return result


def count_plots2_bruteforce(arr, S, steps):
    searched = set()
    odd_searched = set()
    even_searched = set()
    searching = [S]
    h = len(arr)
    w = len(arr[0])

    result = 0
    for s in range(steps):
        # print("Step ", s+1, "searching", searching)
        nextsearch = set()
        for v in searching:
            for d in [Dir.U, Dir.D, Dir.R, Dir.L]:
                u = Dir.move(v, d)
                if get_symbol(arr, u, w, h) != '#' and not u in searched:
                    nextsearch.add(u)
        if (s+1) % 2:
            odd_searched |= nextsearch
        else:
            even_searched |= nextsearch
        searching = nextsearch
        result = len(odd_searched) if s % 2 else len(even_searched)
        print("Step ", s, "Sub result", result)

    # print("even:", even_searched)
    # print("odd", odd_searched)
    return len(odd_searched) if steps % 2 else len(even_searched)


def get_symbol(arr, u, w, h):
    x, y = u
    x = x%h
    y = y%w
    return arr[x][y]

if __name__ == '__main__':

    # assert part1("input21.sample.1.txt", steps=1) == 2
    # assert part1("input21.sample.1.txt", steps=2) == 4
    # assert part1("input21.sample.1.txt", steps=3) == 6
    # assert part1("input21.sample.1.txt", steps=6) == 16
    # assert part1("input21.txt",64) == 3762

    
    part2_bruteforce("input21.sample.1.txt")

    # filename = sys.argv[1]
    # res = part1(filename)

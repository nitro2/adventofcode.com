import sys

def printdebug(*args):
    pass

def printarr(data, debug="off"):
    if debug != "off":
        print("\n".join(["".join(d) for d in data]))

def solution(filename, numcycle):
    with open(filename, "r") as fi:
        data = [list(i.rstrip()) for i in fi.read().splitlines() ]
        printarr(data)
        printdebug()
        data, result = cycle(data, numcycle)
        # printarr(data, debug="on")
        print("Result:", result)
        return result

def cycle(data, numcycle=0):
    for i in range(numcycle):
        printdebug("-"*100)
        data = go_north(data)
        printdebug("-"*100)
        data = go_west(data)
        printdebug("-"*100)
        data = go_south(data)
        printdebug("-"*100)
        data = go_east(data)
        acc = get_load(data)
        print("Cycle", i+1, "acc", acc)
    return data, acc

def get_load(data):
    return sum([r.count('O') * (len(data)-i) for i, r in enumerate(data)])

def go_north(data):
    limit = [0]*len(data[0])
    for i, r in enumerate(data):
        for j, c in enumerate(r):
            if c == 'O':
                if data[limit[j]][j] == '.':
                    data[i][j]='.'
                    data[limit[j]][j] = 'O'
                limit[j] += 1
            elif c == '#':
                limit[j] = i+1
    printarr(data)
    return data

def go_south(data):
    data = data[::-1]
    limit = [0]*len(data[0])
    for i, r in enumerate(data):
        for j, c in enumerate(r):
            if c == 'O':
                if data[limit[j]][j] == '.':
                    data[i][j]='.'
                    data[limit[j]][j] = 'O'
                limit[j] += 1
            elif c == '#':
                limit[j] = i+1
    data = data[::-1]
    printarr(data)
    return data

def go_west(data):
    limit = [0]*len(data[0])
    for i, r in enumerate(data):
        for j, c in enumerate(r):
            if c == 'O':
                if data[i][limit[i]] == '.':
                    data[i][j]='.'
                    data[i][limit[i]] = 'O'
                limit[i] += 1
            elif c == '#':
                limit[i] = j+1
    printarr(data)
    return data

def go_east(data):
    limit = [0]*len(data[0])
    for i, r in enumerate(data):
        data[i] = data[i][::-1]
        for j, c in enumerate(data[i]):
            if c == 'O':
                if data[i][limit[i]] == '.':
                    data[i][j]='.'
                    data[i][limit[i]] = 'O'
                limit[i] += 1
            elif c == '#':
                limit[i] = j+1
        data[i] = data[i][::-1]
    printarr(data)
    return data


if __name__ == '__main__':
    # Calculate after 100 cycle:
    # Cycle start at Cycle 3, period = 7
    # (100-3)%7 = 6 ==> Cycle 100 = Cycle 6+3 = Cycle 9
    # assert solution("input14.sample.txt", numcycle = 100) == 68 #-> period=7
    
    
    # Calculate after 1000 cycles:
    # Cycle start at Cycle 105, period = 13
    '''
    Cycle 106 acc 87286
    Cycle 107 acc 87284
    Cycle 108 acc 87282
    Cycle 109 acc 87264
    Cycle 110 acc 87258
    Cycle 111 acc 87272
    Cycle 112 acc 87286
    Cycle 113 acc 87288
    Cycle 114 acc 87271
    Cycle 115 acc 87266
    Cycle 116 acc 87273
    Cycle 117 acc 87287
    Cycle 118 acc 87292
    '''
    # (1000-105)%13 = 11  ==> Cycle 1000 = Cycle 11+105 = Cycle 116 = 87273
    assert solution("input14.txt", 1000) == 87273 #--> period=13
    
    # (1000000000-105)%13 + 105 = 116 -> Cycle 116 acc 87273
    # assert solution("input14.txt", 1000000000) == 87273

    # filename = sys.argv[1]
    # res = solution(filename)


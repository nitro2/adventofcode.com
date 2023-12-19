import sys
import numpy as np

def printarr(data):
    print("\n".join([d for d in data]))

def checkemptyspace(l):
    return len(set(list(l))) == 1 and set(list(l)) == set('.')

def solution(filename, expand_factor=2):
    with open(filename, "r") as fi:
        data = fi.readlines()
 
        a = np.array([list(line.rstrip()) for line in data])
        print(a)

        # Get empty row
        emptyrow = [i for i in range(len(a)) if checkemptyspace(a[i, :])]
        # print("emptyrow", emptyrow)

        # Get empty column
        emptycol = [i for i in range(len(a[0])) if checkemptyspace(a[:, i])]
        # print("emptycol", emptycol)
    
        # Find galaxies
        galaxies = np.where(a == '#')
        gal = list(zip(galaxies[0], galaxies[1]))
        #gal = [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
        # print(gal)
        result = 0
        for i in range(len(galaxies[0])):
            for j in range(i, len(galaxies[0])):
                    result += distance(gal[i],gal[j], emptycol, emptyrow, expand_factor) 

        print("Result:", result)
        return result

def distance(g1, g2, emptycol, emptyrow, expand_factor=2):
    x2 = max(g1[0], g2[0])
    x1 = min(g1[0], g2[0])
    y2 = max(g1[1], g2[1])
    y1 = min(g1[1], g2[1])
    er = list(filter(lambda x: x1<x<x2, emptyrow))
    ec = list(filter(lambda y: y1<y<y2, emptycol))

    return x2-x1 + y2-y1 + (len(ec)+len(er))*(expand_factor-1)


if __name__ == '__main__':
    emptycol = [2, 5, 8]
    emptyrow = [3, 7]
    assert distance((5,1), (9,4), emptycol, emptyrow) == 9 #Between galaxy 5 and galaxy 9: 9
    assert distance((0,3), (8,7), emptycol, emptyrow) == 15 #Between galaxy 1 and galaxy 7: 15
    assert distance((2,0), (6,9), emptycol, emptyrow) == 17 #Between galaxy 3 and galaxy 6: 17
    assert distance((9,0), (9,4), emptycol, emptyrow) == 5 #Between galaxy 8 and galaxy 9: 5


    # Test - part 1
    res = solution("input11.sample.1.txt", 2)
    assert res == 374

    res = solution("input11.sample.1.txt", 10)
    assert res == 1030

    res = solution("input11.sample.1.txt", 100)
    assert res == 8410

    filename = sys.argv[1]
    res = solution(filename, 1000000)


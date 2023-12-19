import sys
import numpy as np

def printarr(data):
    print("\n".join([d for d in data]))

def checkemptyspace(l):
    return len(set(list(l))) == 1 and set(list(l)) == set('.')

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        newarr = []
        for line in data:
            l = line.rstrip()
            newarr.append(list(l))
            # Duplicate line if contain only .
            if checkemptyspace(l):
                newarr.append(list(l))

        a = np.array(newarr)

        # Get empty column
        emptycol = []
        for i in range(len(a[0])):
            if checkemptyspace(a[:, i]):
                emptycol.append(i)

        # Insert 
        a = np.insert(a, emptycol, '.', axis=1)

        print(a)

        # Finish expand universe
        # galaxies = (array([ 0,  1,  2,  5,  6,  7, 10, 11, 11]), array([ 4,  9,  0,  8,  1, 12,  9,  0,  5]))
        galaxies = np.where(a == '#')
        gal = list(zip(galaxies[0], galaxies[1]))
        print(gal)
        result = 0
        for i in range(len(galaxies[0])):
            for j in range(i, len(galaxies[0])):
                    result += distance(gal[i],gal[j]) 

        print("Result:", result)
        return result

def distance(g1, g2):
    return abs(g2[0]-g1[0]) + abs(g2[1]-g1[1])


if __name__ == '__main__':
    assert distance((6,1), (11,5)) == 9 #Between galaxy 5 and galaxy 9: 9
    assert distance((0,4), (10,9)) == 15 #Between galaxy 1 and galaxy 7: 15
    assert distance((2,0), (7,12)) == 17 #Between galaxy 3 and galaxy 6: 17
    assert distance((11,0), (11,5)) == 5 #Between galaxy 8 and galaxy 9: 5


    # Test
    res = solution("input11.sample.1.txt")
    assert res == 374


    filename = sys.argv[1]
    res = solution(filename)


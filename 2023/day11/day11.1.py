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
        

        return 0


if __name__ == '__main__':
    # Test
    res = solution("input11.sample.1.txt")
    assert res == 4

    res = solution("input11.sample.2.txt")
    assert res == 4


    filename = sys.argv[1]
    res = solution(filename)
    print("Result:", res)


import sys

def printarr(data):
    print("\n".join([d for d in data]))

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        
        height = len(data)
        base = [height]*len(data[0])
        result = 0
        print(base)
        for i, r in enumerate(data):
            for j, c in enumerate(list(r.rstrip())):
                if c == 'O':
                    result += base[j]
                    base[j] -= 1
                elif c == '#':
                    base[j] = height-i-1


        print("Result:", result)
        return result



if __name__ == '__main__':
    assert solution("input14.sample.txt") == 136

    filename = sys.argv[1]
    res = solution(filename)


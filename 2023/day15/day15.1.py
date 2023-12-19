import sys
import functools

def printarr(data):
    print("\n".join([d for d in data]))

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read().rstrip().split(',')
        
        result = sum([hash(d,0) for d in data])
        print("Result:", result)
        return result

def hash(str, seed):
    return functools.reduce(lambda x,y: ((ord(y) + x) * 17) % 256 ,list(str), seed)  

if __name__ == '__main__':
    assert hash("HASH", 0) == 52
    assert hash("rn=1", 0) == 30
    assert hash("cm-", 0) == 253
    assert hash("qp=3", 0) == 97

    assert solution("input15.sample.txt") == 1320
    filename = sys.argv[1]
    res = solution(filename)


import sys
import functools
import re
from collections import OrderedDict

def printarr(data):
    print("\n".join([d for d in data]))

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read().rstrip().split(',')
        
        result = 0
        boxes = [OrderedDict() for i in range(256)]
        for d in data:
            pattern = re.compile(r"(\w+)([\-\=])(\d*)")
            s = re.match(pattern, d)
            label = s.group(1)
            n = hash(label, 0)
            if s.group(2) == '-':
                if boxes[n].get(label):
                    del(boxes[n][label])
            elif s.group(2) == '=':
                lens = int(s.group(3))
                if not boxes[n].get(label):
                    boxes[n][label] = lens
                else:
                    boxes[n].update({label:lens})
            else:
                print("unknown")
                raise()
        # print(boxes)
        for i, b in enumerate(boxes):
            for j, item in enumerate(b.values()):
                result += (i+1)*(j+1)*item

        print("Result:", result)
        return result

def hash(str, seed):
    return functools.reduce(lambda x,y: ((ord(y) + x) * 17) % 256 ,list(str), seed)  

if __name__ == '__main__':
    # assert hash("HASH", 0) == 52
    # assert hash("rn=1", 0) == 30
    # assert hash("cm-", 0) == 253
    # assert hash("qp=3", 0) == 97

    assert solution("input15.sample.txt") == 145
    filename = sys.argv[1]
    res = solution(filename)


import sys
import re

import math

def solution(filenaem):
    with open(filename, "r") as fi:
        data = fi.read()
        # print(data)
        blocks = re.split(r'\n', data)
        print(blocks)

        time = list(map(int,blocks[0].split()[1:]))
        distance = list(map(int,blocks[1].split()[1:]))
        print(time,distance)

        res = 1
        for x,y in zip(time, distance):
            x1 = (x+math.sqrt(x*x-4*y))/2
            x2 = (x-math.sqrt(x*x-4*y))/2
            d=  math.floor(x1) - math.ceil(x2) + 1
            d -= x1.is_integer()*1 + x2.is_integer()*1
            # print(x,y,x1,x2,d)
            res *= d

        return res
        # reduce(lambda x,y: int((x+math.sqrt(x*x-4*y))/2) - int((x+math.sqrt(x*x-4*y))/2) )

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

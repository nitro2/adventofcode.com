import sys
import numpy as np

def printarr(data):
    print("\n".join([d for d in data]))


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        result = sum([arrangement(line) for line in data])
        print("Result:", result)
        return result

def arrangement(line):
    springs , records = line.rstrip().split()
    records = list(map(int,records.split(',')))
    print(springs, records)
    a = buildtree(springs, records, 0)

    print("arrangement", a)
    print("="*100)
    return a

def buildtree(springs, records, currdamage=0, debugtree=[]):
    print("{} \t{} {} {}".format("".join(debugtree),springs, records, currdamage))
    if len(springs) == 0:
        if currdamage == 0 and len(records)==0:
            print("Got 1")
            return 1
        if currdamage == records[0]:
            records = records[1:]
            currdamage = 0
            return buildtree(springs, records, currdamage, debugtree=debugtree)
        else:
            return 0 # Not a valid branch
    else:
        c = springs[0]
        if c == '.':
            if len(records)>0 and currdamage == records[0]:
                records = records[1:]
                currdamage = 0
            if currdamage > 0: return 0 # Should not increase current damage
            return buildtree(springs[1:], records, currdamage, debugtree=debugtree+[c])
        elif c == '#':
            if len(records) == 0: return 0
            currdamage += 1
            return buildtree(springs[1:], records, currdamage, debugtree=debugtree+[c])
        elif c == '?':
            return buildtree('.' + springs[1:],records, currdamage, debugtree=debugtree) + buildtree('#' + springs[1:],records, currdamage, debugtree=debugtree) 
        else:
            print("Unknown branch")
            return 0


if __name__ == '__main__':
    assert arrangement(".#.###.# 1,3,1") == 1
    assert arrangement("???.### 1,1,3") == 1
    assert arrangement(".??..??...?##. 1,1,3") == 4
    assert arrangement("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    assert arrangement("????.#...#... 4,1,1") == 1
    assert arrangement("????.######..#####. 1,6,5") == 4
    assert arrangement("?###???????? 3,2,1") == 10


    # Test
    assert solution("input12.sample.1.txt") == 21


    filename = sys.argv[1]
    res = solution(filename)


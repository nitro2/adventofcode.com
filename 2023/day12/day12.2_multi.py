import sys

def printarr(data):
    print("\n".join([d for d in data]))


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        result = sum([arrangement_part2_improve(line) for line in data])
        # print("Result:", result)
        print(result)
        return result

called = 0
def arrangement(line):
    springs , records = line.rstrip().split()
    records = list(map(int,records.split(',')))
    # print(springs, records)
    global called
    called = 0
    a = buildtree(springs, records, 0)

    # print("arrangement", a, "called", called)
    # print("="*100)
    return a

def arrangement_part2(line):
    springs , records = line.rstrip().split()
    records = list(map(int,records.split(',')))*5
    springs = '?'.join([springs]*5)
    # print(springs, records)
    global called
    called = 0
    a = buildtree(springs, records, 0)
    # print("arrangement_part2_origin", a, "called", called)
    # # print("arrangement2", a)
    # print("="*100)
    return a

def buildtree(springs, records, currdamage=0, debugtree=[]):
    global called
    called += 1
    # # print("{} \t{} {} {}".format("".join(debugtree),springs, records, currdamage))
    if len(springs) == 0:
        if currdamage == 0 and len(records)==0:
            # # print("Got 1")
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
            # print("Unknown branch")
            return 0

def arrangement_part2_improve(line):
    springs , records = line.rstrip().split()
    records = list(map(int,records.split(',')))*5
    springs = '?'.join([springs]*5)
    # print(springs, records)
    global called
    called = 0
    a = buildtree2(springs, records, 0)
    # print("arrangement_part2_improve", a, "called", called)
    return a

def buildtree2(springs, records, currdamage=0, debugtree=[]):
    global called
    called += 1
    # # print("{} \t{} {} {}".format("".join(debugtree),springs, records, currdamage))
    if len(springs) == 0:
        if currdamage == 0 and len(records)==0:
            # # print("Got 1")
            return 1
        if currdamage == records[0]:
            records = records[1:]
            currdamage = 0
            return buildtree2(springs, records, currdamage, debugtree=debugtree)
        else:
            return 0 # Not a valid branch
    else:
        c = springs[0]
        if c == '.':
            if len(records)>0:
                if currdamage == records[0]:
                    records = records[1:]
                    currdamage = 0
                elif currdamage > records[0]:
                    return 0
            if currdamage > 0: return 0 # Should not increase current damage
            return buildtree2(springs[1:], records, currdamage, debugtree=debugtree+[c])
        elif c == '#':
            if len(records) == 0: return 0
            currdamage += 1
            if currdamage > records[0]: return 0
            return buildtree2(springs[1:], records, currdamage, debugtree=debugtree+[c])
        elif c == '?':
            x = 0
            if (len(records) > 0 and foreseen('#' + springs[1:], records[0])) or True:
                x = buildtree2('#' + springs[1:],records, currdamage, debugtree=debugtree) 
            return buildtree2('.' + springs[1:],records, currdamage, debugtree=debugtree) + x
        else:
            # print("Unknown branch")
            return 0

def foreseen(springs, rec):
    x = springs.split('.')
    # # print("foreseen", x, rec)
    if len(x[0]) < rec: return False
    else: return True

if __name__ == '__main__':
    # assert arrangement(".#.###.# 1,3,1") == 1
    # assert arrangement("???.### 1,1,3") == 1
    # assert arrangement(".??..??...?##. 1,1,3") == 4
    # assert arrangement("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    # assert arrangement("????.#...#... 4,1,1") == 1
    # assert arrangement("????.######..#####. 1,6,5") == 4
    # assert arrangement("?###???????? 3,2,1") == 10

    # assert arrangement_part2(".#.###.# 1,3,1") == 1
    # assert arrangement_part2("???.### 1,1,3") == 1
    # assert arrangement_part2(".??..??...?##. 1,1,3") == 16384
    # assert arrangement_part2("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    # assert arrangement_part2("????.#...#... 4,1,1") == 16
    # assert arrangement_part2("????.######..#####. 1,6,5") == 2500
    # assert arrangement_part2("?###???????? 3,2,1") == 506250

    # assert arrangement_part2_improve(".#.###.# 1,3,1") == 1
    # assert arrangement_part2_improve("???.### 1,1,3") == 1
    # assert arrangement_part2_improve(".??..??...?##. 1,1,3") == 16384
    # assert arrangement_part2_improve("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    # assert arrangement_part2_improve("????.#...#... 4,1,1") == 16
    # assert arrangement_part2_improve("????.######..#####. 1,6,5") == 2500
    # assert arrangement_part2_improve("?###???????? 3,2,1") == 506250


    # # Test
    # assert solution("input12.sample.1.txt") == 525152


    filename = sys.argv[1]
    res = solution(filename)


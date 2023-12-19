import sys
import re

def solution(lines):
    pre_copy=[1]*len(lines)
    idx=0
    for line in lines:
        card = re.match(r"(Card\s+(\d+):\s*)((\d+\s*)+)\|\s*((\d+\s*)+)", line)
        print(card.groups())
        index = card.group(2)
        winnum = set(card.group(3).split())
        mynum = set(card.group(5).split())
        # print(winnum, mynum)
        count = 0
        for n in mynum:
            if n in winnum:
                count += 1
        if count > 0:
            for i in range(count):
                pre_copy[i+1+idx] += pre_copy[idx]
        idx += 1
    res = sum(pre_copy)
    return res


if __name__ == '__main__':
    filename = sys.argv[1]
    # filename = '/Users/nngo/Projects/Dreamer/adventofcode.com/2023/day04/input04.sample.txt'
    with open(filename, "r") as fi:
        print("Result:", solution(fi.readlines()))
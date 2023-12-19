import sys
import re

def solution(lines):
    # print(lines)

    # Make array
    arr = []
    sum = 0
    for line in lines:
        card = re.match(r"(Card\s+\d+:\s*)((\d+\s*)+)\|\s*((\d+\s*)+)", line)
        # print(card.groups())
        # print(card[2])
        winnum = set(card.group(2).split())
        mynum = set(card.group(4).split())
        print(winnum, mynum)
        count = 0
        for n in mynum:
            if n in winnum:
                count += 1
        if count > 0:
            sum += 2**(count-1)
    return sum


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as fi:
        print("Result:", solution(fi.readlines()))
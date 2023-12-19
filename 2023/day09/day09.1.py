import sys
import functools


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()

        result = 0
        for line in data:
            series = list(map(int, line.split()))
            # diff = [1]
            nextnum = series[-1]
            print("==========\n", series)
            while set(series) != {0}:
                series = list(map(lambda x, y: y - x, series[:-1], series[1:]))
                nextnum += series[-1]
                print(series, "---", nextnum)
            print("nextnum", nextnum)
            result += nextnum
        return result

if __name__ == '__main__':
    # Test
    res = solution("input09.sample.txt")
    assert res == 114

    filename = sys.argv[1]
    res = solution(filename) #1980437560
    print("Result:", res)


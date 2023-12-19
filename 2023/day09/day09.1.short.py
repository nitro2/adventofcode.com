import sys

def find_next(series):
    nextnum = series[-1]
    while set(series) != {0}:
        series = list(map(lambda x, y: y - x, series[:-1], series[1:]))
        nextnum += series[-1]
    return nextnum

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        return sum([find_next(list(map(int, line.split()))) for line in data])

if __name__ == '__main__':
    # Test
    res = solution("input09.sample.txt")
    assert res == 114

    res = solution("input09.txt")
    assert res == 1980437560

    filename = sys.argv[1]
    res = solution(filename) #1980437560
    print("Result:", res)



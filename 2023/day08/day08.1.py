import sys


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        return

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

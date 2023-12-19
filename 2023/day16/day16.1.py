import sys
import numpy as np
from collections import Counter

def printarr(data):
    for d in data:
        print(" ".join(map(str,map(int,d))))


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read().rstrip().split('\n')
        data = np.array([list(d) for d in data])
        print(data)
        energized = mark_energized(data)
        # print(energized)
        printarr(energized)

        result = len(np.where(energized != 0)[0])
        print("Result:", result)
        return result


class Dir:
    #      (y, x)
    #  (up/down, left/right)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    # Debug purpose
    name = {
        LEFT:"LEFT",
        RIGHT:"RIGHT",
        UP:"UP",
        DOWN:"DOWN"
    }
    # Return next position
    def move(pos, dir):
        return tuple(map(sum, zip(pos, dir)))

    
    def str(dir):
        return Dir.name[dir]

# energized is a double 3D array to store (checked, energized) values
# We recursively follow the beam, if a cell checked 2 times, it rejects new check.
def mark_energized(data):
    w, h = data.shape
    energized = np.zeros(shape=(w, h))

    next_position_list = [((0, 0), Dir.RIGHT)]
    for pos, dir in next_position_list:
        # print(Dir.str(dir), pos)
        if validposition(pos, w, h):
            symbol = data[pos[0]][pos[1]]
            energized[pos[0]][pos[1]] += 1
            if energized[pos[0]][pos[1]] > 1000:
                continue

            if symbol == '.':
                next_position_list.append((Dir.move(pos, dir), dir))
            elif symbol == '|':
                if dir == Dir.LEFT or dir == Dir.RIGHT:
                    next_position_list.append((Dir.move(pos, Dir.DOWN), Dir.DOWN))
                    next_position_list.append((Dir.move(pos, Dir.UP), Dir.UP))
                else:
                    next_position_list.append((Dir.move(pos, dir), dir))
            elif symbol == '-':
                if dir == Dir.UP or dir == Dir.DOWN:
                    next_position_list.append((Dir.move(pos, Dir.LEFT), Dir.LEFT))
                    next_position_list.append((Dir.move(pos, Dir.RIGHT), Dir.RIGHT))
                else:
                    next_position_list.append((Dir.move(pos, dir), dir))
            elif symbol == '/':
                if dir == Dir.UP:
                    next_position_list.append((Dir.move(pos, Dir.RIGHT), Dir.RIGHT))
                elif dir == Dir.DOWN:
                    next_position_list.append((Dir.move(pos, Dir.LEFT), Dir.LEFT))
                elif dir == Dir.LEFT:
                    next_position_list.append((Dir.move(pos, Dir.DOWN), Dir.DOWN))
                elif dir == Dir.RIGHT:
                    next_position_list.append((Dir.move(pos, Dir.UP), Dir.UP))
                else:
                    raise
            elif symbol == '\\':
                if dir == Dir.DOWN:
                    next_position_list.append((Dir.move(pos, Dir.RIGHT), Dir.RIGHT))
                elif dir == Dir.UP:
                    next_position_list.append((Dir.move(pos, Dir.LEFT), Dir.LEFT))
                elif dir == Dir.LEFT:
                    next_position_list.append((Dir.move(pos, Dir.UP), Dir.UP))
                elif dir == Dir.RIGHT:
                    next_position_list.append((Dir.move(pos, Dir.DOWN), Dir.DOWN))
                else:
                    raise
            else:
                raise
    return energized

def validposition(p, width, height):
    return (0 <= p[1] < width) and (0 <= p[0] < height)


if __name__ == '__main__':
    assert solution("input16.sample.txt") == 46
    filename = sys.argv[1]
    res = solution(filename)

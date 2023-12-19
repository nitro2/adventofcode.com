import sys
import re

def solution(lines):
    # print(lines)

    # Format: 
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    #  game  - subsets
    # index  - 
    r = re.compile('Game (\d+):(.*)')
    result = 0
    for line in lines:
        game, subsets = line.split(':')
        index = game.split()[1]
        d = dict({'red':0, 'green':0, 'blue':0})
        for s in subsets.split(';'):
            # print(s)
            for c in s.split(','):
                cubes = c.split()
                # print(cubes)
                value = cubes[0]
                color = cubes[1] 
                d[color] = max(int(value), d[color])
        
        # Verify if subsets satisfy the request
        # the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
        result += d['green']*d['red']*d['blue']

        print(index, d)
    
    print("Final result:", result)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as fi:
        print(solution(fi.readlines()))
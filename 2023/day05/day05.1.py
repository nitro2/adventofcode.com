import sys
import re


def solution(filenaem):
    with open(filename, "r") as fi:
        data = fi.read()
        # print(data)
        blocks = re.split(r'\n\n', data)
        # print(blocks)

        # seeds
        seeds = blocks[0].strip().split(':')[1].split()
        print("seeds", seeds)

        # Sample of # seed-to-soil map:
        # s = blocks[1].strip().split(':')[1].strip()
        # seed2soil = [x.split() for x in s.split('\n')]
        # print("seed2soil", seed2soil)

        # create thoudsands thoudsands of maps:
        maps = []
        for b in blocks[1:]:
            m = b.strip().split(':')[1].strip()
            a2b = [x.split() for x in m.split('\n')]
            # print(a2b)
            maps.append(a2b)
        print(maps)

        res = sys.maxsize
        # Loop through the seeds:
        for s in seeds:
            v = int(s) # input thing to search in map
            # maps contains: seed-to-soil, soil-to-fertilizer, fertilizer-to-water, etc.
            for m in maps:
                for line in m:
                    dest, source, len = [int(x) for x in line] # eg: 50 98 2
                    if source <= v < source + len:
                        v = dest + (v-source)
                        break # stop searching here
            res = min(res, v)

        return res



if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

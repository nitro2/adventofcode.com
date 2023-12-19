import sys
import re


def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read()
        # print(data)
        blocks = re.split(r'\n\n', data)
        # print(blocks)

        # seeds
        seeds_range = blocks[0].strip().split(':')[1].split()
        seeds_range = [eval(i) for i in seeds_range]
        print("seeds", seeds_range)

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
        # print(maps)

        res = sys.maxsize

        # Build a FIFO seed list:
        process_list = []
        for i in range(0,len(seeds_range)-1,2):
            process_list.append((int(seeds_range[i]),int(seeds_range[i+1])))


        # input:
        #  + seed pair list
        #  + map i
        # output seed pair list

        # maps contains: seed-to-soil, soil-to-fertilizer, fertilizer-to-water, etc.
        for m in maps:
            # print("process_list", process_list)
            process_list = seed_to_soil(m, process_list)
            # print("output_list", process_list)
        return min(map(lambda x:x[0], process_list))


def seed_to_soil(m, process_list):
    output_list = []
    for p in process_list:
        # print("Process",p)
        ov = v = p[0]
        ol = l = p[1]

        for line in m:
            dest, source, length = [int(x) for x in line] # eg: 50 98 2
            if source <= v < source + length:
                ov = dest + (v-source)
                if v+l > source+length :
                    # append undefined seed to next list
                    process_list.append((v+(source+length-v), l-(source+length-v)))
                    ol = length - (v - source)
                    break
        output_list.append((ov,ol))
    return output_list


if __name__ == '__main__':
    filename = sys.argv[1]
    # filename = '/Users/nngo/Projects/Dreamer/adventofcode.com/2023/day05/input05.sample.short.txt'
    print("Result:", solution(filename))


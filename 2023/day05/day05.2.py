import sys
import re


def solution(filenaem):
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
        # for m in maps:
        #     process_list = seed_to_soil(m, process_list)
  
        return min(process_list[::2])


def seed_to_soil(m, process_list):
    output_list = []
    for p in process_list:
        v = p[0]
        l = p[1]
        for line in m:
            dest, source, length = [int(x) for x in line] # eg: 50 98 2
            if source <= v < source + length:
                            v = dest + (v-source)
                            if v+l > source+length :
                                # append undefined seed to next list
                                process_list.append((v, l-(source+length-v)))
                                l = length - (v - source)
                            break # stop searching here
    return output_list

def union_difference(ir, cr):
    max(ir[0])

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

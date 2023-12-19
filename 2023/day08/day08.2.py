import sys
import re
from math import lcm

def parse_node(str):
    s = re.match(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)", str)
    return {s.group(1): (s.group(2), s.group(3))}

def solution(filename):
    with open(filename, "r") as fi:
        data = fi.readlines()
        instruction = data[0].rstrip()
        node_list = dict()
        for line in data[2:]:
            node_list.update(parse_node(line))
        
        print("instruction", instruction)

        # Get all node ending 'A'
        start_point = [k for k,v in node_list.items() if k.endswith('A')]

        ghost_run_list = []
        for s in start_point:
            count = 0
            node = s
            while not node.endswith('Z'):
                for ins in instruction:
                    next_node = node_list[node][0] if ins == 'L' else node_list[node][1]
                    # print("node={} ins={} next_node={}".format(node, ins, next_node))
                    count +=1
                    print(next_node)
                    node = next_node
                    if node.endswith('Z'):
                        break
            ghost_run_list.append(count)

        # Final result is the least common multiple
        return lcm(*ghost_run_list)

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

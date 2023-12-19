import sys
import re


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
        node = 'AAA'
        count = 0
        while node != 'ZZZ':
            for ins in instruction:
                next_node = node_list[node][0] if ins == 'L' else node_list[node][1]
                print("node={} ins={} next_node={}".format(node, ins, next_node))
                count +=1
                print(next_node)
                node = next_node
                if node == 'ZZZ':
                    break

        return count

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

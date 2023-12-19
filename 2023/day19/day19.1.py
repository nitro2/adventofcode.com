import sys
import re


def printarr(data):
    for d in data:
        print("".join(d))


def solution(filename):
    with open(filename, "r") as fi:
        result = 0
        workflows_str, parts_str = fi.read().rstrip().split('\n\n')
        workflows_str = workflows_str.splitlines()
        parts_str = parts_str.splitlines()
        # print(workflows_str)
        # print(parts_str)

        workflows = create_workflows(workflows_str)
        part_list = create_parts(parts_str)
        result = process_rules(part_list, workflows)

        print("Result:", result)
        return result


'''
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
'''


def create_workflows(workflows_str):
    workflows = {}
    for w in workflows_str:
        r = re.search(r"(\w+)\{(.*)\}", w)
        workname = r.group(1)  # workname = px
        flow = r.group(2)     # flow = a<2006:qkq,m>2090:A,rfg
        print(workname)
        print(flow)
        workflows[workname] = flow
    print("workflows", workflows)
    return workflows


def create_parts(parts_str):
    outpart_list = []
    for part in parts_str:
        # p = {x=787,m=2655,a=1222,s=2876}
        d = dict()
        # print(part[1:-1])
        for p in part[1:-1].split(','):
            r = re.search(r"(\w)(\=)(\d+)", p)
            k = r.group(1)
            v = int(r.group(3))
            d[k] = v
        outpart_list.append(d)
    print("outpart_list", outpart_list)  # {x:787, m:2655, a:1222, s:2876}
    return outpart_list


def process_rules(part_list, workflows):
    total = 0
    for part in part_list:
        out = rule(part, workflows['in'])
        while out != 'A' and out != 'R':
            out = rule(part, workflows[out])
        if out == 'A':
            total += sum([v for _, v in part.items()])
    print("total", total)
    return total


'''
flow = a<2006:qkq,m>2090:A,rfg
'''


def rule(part, flow):
    rules_str = flow.split(',')
    next_dest = rules_str[-1]
    for r in rules_str[:-1]:
        # r = a<2006:qkq
        condition, out = r.split(':')
        p = condition[0]  # p = a
        op = condition[1]  # op = <
        num = int(condition[2:])
        v = part[p]
        # eval the "v op num"
        if op == '<' and v < num:
            return out
        if op == '>' and v > num:
            return out
    return next_dest


if __name__ == '__main__':
    assert solution("input19.sample.txt") == 19114
    assert solution("input19.txt") == 353046
    
    # filename = sys.argv[1]
    # res = solution(filename)

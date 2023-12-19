import copy
import sys
import re


def printarr(data):
    for d in data:
        print("".join(d))


def part1(filename):
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
        # print(workname)
        # print(flow)
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


# ===============================PART 2=========================================================


def part2(filename):
    with open(filename, "r") as fi:
        result = 0
        workflows_str, *parts_str = fi.read().rstrip().split('\n\n')
        workflows_str = workflows_str.splitlines()

        workflows = create_workflows(workflows_str)
        result = combinations_accept(workflows)

        print("Result:", result)
        return result


def combinations_accept(workflows):
    valid_parts = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    return cal_combine(workflows, 'in', valid_parts)


def cal_combine(workflows, in_flow, valid_parts):
    if in_flow == 'R':
        return 0
    # if check_invalid_range(valid_parts): return 0
    if in_flow == 'A':
        return cal_accepts(valid_parts)
    flow = workflows[in_flow]
    rules_str = flow.split(',')
    next_dest = rules_str[-1]
    total = 0
    for r in rules_str[:-1]:
        # r = a<2006:qkq
        condition, out = r.split(':')
        p = condition[0]  # p = a
        op = condition[1]  # op <
        num = int(condition[2:])
        v = valid_parts[p]

        valid_range, invalid_range = new_range(v, op, num)
        remain_parts = copy.deepcopy(valid_parts)
        remain_parts[p] = valid_range

        total += cal_combine(workflows, out, remain_parts)

        if invalid_range == (0, 0):
            break
        valid_parts[p] = invalid_range
    print("subtotal", total, "flow", flow)
    return total + cal_combine(workflows, next_dest, valid_parts)


def new_range(v, op, num):
    # v(2000,3000) <2006
    valid_range = (0,0)
    invalid_range = v

    # eval the "v op num"
    # v = (2000, 3000), op <
    # num = 1000 -> Not accept, process next rule -> valid_range = (0,0),          invalid_range = v
    # num = 2500 -> accept a part                 -> valid_range = (2000, 2500-1)  invalid_range = (2500, 3000)
    # num = 3500 -> accept all, u = (2000, 3000)  -> valid_range = v               invalid_range = (0, 0)
    if op == '<' and v[0] < num:
        valid_range = (v[0], min(num-1, v[1]))
        if num <= v[1]:
            invalid_range = (num, v[1])
        else:
            invalid_range = (0,0)


    # v = (2000, 3000), op >
    # num = 1000 -> accept all, u = (2000, 3000)  -> valid_range = v               invalid_range = (0, 0)
    # num = 2500 -> accept a part                 -> valid_range = (2500+1, 3000)  invalid_range = (2500, 3000)
    # num = 3500 -> Not accept, process next rule -> valid_range = (0,0)           invalid_range = v
    if op == '>' and v[1] > num:
        valid_range = (max(num+1, v[0]), v[1])
        if v[0] <= num:
            invalid_range = (v[0], num)
        else:
            invalid_range = (0,0)

    print(valid_range, invalid_range)

    return valid_range, invalid_range


def cal_accepts(valid_parts):
    total = 1
    for _, v in valid_parts.items():
        total *= v[1]-v[0]+1
    return total


if __name__ == '__main__':
    # assert part1("input19.sample.txt") == 19114
    # assert part1("input19.txt") == 353046
    assert ((2000, 2500-1), (2500,3000)) == (new_range((2000,3000), '<', 2500))
    assert ((0, 0), (2000,3000)) == new_range((2000,3000), '<', 1000)
    assert ((2000,3000), (0, 0)) == new_range((2000,3000), '<', 3500)
    
    assert ((2500+1, 3000), (2000,2500)) == new_range((2000,3000), '>', 2500)
    assert ((2000,3000), (0, 0)) == new_range((2000,3000), '>', 1000)
    assert ((0, 0), (2000,3000)) == new_range((2000,3000), '>', 3500)

    assert ((1,1349), (1350, 4000)) == new_range((1,4000), '<', 1350)
    assert ((1351,4000), (1, 1350)) == new_range((1,4000), '>', 1350)
    assert ((0, 0), (2000,3000)) == new_range((2000,3000), '>', 3000)
    assert ((2001,3000), (2000,2000)) == new_range((2000,3000), '>', 2000)
    assert ((3000,3000), (2000,2999)) == new_range((2000,3000), '>', 2999)

    

    assert part2("input19.sample.2.txt") == 140192430000000
    assert part2("input19.sample.txt") == 167409079868000
    assert part2("input19.txt") == 125355665599537
    # 256000000000000
    # 167409079868000

    # filename = sys.argv[1]
    # res = part1(filename)

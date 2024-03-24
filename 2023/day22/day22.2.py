import sys
import heapq

class Point:
    def __init__(self, instring):
        self.x , self.y, self.z = tuple(map(int, instring.split(',')))
    
    def __str__(self) -> str:
        return ",".join(map(str,(self.x , self.y, self.z)))

class Segment:
    def __init__(self, P1, P2):
        self.P1 = P1
        self.P2 = P2

def intersect(s0,s1):
    dx0 = s0.P2.x-s0.P1.x
    dx1 = s1.P2.x-s1.P1.x
    dy0 = s0.P2.y-s0.P1.y
    dy1 = s1.P2.y-s1.P1.y
    p0 = dy1*(s1.P2.x-s0.P1.x) - dx1*(s1.P2.y-s0.P1.y)
    p1 = dy1*(s1.P2.x-s0.P2.x) - dx1*(s1.P2.y-s0.P2.y)
    p2 = dy0*(s0.P2.x-s1.P1.x) - dx0*(s0.P2.y-s1.P1.y)
    p3 = dy0*(s0.P2.x-s1.P2.x) - dx0*(s0.P2.y-s1.P2.y)
    return (p0*p1<=0) & (p2*p3<=0)

class Brick:
    def __init__(self, indata, index):
        self.name = 'B' + str(index) # + indata
        # [[x1,y1,z1],[x2,y2,z2]]
        P1, P2 = indata.split('~')
        self.pos = Segment(Point(P1), Point(P2))
        # print(self.pos)
        self.fallingz = min(self.pos.P1.z, self.pos.P2.z)
        self.supporting = set()
        self.supported = set()
        self.disintegrable = False
        self.total_supporting_set = set()
    
    def __str__(self):
        return self.name

    def dropped_position(self, dropped):
        high = self.pos.P2.z - self.pos.P1.z
        self.pos.P1.z = dropped
        self.pos.P2.z = self.pos.P1.z + high

    def intersect_xy(self, anotherbrick):
        if intersect(self.pos, anotherbrick.pos):
            return self.fallingz
        else:
            return 0
    
    def set_supporting(self, bname):
        self.supporting.add(bname)

    def set_supported(self, bname):
        self.supported.add(bname)

    def set_disintegrable(self, flg):
        self.disintegrable = flg

    def set_total_supporting_set(self, bricks):
        for s in self.supporting:
            if bricks[s].disintegrable:
                self.total_supporting_set |= bricks[s].total_supporting_set
            self.total_supporting_set.add(s)

def print_bricks(bricks):
    for k, v in bricks.items():
        print(k, v.pos.P1, v.pos.P2)

def part1(filename):
    print("="*100)
    with open(filename, "r") as fi:
        result = 0
        data = fi.read().rstrip().split('\n')
        
        bricks = dict()
        for i, d in enumerate(data):
            b = Brick(d, i)
            bricks[b.name] = b

        # Create an falling_list order list of brick by its pos_z
        falling_list, highest_stack = get_falling_list(bricks)
        print("highest_stack", highest_stack)
        # Scan from ground to top by z direction, give output layers is the order of bricks
        # after the drop to ground
        layers = get_layers(falling_list, bricks, highest_stack)
        # Scan the ground_list to find which Brick can be disintegrated
        # print("layers", layers)
        result = count_disintegrated(layers, bricks)

        print("Result:", result)
        return result

# [(z, 'B0), ...]
def get_falling_list(bricks):
    falling_list = []
    highest_stack = 0
    for _, b in bricks.items():
        heapq.heappush(falling_list, (b.fallingz, b.name))
        highest_stack = max(highest_stack, b.pos.P2.z)
    print(falling_list) # [(1, 'B0'), (3, 'B2'), (2, 'B1'), (5, 'B4'), (8, 'B6'), (6, 'B5'), (4, 'B3')]
    return falling_list, highest_stack

# We have a dict of z layers:
# Layer1 : {B1, B2}
# Layer2 : {B2, B4}
# So a falling brick has to scan if it stucks on any layer.
def get_layers(falling_list, bricks, highest_stack):
    layers = [None]*(highest_stack*3) # TODO fixme
    while len(falling_list)>0:
        z, name = heapq.heappop(falling_list)
        b = bricks[name]
        dropped = get_stuck_layer(layers, bricks, name)
        # Add brick to layer[i]
        for i in range(b.pos.P1.z, b.pos.P2.z+1):
            print('i', i, name)
            if layers[i] is not None:
                layers[i].add(name)
            else:
                layers[i] = {name}
    # print_bricks(bricks)
    # TODO: Remove None layer

    return layers

def get_stuck_layer(layers, bricks, name):
    b = bricks[name]
    for i in range(len(layers)-1,0, -1):
        if layers[i] is not None:
            isstuck = False
            for o in layers[i]:
                if b.intersect_xy(bricks[o]):
                    # update supporting/supported
                    b.set_supported(bricks[o].name)
                    bricks[o].set_supporting(name)
                    b.dropped_position(i+1)
                    isstuck = True
            if isstuck:
                return i+1
    b.dropped_position(1)
    return 1 # Ground layer.


def count_disintegrated(layers, bricks):
    disintegrated = set()
    for l in layers:
        if l is not None:
            for name in l:
                if len(bricks[name].supporting) == 0:
                    disintegrated.add(name)
                else: # >0
                    disintegrable = True
                    for s in bricks[name].supporting:
                        if len(bricks[s].supported) <2:
                            disintegrable = False
                            break
                    if disintegrable:
                        disintegrated.add(name)
    print("disintegrated", disintegrated)
    return len(disintegrated)

#============= PART 2

def get_cant_disintegrated(layers, bricks):
    disintegrated = set()
    cant_disintegrated = set()
    total_bricks = 0
    for i, l in enumerate(layers[::-1]):
        if l is not None:
            for name in l:
                if len(bricks[name].supporting) == 0:
                    disintegrated.add(name)
                else: # >0
                    disintegrable = True
                    for s in bricks[name].supporting:
                        if len(bricks[s].supported) <2:
                            disintegrable = False
                            break
                    if disintegrable:
                        disintegrated.add(name)
                        bricks[name].set_disintegrable(True)
                    else:
                        # cant_disintegrated
                        cant_disintegrated.add(name) 
                        bricks[name].set_disintegrable(False)
                    bricks[name].set_total_supporting_set(bricks)
            total_bricks += len(l)
    print("disintegrated", disintegrated)
    print("cant_disintegrated", cant_disintegrated)
    
    return cant_disintegrated, disintegrated


def part2(filename):
    print("="*100)
    with open(filename, "r") as fi:
        result = 0
        data = fi.read().rstrip().split('\n')
        
        bricks = dict()
        for i, d in enumerate(data):
            b = Brick(d, i)
            bricks[b.name] = b

        # Create an falling_list order list of brick by its pos_z
        falling_list, highest_stack = get_falling_list(bricks)
        print("highest_stack", highest_stack)
        # Scan from ground to top by z direction, give output layers is the order of bricks
        # after the drop to ground
        layers = get_layers(falling_list, bricks, highest_stack)
        # Scan the ground_list to find which Brick can be disintegrated
        print("layers", layers)
        cant_disintegrated, disintegrated = get_cant_disintegrated(layers, bricks)

        result = count_cant_disintegrated(bricks, cant_disintegrated)

        print("Result:", result)
        return result
    

def count_cant_disintegrated(bricks, cant_disintegrated):
    print("Final cant_disintegrated")
    totaldict = dict()
    total = 0
    for b in cant_disintegrated:
        print(b, bricks[b].total_supporting_set)
        total += count_total_disintegrated(bricks, cant_disintegrated, totaldict, b)

    return total


def count_total_disintegrated(bricks, cant_disintegrated, totaldict, b):
    if b in totaldict:
        return totaldict[b]
    if not b in cant_disintegrated:
        return 1
    total = 0
    for s in bricks[b].total_supporting_set:
        if not s in cant_disintegrated:
            total += 1
        else:
            total += 1 + count_total_disintegrated(bricks, cant_disintegrated, totaldict, s)
        totaldict[b]=total
    return total


if __name__ == '__main__':
    assert True == intersect(Segment(Point("1,0,1"),Point("1,2,1")), Segment(Point("0,0,2"), Point("2,0,2")))
    # assert part1("input22.sample.1.txt") == 5
    # assert part1("input22.txt") == 465

    assert part2("input22.sample.1.txt") == 7
    assert part2("input22.txt") == 0

    # filename = sys.argv[1]
    # res = part1(filename)

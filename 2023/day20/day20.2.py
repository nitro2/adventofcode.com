import copy
import sys
import re


def printarr(data):
    for d in data:
        print("".join(d))


OFF = False
ON = True
HIGH = True
LOW = False

class Module:
    def __str__(self):
        return "{}.{}.{}.{}".format(list(self.inputlist.keys()), self.__class__.__name__, self.name, self.output)

    def get_output(self):
        return self.output
    
    def create_input(self, inname):
        pass

class Flipflop(Module):
    def __init__(self, name, output):
        self.name = name
        self.state = OFF
        self.output = output
        self.pulse_high = 0
        self.pulse_low = 0
        self.inputlist = dict()

    def create_input(self, inname):
        self.inputlist[inname] = LOW

    def trigger(self, pulse, inname, cycles):
        if pulse == LOW:
            # If it was off, it turns on and sends a high pulse.
            # If it was on, it turns off and sends a low pulse.
            if self.state == OFF:
                self.pulse_high += len(self.output)
                self.state = ON
                return [(self.name, self.state, o) for o in self.output], 0, len(self.output)
            else:
                self.pulse_low += len(self.output)
                self.state = OFF
                return [(self.name, self.state, o) for o in self.output], len(self.output), 0
        return [], 0, 0

    def get_pulsed(self):
        return self.pulse_low, self.pulse_high


class Conjunction(Module):
    def __init__(self, name, output):
        self.name = name
        self.inputlist = dict()
        self.output = output
        self.pulse_high = 0
        self.pulse_low = 0
        self.print = False

    def create_input(self, inname):
        self.inputlist[inname] = LOW

    # Return (i,p,o), low_pulses, high_pulses
    def trigger(self, pulse, inname, cycles):
        self.inputlist[inname] = pulse

        # send LOW if all inputs are HIGH
        # otherwise send HIGH
        if all(self.inputlist.values()) == HIGH:
            # if not self.print:
            #     print("Conjunction {} at cycle {}".format(self.name, cycles))
            #     self.print = True
            self.pulse_low += len(self.output)
            return [(self.name, LOW, o) for o in self.output], len(self.output), 0
        else:
            if not self.print:
                print("Conjunction {} send HIGH at cycle {}".format(self.name, cycles))
                self.print = True
            self.pulse_high += len(self.output)
            return [(self.name, HIGH, o) for o in self.output], 0, len(self.output)


    def get_pulsed(self):
        return self.pulse_low, self.pulse_high


'''

'''


def part1(filename, times=1000):
    print("="*100)
    with open(filename, "r") as fi:
        result = 0
        data = fi.read().rstrip().split('\n')
        modules = dict()
        links = list()  # Store links between modules
        for d in data:
            # print(d)
            inmodule, outmodules = d.split(" -> ")
            print(inmodule, outmodules)
            output = outmodules.rsplit(", ")
            if inmodule == "broadcaster":
                broadcaster = [("broadcaster",LOW,o) for o in output]
                print(broadcaster)
            else:
                sign = inmodule[0]
                name = inmodule[1:]
                if sign == '%':
                    modules[name] = Flipflop(name, output)
                elif sign == '&':
                    modules[name] = Conjunction(name, output)
                else:
                    print("Error", inmodule)
                    raise

        # Create inputs for each module using output list
        for name, module in modules.items():
            for n in module.get_output():
                    if modules.get(n):
                        modules[n].create_input(name)
        
        # Print the structure:
        for name, module in modules.items():
            print(module)


        # print(broadcaster)
        result = press(broadcaster, modules, times)

        print("Result:", result)
        return result


'''
(in,pulse,out)

steps = [(broadcast,LOW,a), (broadcast,LOW,a), (broadcast,LOW,a)]
nextsteps = [(a,HIGH,b), (b,HIGH,c), (c,HIGH,inv)]
'''


def press(broadcaster, modules, times):
    total_low_pulse = 0
    total_high_pulse = 0
    for n in range(times):
        sl = 1 # Button press
        sh = 0
        steps = broadcaster
        sl += len(broadcaster)
        # print("step", n)
        while len(steps) > 0:
            nextsteps = []
            for i,p,o in steps:
                if modules.get(o):
                    out, l, h = modules[o].trigger(p,i, cycles=n+1)
                    # print("process", o, "out=", out)
                    sl += l
                    sh += h
                    nextsteps += out
                    check_rx(out, i)
                else:
                    # print("Not found", o)
                    pass
            steps = nextsteps
        # print("low=",sl, "high=", sh)
        total_low_pulse += sl
        total_high_pulse += sh
    print("times", times, "total_low_pulse", total_low_pulse, "total_high_pulse", total_high_pulse)
    return total_low_pulse*total_high_pulse

def check_rx(out, i):
    for t in out:
        if len(t) > 0 and t[2] == "rx" and t[1] == False:
                        print("Got answer at step", i)
                        raise

def count_pulse(modules):
    sl = 0
    sh = 0
    for _,m  in modules.items():
        l, h = m.get_pulsed()
        sl += l
        sh += h
    return sl, sh


if __name__ == '__main__':
    # assert part1("input20.sample.1.txt", times=1) == 32
    # assert part1("input20.sample.1.txt", times=1000) == 32000000
    # assert part1("input20.sample.2.txt", times=1) == 4*4
    # assert part1("input20.sample.2.txt", times=2) == (4+4)*(4+2)
    # assert part1("input20.sample.2.txt", times=3) ==  (4+4+5)*(4+2+3) 
    # assert part1("input20.sample.2.txt", times=4) ==  (4+4+5+4)*(4+2+3+2)
    # assert part1("input20.sample.2.txt", times=1000) == 11687500
    assert part1("input20.txt", times=100000) == 0
    # assert part1("input20.txt", times=100000000) == 0

    # filename = sys.argv[1]
    # res = part1(filename)

    # 212763526041600 is too low
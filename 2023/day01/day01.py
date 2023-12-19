def day_01_part1(lines):
    result = 0
    for line in lines:
        digits = [c for c in line if '0' <= c <= '9']
        if len(digits) > 0:
            result += int(digits[0] + digits[-1])
    return result


def day_01_part2(lines):
    result = 0
    TEXT_DIGIT = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for line in lines:
        digits = []
        for i, c in enumerate(line):
            if '0' <= c <= '9':
                digits += [c]
            elif (w := line[i:i+3]) in ("one", "two", "six") or \
                (w := line[i:i+4]) in ("four", "five", "nine") or \
                (w := line[i:i+5]) in ("three", "seven", "eight"):
                digits += [str(TEXT_DIGIT.index(w))]

        if len(digits) > 0:
            print("{}{}".format(digits[0],digits[-1]))
            result += int(digits[0] + digits[-1])
    return result


if __name__ == '__main__':
    with open("input01.txt", "r") as fi:
        print(day_01_part2(fi.readlines()))
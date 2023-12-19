import sys
import re

def solution(lines):
    # print(lines)

    # Make array
    arr = []
    for line in lines:
        arr.append(list(line))

    # Check condition
    i = 0
    j = 0
    sum = 0
    max_i = len(arr)
    max_j = len(arr[0])-1 # Minus `\n` 
    print(max_i, max_j)
    for row in arr:
        num = 0
        is_near_symbol = False
        j = 0
        for c in row:
            if c.isdigit():
                num = num*10 + int(c)
                if not is_near_symbol:
                    is_near_symbol = check_neighbor_symbol(i, j, arr, max_i, max_j)
            elif num > 0:
                # We got a valid number
                # print(num)
                # Now we need to check if the number is near any symbol
                # Then sum it
                if is_near_symbol:
                    sum += num

                num = 0
                is_near_symbol = False
            j += 1
        i+=1
    return sum

def check_neighbor_symbol(i, j, arr, max_i=10, max_j=10):
    # Check all 8 direction if are there any symbol:
    # (i-1, j-1),  (i-1, j),  (i-1, j+1)
    # (i, j-1)  ,  (i, j)  ,  (i, j+1)
    # (i+1, j-1),  (i+1, j),  (i+1, j+1)
    dir = [(i-1, j-1), (i-1, j),  (i-1, j+1),
           (i, j-1)  ,  (i, j)  ,  (i, j+1),
           (i+1, j-1),  (i+1, j),  (i+1, j+1)]
    for d in dir:
        if 0<= d[0] <  max_i and 0 <= d[1] < max_j:
            if arr[d[0]][d[1]] != '.' and not arr[d[0]][d[1]].isdigit():
                return True
    return False

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as fi:
        print("Result:", solution(fi.readlines()))
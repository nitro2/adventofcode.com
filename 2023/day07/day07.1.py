import sys
from collections import Counter
from functools import cmp_to_key

class Type:
    HIGH_CARD=1
    ONE_PAIR=2
    TWO_PAIR=3
    THREE_KIND=4
    FULL_HOUSE=5
    FOUR_KIND=6
    FIVE_KIND=7




class Hand():
    def __init__(self, str):
        self.str = str
        card, bid = str.split()
        self.card = card
        self.bid = bid

        self.type = self.gettype()
    
    def gettype(self):
        s = Counter(self.card).most_common(5)
        print(s)
        t1 = s[0][1]
        # Five of a kind, where all five cards have the same label: AAAAA
        if t1 == 5:
            return Type.FIVE_KIND
        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        elif t1==4:
            return Type.FOUR_KIND
        elif t1==3:
            t2 = s[1][1]
            # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            if t2==2:
                return Type.FULL_HOUSE
            # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            else:
                return Type.THREE_KIND
        elif t1==2:
            t2 = s[1][1]
            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            if t2==2:
                return Type.TWO_PAIR
            # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
            else:
                return Type.ONE_PAIR
        # High card, where all cards' labels are distinct: 23456
        else:
            return Type.HIGH_CARD
        
    def getcard(self):
        return self.card
    
    def getbid(self):
        return int(self.bid)
    
    def __str__(self):
        return "Type={} Card={} Bid={}".format(self.type, self.card, self.bid)


Strength = {
    'A':14, 'K':13, 'Q':12, 'J':11, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2
}
def compare_string(card1, card2):
    for x,y in zip(card1, card2):
        if x!=y:
            return Strength[x] - Strength[y]
    return 0

def compare_hand(h1, h2):
    type1 = h1.gettype()
    type2 = h2.gettype()
    if type1 == type2:
        return compare_string(h1.getcard(), h2.getcard())
    else:
        return type1 - type2





def solution(filename):
    with open(filename, "r") as fi:
        data = fi.read()
        # print(data)
        hands = data.split('\n')
        # print(hands)
        hand_list = [Hand(h) for h in hands]
        sorted_hand_list = sorted(hand_list, key=cmp_to_key(compare_hand))
        sum = 0
        for i,h in enumerate(sorted_hand_list):
            sum += (i+1)*h.getbid()

        return sum

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

import sys
from collections import Counter
from functools import cmp_to_key

class Type:
    HIGH_CARD=0
    ONE_PAIR=11000
    TWO_PAIR=22110
    THREE_KIND=33300
    FULL_HOUSE=33322
    FOUR_KIND=44440
    FIVE_KIND=55555




class Hand():
    def __init__(self, str):
        self.str = str
        card, bid = str.split()
        self.card = card
        self.bid = bid

        self.type = self.gettype()
    
    def gettype(self):
        c = Counter(self.card)
        jcards =  int(0 if c.get('J') is None else int(c.get('J')))

        # Remove J from Counter to prevent wrong counting it
        if jcards > 0: del c['J']
        if jcards == 5: return Type.FIVE_KIND

        s = c.most_common(5)

        # print(s) # [('3', 2), ('2', 1), ('T', 1), ('K', 1)]
        # print(self.card)
        t1 = s[0][1]
        t2 = int(0 if len(s) <=1 else  s[1][1])
        # print("J", jcards)
        res = Type.HIGH_CARD
        # Five of a kind, where all five cards have the same label: AAAAA
        if t1 == 5:
            return Type.FIVE_KIND
        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        elif t1==4:
            res = Type.FOUR_KIND
        elif t1==3:
            # t2 = s[1][1]
            # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            if t2==2:
                res = Type.FULL_HOUSE
            # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            else:
                res = Type.THREE_KIND
        elif t1==2:
            # t2 = s[1][1]
            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            if t2==2:
                res = Type.TWO_PAIR 
            # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
            else:
                res = Type.ONE_PAIR
        # High card, where all cards' labels are distinct: 23456
        else:
            res = Type.HIGH_CARD
        
        
        # Adjust result:
        if s[0][0] != 'J' and jcards > 0:
            if res == Type.FOUR_KIND: res = Type.FIVE_KIND   # AAAAJ
            elif res == Type.FULL_HOUSE: res = Type.FIVE_KIND # AAAJJ
            elif res == Type.THREE_KIND: 
                if jcards == 1: res = Type.FOUR_KIND # AAAKJ
                else: res = Type.FIVE_KIND # JJAAA
            elif res == Type.TWO_PAIR: res = Type.FULL_HOUSE  # AAKKJ
            elif res == Type.ONE_PAIR: 
                if jcards == 1:
                    res = Type.THREE_KIND  # AAKQJ
                elif jcards == 2:
                    res = Type.FOUR_KIND  # AAKJJ
                elif jcards == 3:
                    res = Type.FIVE_KIND  # AAJJJ
                else:
                    raise "Unreachable code"
            else: # res == Type.HIGH_CARD:
                if jcards == 1:
                    res = Type.ONE_PAIR  # 2345J
                elif jcards == 2:
                    res = Type.THREE_KIND  # 234JJ
                elif jcards == 3:
                    res = Type.FOUR_KIND # 23JJJ
                else: # jcards = 4
                    res = Type.FIVE_KIND # 2JJJJ
        return res

        
    def getcard(self):
        return self.card
    
    def getbid(self):
        return int(self.bid)
    
    def __str__(self):
        # return "Type={} Card={} Bid={}".format(self.type, self.card, self.bid)
        return self.card


Strength = {
    # J is lowest
    'A':14, 'K':13, 'Q':12, 'J':1, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2
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
            print(h)
            sum += (i+1)*h.getbid()

        return sum

if __name__ == '__main__':
    filename = sys.argv[1]
    print("Result:", solution(filename))

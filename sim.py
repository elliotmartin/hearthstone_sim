# 1 - illuminate - look at 3 bottom, put on top
# 2 -  shard - draw 1    
# 3 - thrive - discover spell from deck
# 4 - switcharoo - find is success
# 5,6 - twin/dwing - draw is fail
# 7 - coin
# 8 - discounted switch
# 9 - discounted thrive 
import random
import copy

def do_sim(target_turns):
    turn = 0
    hand, deck, coin = init_sim()
    hand = sim_mull(hand, deck, coin)
    print('starting hand ', hand, 'coin ', coin)
    while turn < target_turns:
        turn += 1
        print('turn: ', turn)
        hand = sim_turn(hand, deck, turn)
    return hand

def init_sim():
    deck = [0] * 20
    deck += [1, 1, 2, 2, 3, 3, 4, 4, 5, 6]
    hand = []
    
    random.shuffle(deck)
    coin = random.choice([True, False])
    return hand, deck, coin

def sim_mull(hand, deck, coin):
    hand, to_toss = get_mull_choices(deck, coin)
    hand = do_mull(hand, to_toss, deck, coin)
    if coin:
        hand.append(7)
    return hand

def sim_turn(hand, deck, turn):
    PLAYED_ILLUM = False
    mana = turn
    hand.append(deck.pop())
    #switch in hand, so do nothing
    print("hand: ", hand)
    if 4 in hand:
        if 1 in hand:
            print('play illum switch in hand')
            hand.remove(1)
            play_illuminate(hand, deck)
        return hand
    if 8 in hand:
        if 1 in hand:
            print('play illum free switch in hand')
            hand.remove(1)
            play_illuminate(hand, deck)
        return hand
    #prioritize free thrive
    if 9 in hand:
        print('play free thrive')
        hand.remove(9)
        play_thrive(hand, deck)
    #then thrive
    if 3 in hand:
        if mana >= 2:
            print('play thrive')
            hand.remove(3)
            mana -= 2
            play_thrive(hand, deck)
    #then illuminate
    if 1 in hand:
        print('play illum')
        hand.remove(1)
        play_illuminate(hand, deck)
        PLAYED_ILLUM = True
    #last cycle shard
    if 2 in hand:
        if mana >= 1:
            if not PLAYED_ILLUM:
                print('cycle shard')
                hand.remove(2)
                mana -= 1
                trade_shard(hand, deck)
    return hand

def play_illuminate(hand, deck):
    options = deck[0:2]
    if 4 in options:
        deck.remove(4)
        deck.append(8)
    if 4 in hand:
        if 1 in options:
            deck.remove(1)
            deck.append(1)
        if 3 in options:
            deck.remove(3)
            deck.append(9)
    else:
        if 3 in options:
            deck.remove(3)
            deck.append(9)
        if 1 in options:
            deck.remove(1)
            deck.append(1)
    if 2 in options:
        deck.remove(2)
        deck.append(2)

#TODO discover % doesnt change with duplicates, so this is slightly inaccurate
def play_thrive(hand, deck):
    deck_copy = copy.deepcopy(deck)
    options = []
    for i in range(2):
        options.append(random.choice(deck_copy))
        random.shuffle(deck_copy)
        deck_copy.remove(options[i])
    if 4 in options:
        deck.remove(4)
        hand.append(4)
    if 4 in hand:
        if 1 in options:
            deck.remove(1)
            hand.append(1)
        if 3 in options:
            deck.remove(3)
            hand.append(3)
    else:
        if 3 in options:
            deck.remove(3)
            hand.append(3)
        if 1 in options:
            deck.remove(1)
            hand.append(1)
    if 2 in options:
        deck.remove(2)
        hand.append(2)



def trade_shard(hand, deck):
    hand.append(deck.pop())
    deck.insert(random.randint(0, len(deck)), 2)

def get_mull_choices(deck, coin):
    toss = []
    if coin:
        hand = [deck.pop(), deck.pop(), deck.pop()]
    else: 
        hand = [deck.pop(), deck.pop(), deck.pop(), deck.pop()]
    if 5 in hand:
        toss.append(5)
    if 6 in hand:
        toss.append(6)
    
    #if we found switch keep everything else
    #if not found switch, toss all but 1,3,4
    if 4 not in hand:
        for o in hand:
            if o not in [1,3,4,5,6]:
                toss.append(o)
    
    for item in toss:
        hand.remove(item)

    return hand, toss


def do_mull(hand, to_toss, deck, coin):
    if coin:
        handsize = 4
    else:
        handsize = 3
    while len(hand) < handsize:
        hand.append(deck.pop())
    deck += to_toss
    random.shuffle(deck)

    return hand

if __name__ == '__main__':
    print('ending hand ', do_sim(6))

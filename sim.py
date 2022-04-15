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

debug = False

def do_sim(target_turns):
    turn = 0
    hand, deck, coin = init_sim()
    hand = sim_mull(hand, deck, coin)
    if debug:
        print('starting hand ', hand, 'coin ', coin)
    while turn < target_turns:
        turn += 1
        if (5 in hand) or (6 in hand):
            return False
        if 8 in hand:
            if deck[-1] in [5, 6]:
                return False
            return True
        if 4 in hand:
            if deck[-1] in [5, 6]:
                return False
            if turn == 3:
                return True
            elif (turn == 2) and (7 in hand):
                return True
        if debug:
            print('turn: ', turn)
        hand = sim_turn(hand, deck, turn)

def init_sim():
    deck = [1, 1, 2, 2, 3, 3, 4, 4, 5, 6]
    deck += [101,102,103,104,105,106,107,108,109,110]
    deck += [101,102,103,104,105,106,107,108,109,110]
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
    if debug:
        print("hand: ", hand)
    if 4 in hand:
        if 1 in hand:
            if debug:
                print('play illum switch in hand')
            hand.remove(1)
            play_illuminate(hand, deck)
        return hand
    if 8 in hand:
        if 1 in hand:
            if debug:
                print('play illum free switch in hand')
            hand.remove(1)
            play_illuminate(hand, deck)
        return hand
    #prioritize free thrive
    if 9 in hand:
        if debug:
            print('play free thrive')
        hand.remove(9)
        play_thrive(hand, deck)
    #then thrive
    if 3 in hand:
        if mana >= 2:
            if debug:
                print('play thrive')
            hand.remove(3)
            mana -= 2
            play_thrive(hand, deck)
    #then illuminate
    if 1 in hand:
        if debug:
            print('play illum')
        hand.remove(1)
        play_illuminate(hand, deck)
        PLAYED_ILLUM = True
    #last cycle shard
    if 2 in hand:
        if mana >= 1:
            if not PLAYED_ILLUM:
                if debug:
                    print('cycle shard')
                hand.remove(2)
                mana -= 1
                trade_shard(hand, deck)
    return hand

def play_illuminate(hand, deck):
    options = deck[0:3]
    if debug:
        print("illum options",options)
    if 4 in options:
        deck.remove(4)
        deck.append(8)
        return
    if 4 in hand:
        if 1 in options:
            deck.remove(1)
            deck.append(1)
            return
        if 3 in options:
            deck.remove(3)
            deck.append(9)
            return
    else:
        if 3 in options:
            deck.remove(3)
            deck.append(9)
            return
        if 1 in options:
            deck.remove(1)
            deck.append(1)
            return
    if 2 in options:
        deck.remove(2)
        deck.append(2)
        return
    filt = lambda x: x not in [5, 6]
    pool = list(set(filter(filt, options)))
    deck.remove(pool[0])
    deck.append(pool[0])

def play_thrive(hand, deck):
    deck_copy = list(set(copy.deepcopy(deck)))
    options = []
    choose = []
    rev = bool(random.getrandbits(1))

    if 5 in deck_copy:
        deck_copy.remove(5)
    if 6 in deck_copy:
        deck_copy.remove(6)

    for i in range(3):
        options.append(random.choice(deck_copy))
        random.shuffle(deck_copy)
        deck_copy.remove(options[i])
    if debug:
        print("thrive options ",options)
    if 4 in options:
        choose.append(4)
    if 4 in hand:
        if 1 in options:
            choose.append(1)
        if 3 in options:
            choose.append(3)
    else:
        if 3 in options:
            choose.append(3)
        if 1 in options:
            choose.append(1)
    if 2 in options:
        choose.append(2)
    else:
        choose.append(options[0])

    card = choose[0]
    idxs = [i for i in range(len(deck)) if deck[i] == card]
    hand.append(deck.pop(random.choice(idxs)))


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
    attempts = 1000000
    success = 0
    for i in range(attempts):
        if do_sim(6):
            success += 1
    print(success/attempts)


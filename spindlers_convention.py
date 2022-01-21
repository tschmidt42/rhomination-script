from copy import deepcopy

L = [[0, 1, 1]]
C = [[1],[1]]
R = [[1, 1]]
# rhombination games are represented with lists
# each element is a triangle and every other triangle is reflected
# so if x and y are both even or both odd board[x][y] is this triangle <|
# if one is even and one is odd board[x][y] is this triangle |>

# copied rhombination code but now we only care who loses 
# and players don't assume rationality of opponents 
# the board code is unchanged but the player logic is significantly altered

cache = {}

outcome_classes = {
    'LLL': 0, 'LLC': 0, 'LCL': 0, 'CLL': 0, 'LCC': 0, 'CLC': 0, 'CCL': 0, 
    'CCC': 0, 'LLR': 0, 'LRL': 0, 'RLL': 0, 'LRR': 0, 'RLR': 0, 'RRL': 0,
    'LCR' : 0, 'LRC': 0, 'CLR': 0, 'RCL': 0, 'RLC': 0, 'CRL': 0, 
    'CCR': 0, 'CRC': 0, 'RCC': 0, 'CRR': 0, 'RCR': 0, 'RRC': 0, 'RRR': 0,
}

ones = [[True, False, True, True, False, False],[True, False, False, False, True, True]]

s = set()

def find_zeros(i):
    games = generate_boards(i, generate_list(i))
    for g in games:
        if outcome_class(g) == "CR, LR, LC":
            s.add(to_tuple(g))
    return s
   
def to_tuple(g):
    tuples = []
    for x in g:
        tuples.append(tuple(x))
    return tuple(tuples)

def to_arr(g):
    arr = []
    for x in g:
        arr.append(list(x))
    return arr

def check_ones(i):
    games = generate_boards(i, generate_list(i))
    x = 0
    for g in games:
        if x % (len(games) / 10) == 0: print("\u2588", end = "")
        outcome1 = outcome_class(g)
        outcome2 = outcome_class(add(g, ones))
        if outcome1 != outcome2:
            print(outcome1, outcome2)
        x += 1
    print("\n")

def check_zero_class(i):
    games = generate_boards(i, generate_list(i))
    # print(games)
    for g in games:
        outcome1 = outcome_class(g)
        for zero in s:
            outcome2 = outcome_class(add(g, to_arr(zero)))
            if outcome1 != outcome2:
                print(outcome1, outcome2)
                print(g)
                print(zero)

def check_square(x, y):
    boards = generate_boards(x, generate_list(y))

    for b in boards:
        outcome = outcome_class(b)
        outcome_classes[outcome] += 1
#        if outcome == 'CLR':
#            print(b)


# --- board generation ---  
def generate_boards(x, lists):
    if (x == 1): return [[l.copy()] for l in lists] 
    boards = generate_boards(x - 1, lists)
    stuff = []
    for b in boards:
        stuff += [deepcopy(b) + [l.copy()] for l in lists]
    return stuff

def generate_list(x):
    if (x == 1): return [[True],[False]]
    lists = generate_list(x - 1)
    stuff = []
    for l in lists:
        stuff.append(l.copy() + [True])
        stuff.append(l.copy() + [False])
    return stuff


# --- game solver ---
outcome_cache = {}
def outcome_class(game):
    key = str(game)
    if key in outcome_cache: 
        return outcome_cache[key] 
    soln = f"{p_outcome(game, 'Left')}, {p_outcome(game, 'Center')}, {p_outcome(game, 'Right')}"
    outcome_cache[key] = soln
    return soln

def p_outcome(game, player):
    l = not "L" in player_play(game, player, 0)
    c = not "C" in player_play(game, player, 1)
    r = not "R" in player_play(game, player, 2)

    winners = ""
    if l: winners = "L"
    if c: winners += "C"
    if r: winners += "R"

    return winners


#0 - left is smart
#1 - center is smart
#2 - right is smart

def left_cond(game, x, y):
    return (x + y & 1 and game[x][y] and game[x][y + 1])

def center_cond(game, x, y):
    return (not x + y & 1) and game[x][y] and game[x + 1][y]

def right_cond(game, x, y):
    return (not x + y & 1) and game[x][y] and game[x][y + 1]

def left_move(game, x, y):
    game[x][y] = 0
    game[x][y + 1] = 0
    return game 

def center_move(game, x, y):
    game[x][y] = 0
    game[x + 1][y] = 0
    return game
             
def right_move(game, x, y):
    game[x][y] = 0
    game[x][y + 1] = 0
    return game

left_letters = "C", "R", "L"

center_letters = "L", "R", "C"

right_letters =  "L", "C", "R"
             
def player_move(player):
    if player == "Left":
        return left_cond, left_move, "Center", left_letters, 0, 1
    elif player == "Center":
        return center_cond, center_move, "Right", center_letters, 1, 0
    else:
        return right_cond, right_move, "Left", right_letters, 0, 1

def call_smart(player, smart):
    if not smart:
        return player == "Left"
    elif smart == 1:
        return player == "Center"
    else:
        return player == "Right"

def player_play(game, player, smart):
    clean(game)
    key = str(game), player, smart
    if key in cache: return cache[key]
    if call_smart(player, smart): 
        return player_smart(game, player, key, smart)
    else: 
        return player_unpredictable(game, player, key, smart)

def player_smart(game, player, key, smart):
    other1 = False
    other2 = False
    me_and_other1 = False
    me_and_other2 = False
    funcs = player_move(player)
    # check result of each possible move and return most favorable one
    l1, l2, l3 = funcs[3]
    for x in range(len(game) - funcs[4]):
        for y in range(len(game[x]) - funcs[5]):
            if funcs[0](game, x, y):
                currgame = deepcopy(game)
                currl = player_play(funcs[1](currgame, x, y), funcs[2], smart)
                if currl == l1 or currl == l1 + l2:
                    other1 = True
                if currl == l2 or currl == l1 + l2:
                    other2 = True
                if l1 in currl and l3 in currl:
                    me_and_other1 = True
                if l2 in currl and l3 in currl: 
                    lr = True
    if other1: 
        if other2: 
            cache[key] = l1 + l2
            return l1 + l2
        else:
            cache[key] = l1
            return l1
    elif other2: 
        cache[key] = l2
        return l2
    elif me_and_other1:
        if me_and_other2:
            cache[key] = "LCR"
            return "LCR"
        else:
            cache[key] = l1 + l3
            return l1 + l3
    elif me_and_other2:
        cache[key] = l2 + l3
        return l2 + l3
    else: 
        cache[key] = l3
        return l3

def player_unpredictable(game, player, key, smart):
    l_loss = False
    c_loss = False
    r_loss = False
    funcs = player_move(player)
    for x in range(len(game) - funcs[4]):
        for y in range(len(game[x]) - funcs[5]):
            if funcs[0](game, x, y):
                currgame = deepcopy(game)
                currl = player_play(funcs[1](currgame, x, y), funcs[2], smart)
                for letter in currl:
                    if letter == "L": l_loss = True
                    elif letter == "C": c_loss = True
                    elif letter == "R": r_loss = True
    losers = ""
    if l_loss:
        losers = losers + "L"
    if c_loss:
        losers = losers + "C"
    if r_loss:
        losers = losers + "R"
    if losers == "": 
        losers = player[0] 
    cache[key] = losers
    return losers


# --- game addition ---
def add(b1, b2):
    if len(b1) == 0: return b2
    if len(b2) == 0: return b1
    if len(b1[0]) < len(b2[0]): return add(b2, b1)

    column = [False] * (len(b1[0]) + (len(b1[0]) == len(b2[0])))
    board = [column.copy() for _ in range(len(b1) + len(b2) + 1)]
 
    for x in range(len(b1)):
        for y in range(len(b1[x])):
            board[x][y] = b1[x][y]
    
    mod1 = len(b1) + 1
    mod2 = not len(b1) & 1
    for x in range(len(b2)):
        for y in range(len(b2[x])):
            board[x + mod1][y + mod2] 
            b2[x][y]
            board[x + mod1][y + mod2] = b2[x][y]
      
    return board


# --- board cleaning functions ---
def clean(b):
    if not len(b) or not len(b[0]): return b
    cull_islands(b)
    # remove all empty far right columns 
    while len(b) > 0 and all(tri == 0 for tri in b[len(b) - 1]):
        b.pop(len(b) - 1)
    # remove all pairs of far left columns (parity matters)
    while len(b) > 1 and all(tri == 0 for tri in b[0]) and all(tri == 0 for tri in b[1]):
        b.pop(0)
        b.pop(0)
    # lower row
    while len(b) > 0 and len(b[0]) > 0 and all(row[len(row) - 1] == 0 for row in b):
        for row in b:
          row.pop(len(row) - 1)
    # upper row
    while len(b) > 0 and len(b[0]) > 1 and all(row[0] == 0 and row[1] == 0 for row in b):
        for row in b:
          row.pop(0)
          row.pop(0)

# remove any isolated trianges that can't be used
def cull_islands(b):
    for x in range(len(b)):
      for y in range(len(b[x])):
          if b[x][y] and (y == 0 or not b[x][y-1]) and (y == len(b[x]) - 1 or not b[x][y+1]):
              if (x + y) % 2 == 0:
                  if x == len(b) - 1 or not b[x + 1][y]: b[x][y] = False
              else:
                  if x == 0 or not b[x - 1][y]: b[x][y] = False

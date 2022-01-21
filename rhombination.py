from copy import deepcopy

# Rhomination games are represented with lists, each element is a triangle 
# and every other triangle is reflected. So if x and y are both even or both
# odd board[x][y] is this triangle <| or if one is even and one is odd 
# board[x][y] is this triangle |>

outcome_classes = {
    'LLL': 0, 'LLC': 0, 'LCL': 0, 'CLL': 0, 'LCC': 0, 'CLC': 0, 'CCL': 0, 
    'CCC': 0, 'LLR': 0, 'LRL': 0, 'RLL': 0, 'LRR': 0, 'RLR': 0, 'RRL': 0,
    'LCR' : 0, 'LRC': 0, 'CLR': 0, 'RCL': 0, 'RLC': 0, 'CRL': 0, 
    'CCR': 0, 'CRC': 0, 'RCC': 0, 'CRR': 0, 'RCR': 0, 'RRC': 0, 'RRR': 0,
}

# Check if [[1, 0, 1, 1, 0, 0],[1, 0, 0, 0, 1, 1]] is the identity
def check_ones(i):
    ones = [[1, 0, 1, 1, 0, 0],[1, 0, 0, 0, 1, 1]]
    games = generate_boards(i, generate_list(i))
    for g in games:
        outcome1 = outcome_class(g)
        outcome2 = outcome_class(add(g, ones))
        if outcome1 != outcome2:
            print(g)
            print(outcome1, outcome2)

# Add outcome classes to outcome class dictionary for games in an x by y grid
def check_square(x, y):
    boards = generate_boards(x, generate_list(y))

    for b in boards:
        outcome = outcome_class(b)
        outcome_classes[outcome] += 1
#        if outcome == 'CLR':
#            print(b)


# Create all grids made of x lists from lists
def generate_boards(x, lists):
    if (x == 1): return [[l.copy()] for l in lists] 
    boards = generate_boards(x - 1, lists)
    stuff = []
    for b in boards:
        stuff += [deepcopy(b) + [l.copy()] for l in lists]
    return stuff

# Generate all lists of length x (1 means there is a free triangle)
def generate_list(x):
    if (x == 1): return [[1],[0]]
    lists = generate_list(x - 1)
    stuff = []
    for l in lists:
        stuff.append(l.copy() + [1])
        stuff.append(l.copy() + [0])
    return stuff


# Get the outcome class for a given grid
def outcome_class(game):
    outcome = left(game) + center(game) + right(game)
    return outcome

# left's move
def left(game):
    # check if game in in left's dictionary
    clean(game)
    key = str(game)
    if key in l: return l[key]

    posw = ''
    # check result of each possible move and return most favorable one
    for x in range(len(game)):
        for y in range(len(game[x]) - 1):
            if (x + y & 1 and game[x][y] and game[x][y + 1]):
                currgame = deepcopy(game)
                currgame[x][y] = 0
                currgame[x][y + 1] = 0
                currw = center(currgame)
                if currw == 'L':
                    l[key] = 'L'
                    return 'L'
                if currw == 'C':
                    posw = 'C'
    if posw == 'C': 
        l[key] = 'C'
        return 'C'
    else: 
        l[key] = 'R'
        return 'R'

# center's move
def center(game):
    clean(game)
    key = str(game)
    if key in c: return c[key]

    posw = ''
    for x in range(len(game) - 1):
        for y in range(len(game[x])):
            if (not x + y & 1) and game[x][y] and game[x + 1][y]:
                currgame = deepcopy(game)
                currgame[x][y] = 0
                currgame[x + 1][y] = 0
                currw = right(currgame)
                if currw == 'C':
                    c[key] = 'C'
                    return 'C'
                if currw == 'R':
                    posw = 'R'
    if posw == 'R': 
        c[key] = 'R'
        return 'R'
    else: 
        c[key] = 'L'
        return 'L'

# right's move 
def right(game):
    posw = ''
    for x in range(len(game)):
        for y in range(len(game[x]) - 1):
            if (not x + y & 1) and game[x][y] and game[x][y + 1]:
                currgame = deepcopy(game)
                currgame[x][y] = 0
                currgame[x][y + 1] = 0
                currw = left(currgame)
                if currw == 'R':
                    return 'R'
                if currw == 'L':
                    posw = 'L'
    if posw == 'L': 
        return 'L'
    else: 
        return 'C'


# Adds two grids (addition in this context means any given player can move on either grid 
# if some such move is avalible and there are no moves on both grids)
def add(b1, b2):
    if b1 == []: return b2
    if b2 == []: return b1
    if len(b1[0]) < len(b2[0]): return add(b2, b1)

    column = [0] * (len(b1[0]) + (len(b1[0]) == len(b2[0])))
    board = [column.copy() for _ in range(len(b1) + len(b2) + 1)]
 
    for x in range(len(b1)):
        for y in range(len(b1[x])):
            board[x][y] = b1[x][y]
    
    mod1 = len(b1) + 1
    mod2 = not len(b1) & 1
    for x in range(len(b2)):
        for y in range(len(b2[x])):
            board[x + mod1][y + mod2] = b2[x][y]
      
    return board


# Addition sometimes creates big messy boards, this function trims off
# big chunks of empty space that aren't needed
def clean(b):
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

# Remove any isolated trianges that can't be used
def cull_islands(b):
    for x in range(len(b)):
      for y in range(len(b[x])):
          if b[x][y] and (y == 0 or not b[x][y-1]) and (y == len(b[x]) - 1 or not b[x][y+1]):
              if (x + y) % 2 == 0:
                  if x == len(b) - 1 or not b[x + 1][y]: b[x][y] = 0
              else:
                  if x == 0 or not b[x - 1][y]: b[x][y] = 0

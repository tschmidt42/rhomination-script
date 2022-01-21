# Rhomination tests

I originally this script for an [IGL project on Surreal Numbers](https://math.illinois.edu/research/igl/projects?field_project_semester_value=Summer&field_project_year_value=2019)
in 2019. These scripts were used to look for counter examples to conjectures we had.

## Rhomination

Rhomination is a three player mathematical game played on a grid of equilateral triangles. The three players, Left (L), Center (C), and Right (R), 
take turns placing rhombus tiles that cover two triangles exactly. Each player has a different predetermined orientation of that rhombus. On their 
turn Each player either places a rhombus in such a way that it does not overlap with an already placed rhombus or that player loses. Grids od triangles 
are then put into "outcome classes" which spesfies who wins when ay player goes first, this is notated by XYZ where X is the player who wins when Left plays 
first, Y is the player who wins when Center plays first, and Z is the player who wins when Right goes first.

![Example Rhombination game](/images/rhombination_example.png)

In two player combinatorial games (games without chance and with perfect information) to find the best move you can always assume best play from the opponent. 
This is not the case in three player games, since one player can 'win make' one opponent over the other. Rhombination attempts to resolve this by ranking every 
players result, the player who last places a piece gets 1st place, the player who could not place a piece gets 3rd place, and the remaining player gets 2nd. 

The greene_convention.py script uses the convention in [Katherine Greene's 2017 thesis](https://wakespace.lib.wfu.edu/bitstream/handle/10339/82171/Greene_wfu_0248M_11002.pdf) 
which defined Rhombination in which every player can be assumed to make the move that optimizes their result. Greene concludes her thesis with 4 conjectures, 
3 of which we found counter examples against. For example we can disprove the second conjecture is "There are no Rhombination games in LRC, CLR, or RCL" by running

```python
from greene_convention import *

# computes every game that can be played in a 3 by 5 grid
check_square(3, 5)

# the results of each game were added to this dictionary
print(outcome_classes)
```

which returns ```{'LLL': 2864, 'LLC': 1641, 'LCL': 2117, 'CLL': 406, 'LCC': 1465, 'CLC': 153, 'CCL': 1942, 'CCC': 1541, 'LLR': 2250, 'LRL': 3148, 'RLL': 231, 'LRR': 1734, 'RLR': 1666, 'RRL': 362, 'LCR': 723, 'LRC': 50, 'CLR': 104, 'RCL': 70, 'RLC': 1560, 'CRL': 498, 'CCR': 1209, 'CRC': 262, 'RCC': 1099, 'CRR': 2301, 'RCR': 1312, 'RRC': 124, 'RRR': 1936}```

Showing that every outcome class has more than one game with that result. 

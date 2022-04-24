########################################################
# IMPORTS
########################################################
import othellogame as og
import othelloplayer as op
########################################################
# CODE STARTS HERE
########################################################
print('#################################')
print('# Game with Minimax player as Black and Random player as White')
print('#################################')
p1 = op.MinimaxPlayer(og.BLACK, 4)
p2 = op.RandomPlayer(og.WHITE)
og.play_game(p1, p2)
print('#################################')
print('# Game with Alphabeta player as White and Random player as Black')
print('#################################')
p1 = op.RandomPlayer(og.BLACK)
p2 = op.MinimaxPlayer(og.WHITE, 4)
og.play_game(p1, p2)

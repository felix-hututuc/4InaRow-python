# 4InaRow-python
Connect-four game developed in python using pygame.

The game can be played either against another human player
or against an AI. The AI has three different difficulty levels:

`easy` - computer makes random moves

`medium` - move based on a `negamax with alpha-beta pruning` algorithm with depth 5

`hard` - move using a `minimax with alpha-beta pruning` algorithm with depth 8

### How to use:

`python 4_in_a_row.py <opponent> <no_rows> <no_cols> <first2move>`

`opponent`   -> opponent type: `player` or `computer`

`no_rows`    -> number of rows of the game board

`no_cols`    -> number of rows of the game board

`first2move` -> player to make the first move: `player1`, `player2`, `computer`

## References:

Pascal Pons - "Solving Connect 4: How to build a perfect AI" - http://blog.gamesolver.org/

Keith Galli - "How to Program a Connect 4 AI (implementing the minimax algorithm)" - https://www.youtube.com/watch?v=MMLtza3CZFM

Wikipedia - Minimax :
https://en.wikipedia.org/wiki/Minimax

Wikipedia - Alpha-beta Pruning: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

Wikipedia - Negamax: https://en.wikipedia.org/wiki/Negamax


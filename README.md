# MADN
Mensch ärgere dich nicht

## Run from command line
From parent directory: `python3 -m MADN`

## Use as package

Open python:
```
python3
```
Then import and use interactively:
```
>>> import MADN
>>> MADN.oneGame()
>>> MADN.oneGame(nPl=3, noPrint=False)
```
One can specify a player's tactic with `tak`, which is a list with values corresponding, in order, to the players' tactics. When a player can choose which piece to move, `"k"` means that kicking out others is prioritised. Any other value means the piece furthest ahead is prioritised. Here, players 1 and 2 are 'kickers' and players 3 and 4 are 'runners':
```
>>> MADN.oneGame(nPl=4, noPrint=False, tak=["k", "k", "s", "s"])
```

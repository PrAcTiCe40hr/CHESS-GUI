# Chess GUI

A simple Chess GUI created using Python and PyQt5, featuring a play against the machine mode that uses the Stockfish engine.

## Features

- Interactive chessboard: Allows players to make moves by clicking on a piece and then the square they want to move it to.
- Move history: Shows a list of all moves made during the game.
- Engine configuration: Users can adjust the thinking time and skill level of the Stockfish engine using sliders.
- Game import/export: Users can import games from PGN files and export the current game to a PGN file.
- Game reset: Allows users to start a new game.
- Game status check: Checks for game end conditions (checkmate, stalemate, draw conditions) after each move.

## Requirements

- Python 3.7 or higher
- PyQt5
- python-chess
- Stockfish chess engine

## How to Run

1. Make sure you have installed all the required dependencies. You can install them using pip:

```bash
pip install python-chess PyQt5
```

2. Run the script:

```bash
python main.py
```

# Assignment One - Sudoku Game

A fully functional 9x9 Sudoku game built with Jaclang as part of the Generative AI Course.

## Features

- 9x9 Sudoku grid with pre-filled numbers
- Interactive gameplay
- Complete Sudoku rule validation (row, column, 3x3 box)
- Input validation and error handling
- Win condition detection
- Protection for original puzzle numbers

## How to Play

1. Run the game: `jac run src/sudoku_game.jac`
2. Enter moves in the format: `row column number`
   - Example: `0 2 8` places number 8 at row 0, column 2
3. Follow Sudoku rules:
   - Each row must contain numbers 1-9 without repetition
   - Each column must contain numbers 1-9 without repetition
   - Each 3x3 box must contain numbers 1-9 without repetition
4. Type `quit` to exit the game

## Requirements

- Python 3.7+
- Jaclang 0.8.7+



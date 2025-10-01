walker main {
    with entry {
        # 9x9 Sudoku grid
        grid = [
            [3,4,0,9,0,5,7,0,1],
            [9,0,1,0,5,0,0,0,0],
            [0,1,0,5,0,0,0,0,0],
            [0,0,7,0,0,3,9,0,0],
            [4,6,9,0,0,2,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ];
        
        # Track original numbers (can't be changed)
        original = [
            [3,4,0,9,0,5,7,0,1],
            [9,0,1,0,5,0,0,0,0],
            [0,1,0,5,0,0,0,0,0],
            [0,0,7,0,0,3,9,0,0],
            [4,6,9,0,0,2,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ];
        
        print('🎯 9x9 SUDOKU GAME 🎯');
        print('=====================');
        print('Enter moves as: row column number');
        print('Example: 0 2 8 to place 8 at top-left');
        print('Type \"quit\" to exit');
        print('');
        
        game_active = 1;
        while game_active == 1 {
            # Display current board
            print('Current board:');
            for i in range(0, 9) {
                line = '';
                for j in range(0, 9) {
                    if grid[i][j] == 0 {
                        line += '. ';
                    } else {
                        line += str(grid[i][j]) + ' ';
                    }
                }
                print(line);
            }
            
            print('');
            user_input = input('Enter your move (row col num): ');
            
            if user_input == 'quit' {
                print('Thanks for playing!');
                game_active = 0;
                continue;
            }
            
            # Parse input
            parts = user_input.split(' ');
            if len(parts) != 3 {
                print('❌ Invalid input! Use: row col number');
                continue;
            }
            
            row = parts[0].to_int();
            col = parts[1].to_int();
            num = parts[2].to_int();
            
            # Validate input range
            if row < 0 or row > 8 or col < 0 or col > 8 or num < 1 or num > 9 {
                print('❌ Invalid values! Use: row(0-8) col(0-8) number(1-9)');
                continue;
            }
            
            # Check if cell is original
            if original[row][col] != 0 {
                print('❌ Cannot change original number!');
                continue;
            }
            
            # Validate Sudoku move
            move_valid = 1;
            
            # Check row
            for j in range(0, 9) {
                if grid[row][j] == num {
                    move_valid = 0;
                }
            }
            
            # Check column
            for i in range(0, 9) {
                if grid[i][col] == num {
                    move_valid = 0;
                }
            }
            
            # Check 3x3 box
            box_row = (row // 3) * 3;
            box_col = (col // 3) * 3;
            for i in range(box_row, box_row + 3) {
                for j in range(box_col, box_col + 3) {
                    if grid[i][j] == num {
                        move_valid = 0;
                    }
                }
            }
            
            if move_valid == 1 {
                grid[row][col] = num;
                print('✅ Move accepted!');
                
                # Check if puzzle is solved
                solved = 1;
                for i in range(0, 9) {
                    for j in range(0, 9) {
                        if grid[i][j] == 0 {
                            solved = 0;
                        }
                    }
                }
                
                if solved == 1 {
                    print('');
                    print('🎉 CONGRATULATIONS! 🎉');
                    print('You solved the Sudoku puzzle!');
                    game_active = 0;
                }
            } else {
                print('❌ Invalid move! Number conflicts with row, column or box.');
            }
            
            print('');
        }
    }
}

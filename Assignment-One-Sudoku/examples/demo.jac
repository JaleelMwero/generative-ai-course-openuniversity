walker main {
    with entry {
        # Demo with validation example
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
        
        print('Sudoku Validation Demo');
        print('=====================');
        
        # Test valid move
        print('Testing: Place 8 at (0,2)');
        valid = 1;
        for j in range(0, 9) {
            if grid[0][j] == 8 { valid = 0; }
        }
        if valid == 1 {
            print('✅ Valid move!');
        } else {
            print('❌ Invalid move!');
        }
    }
}

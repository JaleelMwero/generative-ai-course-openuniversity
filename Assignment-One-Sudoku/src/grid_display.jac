walker main {
    with entry {
        # Simple grid display
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
        
        print('Sudoku Grid Display');
        print('==================');
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
    }
}

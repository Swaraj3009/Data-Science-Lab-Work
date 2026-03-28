import os

class AntiGravityTicTacToe:
    def __init__(self):
        self.rows = 4
        self.cols = 4
        self.grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'
        self.gravity = 'DOWN' # Can be 'DOWN' or 'UP'
        self.winner = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_board(self):
        self.clear_screen()
        print("====== ANTI-GRAVITY TIC TAC TOE ======\n")
        print(f"Current Gravity: {self.gravity}")
        print("-" * 17)
        for r in range(self.rows):
            row_str = " | ".join(self.grid[r])
            print(f"| {row_str} |")
            print("-" * 17)
        print("  0   1   2   3  <-- Column Numbers\n")

    def apply_gravity(self):
        # We process each column independently
        for c in range(self.cols):
            # Extract pieces from this column
            pieces = [self.grid[r][c] for r in range(self.rows) if self.grid[r][c] != ' ']
            
            # Refill the column based on gravity
            if self.gravity == 'DOWN':
                # Empty spaces on top, pieces at the bottom
                empties = self.rows - len(pieces)
                new_col = [' '] * empties + pieces
            else: # UP
                # Pieces at the top, empty spaces at the bottom
                empties = self.rows - len(pieces)
                new_col = pieces + [' '] * empties
            
            for r in range(self.rows):
                self.grid[r][c] = new_col[r]

    def add_piece(self, col):
        if col < 0 or col >= self.cols:
            return False, "Invalid column."
            
        # Check if the column is full (depends on gravity where the "entry" is)
        if self.gravity == 'DOWN':
            if self.grid[0][col] != ' ':
                return False, "Column is full."
            self.grid[0][col] = self.current_player
        elif self.gravity == 'UP':
            if self.grid[self.rows-1][col] != ' ':
                return False, "Column is full."
            self.grid[self.rows-1][col] = self.current_player
            
        self.apply_gravity()
        return True, ""

    def flip_gravity(self):
        if self.gravity == 'DOWN':
            self.gravity = 'UP'
        else:
            self.gravity = 'DOWN'
        self.apply_gravity()

    def check_win(self):
        # Check for 3 in a row
        win_length = 3
        
        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - win_length + 1):
                if self.grid[r][c] != ' ' and all(self.grid[r][c+i] == self.grid[r][c] for i in range(win_length)):
                    return self.grid[r][c]
                    
        # Vertical
        for c in range(self.cols):
            for r in range(self.rows - win_length + 1):
                if self.grid[r][c] != ' ' and all(self.grid[r+i][c] == self.grid[r][c] for i in range(win_length)):
                    return self.grid[r][c]
                    
        # Diagonal (top-left to bottom-right)
        for r in range(self.rows - win_length + 1):
            for c in range(self.cols - win_length + 1):
                if self.grid[r][c] != ' ' and all(self.grid[r+i][c+i] == self.grid[r][c] for i in range(win_length)):
                    return self.grid[r][c]
                    
        # Diagonal (bottom-left to top-right)
        for r in range(win_length - 1, self.rows):
            for c in range(self.cols - win_length + 1):
                if self.grid[r][c] != ' ' and all(self.grid[r-i][c+i] == self.grid[r][c] for i in range(win_length)):
                    return self.grid[r][c]
                    
        # Check for draw (board full)
        is_full = all(self.grid[r][c] != ' ' for r in range(self.rows) for c in range(self.cols))
        if is_full:
            return "DRAW"
            
        return None

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def play(self):
        error_msg = ""
        while not self.winner:
            self.print_board()
            
            if error_msg:
                print(f"!!! {error_msg} !!!\n")
                error_msg = ""
                
            print(f"Player {self.current_player}'s turn.")
            print("1. Drop a piece")
            print("2. Flip Gravity")
            choice = input("Select an action (1 or 2): ").strip()
            
            if choice == '1':
                col_input = input(f"Enter column to drop piece (0-{self.cols - 1}): ").strip()
                if not col_input.isdigit():
                    error_msg = "Please enter a valid number."
                    continue
                col = int(col_input)
                success, msg = self.add_piece(col)
                if not success:
                    error_msg = msg
                    continue
            elif choice == '2':
                self.flip_gravity()
                print("Gravity Flipped!")
            else:
                error_msg = "Invalid choice."
                continue
                
            # After a successful move
            self.winner = self.check_win()
            if not self.winner:
                self.switch_player()
                
        # Game over screen
        self.print_board()
        if self.winner == "DRAW":
            print("GAME OVER! It's a DRAW!")
        else:
            print(f"GAME OVER! Player {self.winner} wins!")


if __name__ == "__main__":
    game = AntiGravityTicTacToe()
    game.play()

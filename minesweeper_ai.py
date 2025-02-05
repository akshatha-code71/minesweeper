import random

class Minesweeper:
    def __init__(self, size=8, mines=10):
        self.size = size
        self.mines = mines
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.mines_locations = set()
        self.generate_board()

    def generate_board(self):
        """Randomly places mines and calculates adjacent numbers."""
        while len(self.mines_locations) < self.mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in self.mines_locations:
                self.mines_locations.add((x, y))
                self.board[x][y] = '*'
        
        for x, y in self.mines_locations:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != '*':
                        self.board[nx][ny] += 1

    def print_board(self, revealed=None):
        """Prints the board with hidden and revealed cells."""
        if revealed is None:
            revealed = set()
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i, j) in revealed:
                    row.append(str(self.board[i][j]))
                else:
                    row.append('.')
            print(" ".join(row))
        print()

class MinesweeperAI:
    def __init__(self, size):
        self.size = size
        self.safe_moves = set()
        self.known_mines = set()
        self.moves_made = set()
    
    def add_knowledge(self, x, y, value):
        """Adds knowledge about safe and mine-containing cells based on the revealed number."""
        if value == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in self.moves_made:
                        self.safe_moves.add((nx, ny))
        elif value > 0:
            unknown_neighbors = set()
            flagged_mines = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if (nx, ny) in self.known_mines:
                            flagged_mines += 1
                        elif (nx, ny) not in self.moves_made:
                            unknown_neighbors.add((nx, ny))
            
            if flagged_mines == value:
                self.safe_moves.update(unknown_neighbors)
            if len(unknown_neighbors) == value - flagged_mines:
                self.known_mines.update(unknown_neighbors)

    def make_move(self):
        """Chooses the next move: first from safe moves, otherwise guesses."""
        if self.safe_moves:
            return self.safe_moves.pop()
        
        # If stuck, choose a random cell that hasn't been played yet
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in self.moves_made and (i, j) not in self.known_mines:
                    return (i, j)
        return None  # No moves left

def play_minesweeper():
    """Runs the Minesweeper AI game."""
    size = 8
    mines = 10
    game = Minesweeper(size, mines)
    ai = MinesweeperAI(size)
    revealed = set()

    while True:
        move = ai.make_move()
        if move is None:
            print("No moves left. Game Over!")
            break

        x, y = move
        ai.moves_made.add(move)
        revealed.add(move)

        if (x, y) in game.mines_locations:
            print(f"AI hit a mine at ({x}, {y})! Game Over.")
            game.print_board(revealed)
            break

        ai.add_knowledge(x, y, game.board[x][y])
        game.print_board(revealed)

        if len(ai.moves_made) == size * size - mines:
            print("AI won! Successfully cleared the board!")
            break

# Run the Minesweeper AI game
play_minesweeper()

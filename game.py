import numpy as np

class Connect4:
    def __init__(self):
        self.board = np.array([[" "] * 7 for _ in range(6)])
        self.game_over = False
        self.player_list = ["R", "Y"]
        self.current_turn = 0
        self.available_moves = self._get_available_moves(self.board)
        self.sum = 0

    def copy(self):
        """Create a fast copy of the game state."""
        new_game = Connect4()
        new_game.board = np.copy(self.board)
        new_game.game_over = self.game_over
        new_game.current_turn = self.current_turn
        # Important: copy the list to avoid reference issues, though strings are immutable
        new_game.player_list = list(self.player_list) 
        # available_moves is a list of ints, a shallow copy or re-generation is fine
        new_game.available_moves = list(self.available_moves)
        return new_game

    def _get_available_moves(self, board=None):
        if board is None:
            board = self.board
        moves = []
        for c in range(7):
            if board[0][c] == " ":
                moves.append(c)
        
        if not moves:
            self.game_over = True
        
        return moves
    
    def make_move(self, move):
        self.available_moves = self._get_available_moves()
        if move in self.available_moves:
            board = np.transpose(self.board)
            invcol = np.flip(board[move])
            for n in range(len(invcol)):
                if invcol[n] == " ":
                    self.board[len(invcol)-n-1][move] = self.player_list[self.current_turn%2]
                    self.current_turn += 1
                    return True
        return False
    
    def simulate_move(self, move, player=None, board=None):
        if player is None:
            player = self.player_list[self.current_turn % 2]
        if board is None:
            board = self.board
        
        board_copy = board.copy()
        for r in range(5, -1, -1):
            if board_copy[r][move] == " ":
                board_copy[r][move] = player
                return board_copy
        return board_copy
    
    def check_win_on_board(self, board):
        # Check horizontal locations for win
        for c in range(7-3):
            for r in range(6):
                if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] and board[r][c] != " ":
                    # print(f"Win Horizontal: Row {r}, Cols {c}-{c+3}")
                    return board[r][c]

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] and board[r][c] != " ":
                    # print(f"Win Vertical: Col {c}, Rows {r}-{r+3}")
                    return board[r][c]

        # Check positively sloped diaganols
        for c in range(7-3):
            for r in range(6-3):
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] and board[r][c] != " ":
                    # print(f"Win Pos Slope: Start ({r},{c})")
                    return board[r][c]

        # Check negatively sloped diaganols
        for c in range(7-3):
            for r in range(3, 6):
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] and board[r][c] != " ":
                    # print(f"Win Neg Slope: Start ({r},{c})")
                    return board[r][c]
        
        return None

    def _check_winstate(self):
        winner = self.check_win_on_board(self.board)
        if winner:
            self.game_over = True
            return winner
        return False

    
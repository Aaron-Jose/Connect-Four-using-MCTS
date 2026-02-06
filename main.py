import game
from mcts import MCTS
from os import system, name

def printGame(board):
    system('cls' if name == 'nt' else 'clear')
    print("___CONNECT_4___")
    for row in board:
        temp = []
        for cell in row:
            if cell == "R":
                cell = f"{'\033[31m'}R{'\033[0m'}"
            elif cell == "Y":
                cell = f"{'\033[33m'}Y{'\033[0m'}"
            temp.append(cell)
        print(f"|{temp[0]}|{temp[1]}|{temp[2]}|{temp[3]}|{temp[4]}|{temp[5]}|{temp[6]}|")
    print("---------------")
    print("|1|2|3|4|5|6|7|")

def main():
    g = game.Connect4()
    simulations = 1000
    ai = MCTS(simulations=simulations, exploration_constant=1)
    print(f"Using Standard MCTS ({simulations} simulations)")
    
    print("Welcome to Connect 4 vs AI!")
    choice = input("Do you want to play as Red (First) or Yellow (Second)? (R/Y): ").upper()
    
    human_player = 'R' if choice != 'Y' else 'Y'
    ai_player = 'Y' if human_player == 'R' else 'R'
    
    print(f"You are {human_player}. AI is {ai_player}.")
    
    while not g.game_over:
        printGame(g.board)
        current_turn_player = g.player_list[g.current_turn % 2]
        
        if current_turn_player == human_player:
            valid_move = False
            while not valid_move:
                try:
                    chosen_move = int(input(f"Your turn ({human_player}). Enter column (1-7): ")) - 1
                    if 0 <= chosen_move <= 6:
                        possible_moves = g._get_available_moves()
                        if chosen_move in possible_moves:
                            g.make_move(chosen_move)
                            valid_move = True
                        else:
                            print("Column full! Try another.")
                    else:
                        print("Invalid column. Enter 1-7.")
                except ValueError:
                    print("Please enter a number.")
        else:
            print(f"AI ({ai_player}) is thinking...")
            move = ai.get_best_move(g)
            if move is None:
                print("No valid moves for AI. It's a draw.")
                break
            g.make_move(move)
        
        result = g._check_winstate()
        if result:
            printGame(g.board)
            print(f"Game Over! Winner: {result}")
            if result == human_player:
                print("Congratulations! You won!")
            else:
                print("AI won. Better luck next time!")
            return

    printGame(g.board)
    print("Game Over! It's a draw.")

if __name__ == "__main__":
    main()

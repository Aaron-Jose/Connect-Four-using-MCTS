import game
from mcts import MCTS
from os import system, name
import time

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
    
    print("Select Game Mode:")
    print("1. Player vs AI")
    print("2. AI vs AI")
    mode_choice = input("Enter choice (1 or 2): ")
    
    if mode_choice == "2":
        # AI vs AI Mode
        print("\n--- AI vs AI ---")
        try:
            sim1 = int(input("Enter simulations for AI 1 (Red): "))
        except ValueError:
            sim1 = 1000
            print(f"Invalid input. Defaulting to {sim1}")
            
        try:
            sim2 = int(input("Enter simulations for AI 2 (Yellow): "))
        except ValueError:
            sim2 = 1000
            print(f"Invalid input. Defaulting to {sim2}")
            
        ai1 = MCTS(simulations=sim1, exploration_constant=1.414)
        ai2 = MCTS(simulations=sim2, exploration_constant=1.414)
        
        print(f"\nStarting Game: AI 1 (Red, {sim1} sims) vs AI 2 (Yellow, {sim2} sims)")
        time.sleep(1)
        
        while not g.game_over:
            printGame(g.board)
            current_player_symbol = g.player_list[g.current_turn % 2]
            
            # Identify which AI is thinking
            if current_player_symbol == "R":
                current_ai = ai1
                ai_name = "AI 1 (Red)"
            else:
                current_ai = ai2
                ai_name = "AI 2 (Yellow)"
                
            print(f"{ai_name} is thinking...")
            move = current_ai.get_best_move(g)
            
            if move is None:
                print("No valid moves. It's a draw.")
                break
                
            g.make_move(move)
            
            # Check win
            result = g._check_winstate()
            if result:
                printGame(g.board)
                print(f"Game Over! Winner: {result}")
                if result == "R":
                    print(f"AI 1 (Red) with {sim1} simulations won!")
                else:
                    print(f"AI 2 (Yellow) with {sim2} simulations won!")
                return
            
            # Optional: slight delay to make it watchable if it's too fast (though MCTS is slow enough)
            # time.sleep(0.5) 
            
    else:
        # Player vs AI Mode
        print("\n--- Player vs AI ---")
        try:
            simulations = int(input("Enter simulations for AI (default 1000): "))
        except ValueError:
            simulations = 1000
            print(f"Invalid input. Defaulting to {simulations}")
            
        ai = MCTS(simulations=simulations, exploration_constant=1.414)
        print(f"AI configured with {simulations} simulations.")
        
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
                        user_input = input(f"Your turn ({human_player}). Enter column (1-7): ")
                        if not user_input.isdigit():
                             print("Please enter a number.")
                             continue
                        chosen_move = int(user_input) - 1
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

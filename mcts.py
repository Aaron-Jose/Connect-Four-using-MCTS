import math
import random

# Monte Carlo Tree Search (MCTS) implementation for Connect4.
# - MCTSNode: represents a node in the search tree holding game state and stats.
# - MCTS: orchestrates selection, expansion, simulation (rollout), and backpropagation.
# Uses UCT (Upper Confidence bound applied to Trees) for selection and
# simple heuristics (immediate win/block checks) to prune or shortcut simulations for speed.

class MCTSNode:
    """
    Node in the MCTS tree.

    Attributes:
    - state: a Connect4 instance representing the game state at this node.
    - parent: parent MCTSNode (None for root).
    - move: the move that led from the parent to this node.
    - children: list of child nodes.
    - wins/visits: statistics used by UCT selection.
    - untried_moves: legal moves from this state that haven't been expanded.
    - player_just_moved: the player who made the move to reach this node.
    """
    def __init__(self, state, parent=None, move=None):
        self.state = state  # The Connect4 game instance state
        self.parent = parent
        self.move = move  # The move that led to this state
        self.children = []
        self.wins = 0
        self.visits = 0
        
        # If the state is terminal (win/loss) there are no untried moves.
        if state._check_winstate():
             self.untried_moves = []
        else:
             # Otherwise initialize with legal moves from the state.
             self.untried_moves = self.get_legal_moves(state)
             
        # Player who acted last to produce this node's state.
        self.player_just_moved = state.player_list[(state.current_turn - 1) % 2]

    def get_legal_moves(self, state):
        """Return a list of legal moves for the given state."""
        return state._get_available_moves()

    def uct_select_child(self, exploration_constant=1.414):
        """
        Select a child node using the UCT (Upper Confidence Bound) formula.
        UCT balances exploitation (high win rate) and exploration (low visits).
        Formula: (wins / visits) + C * sqrt(ln(parent_visits) / visits), C = sqrt(2).
        Returns the child with the highest UCT score.
        """
        # We moved the constant OUTSIDE the square root
        s = sorted(self.children, key=lambda c: c.wins / c.visits + 
                   exploration_constant * math.sqrt(math.log(self.visits) / c.visits) 
                   if c.visits > 0 else float('inf'))
        return s[-1]

    def add_child(self, move, state):
        """
        Create a new child for this node corresponding to 'move' and return it.
        The 'state' should already reflect the move being applied.
        Uses deepcopy to avoid shared state between nodes.
        """
        node = MCTSNode(state.copy(), parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(node)
        return node

    def update(self, result):
        """
        Update node statistics with the simulation result.
        'result' is expected to be 1 for a win for player_just_moved, 0 for loss, 0.5 for draw.
        """
        self.visits += 1
        self.wins += result

class MCTS:
    """
    Monte Carlo Tree Search controller.
    'simulations' controls how many simulations are run when searching for the best move.
    """
    def __init__(self, simulations=100, exploration_constant=1.414):
        self.simulations = simulations
        self.exploration_constant = exploration_constant

    def get_best_move(self, root_state):
        """
        Run MCTS from the given root_state and return the best move found.

        Steps implemented:
        - Quick early checks (no moves, single move, immediate win/block heuristics)
        - Run self.simulations simulations of select -> expand -> simulate -> backpropagate
        - Return the child with the highest visit count (most explored)
        """
        root_node = MCTSNode(state=root_state.copy())
        
        # If there are no moves, return None
        if not root_node.untried_moves:
            return None

        # If there's only one move, don't bother simulating
        if len(root_node.untried_moves) == 1:
            return root_node.untried_moves[0]
        
        # ---------------------------------------------------------
        # Pre-MCTS checks to prevent immediate loss
        # ---------------------------------------------------------
        # Heuristics to speed up and avoid blunders:
        # 1) If we can win immediately, take the winning move.
        # 2) Prune moves that would allow the opponent to win immediately.
        legal_moves = root_state._get_available_moves()
        safe_moves = []
        
        ai_player = root_state.player_list[root_state.current_turn % 2]
        human_player = root_state.player_list[(root_state.current_turn + 1) % 2]
        
        # First, check if WE can win immediately. Use that.
        for move in legal_moves:
            next_board = root_state.simulate_move(move)
            if root_state.check_win_on_board(next_board) == ai_player:
                return move # Take the win!
        
        # Second, check if we MUST block.
        # A move is "unsafe" if the opponent can win immediately after.
        for move in legal_moves:
            # Simulate us making 'move'
            sim_board = root_state.simulate_move(move)
            
            humans_legal_moves = root_state._get_available_moves(sim_board)
            opponent_can_win = False
            
            for opp_move in humans_legal_moves:
                sim2_board = root_state.simulate_move(opp_move, human_player, sim_board)
                if root_state.check_win_on_board(sim2_board) == human_player:
                    opponent_can_win = True
                    break
            
            if not opponent_can_win:
                safe_moves.append(move)
                
        # If we have safe moves, prune unsafe ones (reduces branching factor).
        if safe_moves:
            common_safe = [m for m in root_node.untried_moves if m in safe_moves]
            if common_safe:
                root_node.untried_moves = common_safe
        
        # Main MCTS loop: repeat simulations
        for _ in range(self.simulations):
            node = root_node
            # Work on a fresh copy of the root state for this simulation
            state = root_state.copy()

            # 1. Selection: Use UCT to pick the child to follow.
            while node.untried_moves == [] and node.children != []:
                node = node.uct_select_child(self.exploration_constant)
                state.make_move(node.move)

            # 2. Expansion : Expand one untried move.
            if node.untried_moves != []:
                m = random.choice(node.untried_moves)
                state.make_move(m)
                node = node.add_child(m, state)

            # 3. Simulation (Rollout): Play random moves until the game ends.
            while not state.game_over:
                legal_moves = state._get_available_moves()
                
                if not legal_moves:
                    break
                
                state.make_move(random.choice(legal_moves))
                state._check_winstate()

            # 4. Backpropagation: Propagate results up the tree.
            winner = state._check_winstate()
            
            # Walk up the tree and update each node's statistics.
            while node is not None:
                if winner:
                    # If the player who JUST moved at this node is the winner, count as a win
                    if node.player_just_moved == winner:
                        node.update(1)
                    else:
                        node.update(0)
                else:
                    node.update(0.5)
                node = node.parent

        # Return the move that was most visited (most reliable empirically)
        return sorted(root_node.children, key=lambda c: c.visits)[-1].move

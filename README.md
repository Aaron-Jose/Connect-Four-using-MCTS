# Connect Four — Monte Carlo Tree Search (MCTS)

A lightweight Connect Four implementation powered by a Monte Carlo Tree Search (MCTS) AI.

## Overview

This repository contains a simple, playable Connect Four game with an AI opponent implemented using MCTS. The AI uses simulations (rollouts) and UCT (Upper Confidence bounds applied to Trees) to choose moves. The project is intended as an educational example of applying MCTS to a deterministic, perfect-information game.

## Features

- Play against an MCTS-based AI in the terminal.
- Basic heuristics to detect immediate wins and necessary blocks before running full simulations.
- Easy-to-tune parameters: number of simulations and exploration constant.

## Quickstart

Requirements: Python 3.8+ and NumPy.

Install dependencies:

```bash
pip install numpy
```

Run the game:

```bash
python main.py
```

During play, you will be prompted to choose to play as Red (first) or Yellow (second) and then enter a column number (1-7) to drop your disc.

## How it works (short)

- `mcts.py` implements a standard MCTS pipeline: selection (UCT), expansion, simulation (random rollouts), and backpropagation of results.
- Before searching, the AI performs quick checks: immediate winning moves and pruning moves that allow the opponent to win on the next turn.
- The AI returns the move with the highest visit count after the configured number of simulations.

## Tuning

- `simulations` (in `main.py`): number of simulated play-outs per AI decision. Increasing this improves play strength but slows the AI.
- `exploration_constant` (in `MCTS`): controls exploration vs exploitation in UCT. Typical defaults are around `1.0`–`1.414`.

## Files

- `main.py` — game loop, terminal UI, and entry point.
- `game.py` — `Connect4` game state, move generation, and win checking.
- `mcts.py` — MCTS implementation and search heuristics.
- `Reinforcement_Learning_Algorithms.pdf` — (included) reference material present in the repo.

import csv
import os
import random
from collections import defaultdict

CSV_FILE = "history.csv"

def load_history():
    if not os.path.exists(CSV_FILE):
        return []
    history = []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            history.append(row["user_move"])
    return history

def save_move(round_num, move):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["round", "user_move"])
        writer.writerow([round_num, move])

def predict_move(history):
    if len(history) == 0:
        return random.choice(["r", "p", "s"])

    freq = {"r": 0, "p": 0, "s": 0}
    for m in history:
        freq[m] += 1

    recent = history[-5:]
    weights = [1.0, 0.8, 0.6, 0.4, 0.2]
    weights = weights[:len(recent)]

    for m, w in zip(reversed(recent), weights):
        freq[m] += w

    transitions = defaultdict(lambda: {"r": 0, "p": 0, "s": 0})
    for i in range(len(history) - 1):
        transitions[history[i]][history[i+1]] += 1

    last = history[-1]
    for move, count in transitions[last].items():
        freq[move] += count * 1.2

    return max(freq, key=freq.get)

def counter(move):
    if move == "r":
        return "p"
    if move == "p":
        return "s"
    if move == "s":
        return "r"

def is_win(player, opponent):
    return (
        (player == "r" and opponent == "s") or
        (player == "s" and opponent == "p") or
        (player == "p" and opponent == "r")
    )

def compute_stats(history):
    wins = 0
    losses = 0
    ties = 0

    sim_history = []
    for move in history:
        if len(sim_history) == 0:
            predicted = random.choice(["r", "p", "s"])
        else:
            predicted = predict_move(sim_history)

        computer = counter(predicted)

        if move == computer:
            ties += 1
        elif is_win(move, computer):
            wins += 1
        else:
            losses += 1

        sim_history.append(move)

    total = wins + losses + ties
    win_pct = (wins / total * 100) if total > 0 else 0

    return wins, losses, ties, round(win_pct, 1)

from flask import Flask, render_template, request
from rps_logic import load_history, save_move, predict_move, counter, is_win, compute_stats

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    player = None
    computer = None

    if request.method == "POST":
        player = request.form["choice"]
        history = load_history()
        round_num = len(history) + 1

        predicted = predict_move(history)
        computer = counter(predicted)

        if player == computer:
            result = "It's a tie."
        elif is_win(player, computer):
            result = "You win!"
        else:
            result = "You lose."

        save_move(round_num, player)

    history = load_history()
    wins, losses, ties, win_pct = compute_stats(history)

    return render_template("index.html",
                           result=result,
                           player=player,
                           computer=computer,
                           wins=wins,
                           losses=losses,
                           ties=ties,
                           win_pct=win_pct)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

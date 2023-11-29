import tkinter as tk

def update_scores():
    for i, player in enumerate(players):
        label_var[i].set(f"{player}: {scores[i]}")

def update_custom_score(player_index,increase):
    try:
        custom_score = int(entry_var[player_index].get())
        if increase:
            scores[player_index] += custom_score
        else:
            scores[player_index] -= custom_score

        update_scores()
        entry_var[player_index].set("")  # Clear the entry after updating the score
    except ValueError:
        # Handle the case where the input is not a valid integer
        entry_var[player_index].set("")
    

def increase_score(player_index):
    scores[player_index] += 1
    update_scores()

def decrease_score(player_index):
    scores[player_index] -= 1
    update_scores()

# Example player names and initial scores
players = ["Player 1", "Player 2", "Player 3"]
scores = [0] * len(players)

# Create the main window
root = tk.Tk()
root.title("Player Scores")

# Create label variables and entry variables
label_var = [tk.StringVar() for _ in players]
entry_var = [tk.StringVar() for _ in players]

# Create labels, entry widgets, plus buttons, and minus buttons
for i, player in enumerate(players):
    label = tk.Label(root, textvariable=label_var[i])
    label_var[i].set(f"{player}: {scores[i]}")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

    # Create entry widget
    entry = tk.Entry(root, textvariable=entry_var[i], width=5)
    entry.grid(row=i, column=3, padx=5)

    # Create plus button
    plus_button = tk.Button(root, text="+", command=lambda i=i: update_custom_score(i,True), bg="green", fg="white")
    plus_button.grid(row=i, column=4, padx=5)

    # Create minus button
    minus_button = tk.Button(root, text="-", command=lambda i=i: update_custom_score(i,False), bg="red", fg="white")
    minus_button.grid(row=i, column=5, padx=5)

    # Create increase button
    increase_button = tk.Button(root, text="Right", command=lambda i=i: increase_score(i), bg="green", fg="white")
    increase_button.grid(row=i, column=1, padx=5)

    # Create decrease button
    decrease_button = tk.Button(root, text="Wrong", command=lambda i=i: decrease_score(i), bg="red", fg="white")
    decrease_button.grid(row=i, column=2, padx=5)

# Start the Tkinter event loop
while True:
    root.update()


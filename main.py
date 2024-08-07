import tkinter as tk
import matplotlib.pyplot as plt

# Initialize team details and match parameters
team1 = "Red"
team2 = "Blue"
teams = [team1, team2]
status = True
batting = teams[0]
team1_score = 0
team1_wickets = 0
team1_overs = 0
team1_balls = 0
team2_score = 0
team2_wickets = 0
team2_overs = 0
team2_balls = 0
current_batting_team = batting
team1_scores_per_over = []
team2_scores_per_over = []
team1_wickets_per_over = []
team2_wickets_per_over = []
cumulative_team1_runs = [0]
cumulative_team2_runs = [0]
overs_limit = 6
no_ball_active = False

def decide_batting_team():
    global batting_team, current_batting_team
    batting_team = teams[0]
    current_batting_team = batting_team
    result_label.config(text=f"{batting_team} will bat first!")
    update_background_color()

def update_background_color():
    if current_batting_team == team1:
        root.config(bg="red")
    else:
        root.config(bg="blue")

def disable_buttons():
    for button in buttons.values():
        button.config(state=tk.DISABLED)

def update_score(runs, is_wicket=False, extra=False, dot_ball=False):
    global team1_score, team1_wickets, team1_overs, team1_balls
    global team2_score, team2_wickets, team2_overs, team2_balls
    global current_batting_team, no_ball_active

    if no_ball_active:
        runs += 1
        no_ball_active = False

    if current_batting_team == team1:
        if is_wicket:
            team1_wickets += 1
        else:
            team1_score += runs
            cumulative_team1_runs.append(team1_score)

        if not extra and not dot_ball:
            team1_balls += 1
            if team1_balls == 6:
                team1_scores_per_over.append(team1_score - sum(team1_scores_per_over))
                team1_wickets_per_over.append(team1_wickets - sum(team1_wickets_per_over))
                team1_balls = 0
                team1_overs += 1

        if team1_overs >= overs_limit or team1_wickets >= 10:
            switch_innings()
    else:
        if is_wicket:
            team2_wickets += 1
        else:
            team2_score += runs
            cumulative_team2_runs.append(team2_score)

        if not extra and not dot_ball:
            team2_balls += 1
            if team2_balls == 6:
                team2_scores_per_over.append(team2_score - sum(team2_scores_per_over))
                team2_wickets_per_over.append(team2_wickets - sum(team2_wickets_per_over))
                team2_balls = 0
                team2_overs += 1

        if team2_score > team1_score or team2_overs >= overs_limit or team2_wickets >= 10:
            end_match()

    update_score_label()

def no_ball():
    global no_ball_active
    no_ball_active = True

def switch_innings():
    global current_batting_team
    if current_batting_team == team1:
        current_batting_team = team2
        result_label.config(text=f"{team2} is now batting!")
        update_background_color()
    else:
        end_match()
    update_score_label()

def update_required_run_rate():
    if current_batting_team == team2:
        runs_needed = team1_score - team2_score + 1
        balls_left = (overs_limit * 6) - (team2_overs * 6 + team2_balls)
        required_run_rate = runs_needed / (balls_left / 6) if balls_left > 0 else 0
        if balls_left <= 6:
            result_label.config(text=f"{runs_needed} runs needed in {balls_left} balls")
        else:
            result_label.config(text=f"Required Run Rate: {required_run_rate:.2f} runs/over")

def end_match():
    global status
    disable_buttons()
    if team2_score > team1_score:
        result_label.config(text=f"{team2} wins by {10 - team2_wickets} wickets!")
    elif team2_score == team1_score:
        result_label.config(text="The match is a tie!")
    else:
        result_label.config(text=f"{team1} wins by {team1_score - team2_score} runs!")
    status = False
    plot_analysis()

def update_score_label():
    global status
    score_text = (f"{team1}: {team1_score}/{team1_wickets} in {team1_overs}.{team1_balls} overs\n"
                  f"{team2}: {team2_score}/{team2_wickets} in {team2_overs}.{team2_balls} overs")
    score_label.config(text=score_text)
    if team2_score > team1_score:
        result_label.config(text=f"{team2} wins by {10 - team2_wickets} wickets!")
    elif status == False and team2_score < team1_score:
        result_label.config(text=f"{team1} wins by {team1_score - team2_score} runs!")
    else:
        update_required_run_rate()

def plot_analysis():
    overs = range(1, max(len(team1_scores_per_over), len(team2_scores_per_over)) + 1)
    # Fill missing overs with zeros
    while len(team1_scores_per_over) < len(overs):
        team1_scores_per_over.append(0)
    while len(team2_scores_per_over) < len(overs):
        team2_scores_per_over.append(0)
    while len(team1_wickets_per_over) < len(overs):
        team1_wickets_per_over.append(0)
    while len(team2_wickets_per_over) < len(overs):
        team2_wickets_per_over.append(0)

    # Bar graph for runs per over
    bar_width = 0.35
    fig, ax1 = plt.subplots()
    ax1.bar(overs, team1_scores_per_over, bar_width, label='Red Runs', color='red', alpha=0.6)
    ax1.bar([x + bar_width for x in overs], team2_scores_per_over, bar_width, label='Blue Runs', color='blue', alpha=0.6)
    ax1.set_xlabel('Overs')
    ax1.set_ylabel('Runs', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_xticks([x + bar_width / 2 for x in overs])
    ax1.set_xticklabels(overs)
    ax1.legend()
    plt.title('Runs per Over')
    plt.show()

    # Line graph for cumulative runs
    fig, ax2 = plt.subplots()
    ax2.plot(range(1, len(cumulative_team1_runs) + 1), cumulative_team1_runs, label=f'{team1} Cumulative Runs', color='b')
    ax2.plot(range(1, len(cumulative_team2_runs) + 1), cumulative_team2_runs, label=f'{team2} Cumulative Runs', color='r')
    ax2.set_xlabel('Balls')
    ax2.set_ylabel('Cumulative Runs')
    ax2.set_title('Cumulative Runs Over Time')
    ax2.legend()
    plt.show()

    # Bar graph for wickets per over
    fig, ax3 = plt.subplots()
    ax3.bar(overs, team1_wickets_per_over, bar_width, label='Red Wickets', color='red', alpha=0.6)
    ax3.bar([x + bar_width for x in overs], team2_wickets_per_over, bar_width, label='Blue Wickets', color='blue', alpha=0.6)
    ax3.set_xlabel('Overs')
    ax3.set_ylabel('Wickets', color='b')
    ax3.tick_params('y', colors='b')
    ax3.set_xticks([x + bar_width / 2 for x in overs])
    ax3.set_xticklabels(overs)
    ax3.legend()
    plt.title('Wickets per Over')
    plt.show()

# Create the main Tkinter window
root = tk.Tk()
root.title("Cricket Match")
root.geometry("500x300")
root.config(bg="red")

# Create the result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Create the score label
score_label = tk.Label(root, text="")
score_label.pack(pady=10)

# Create buttons for the different actions
# Create frames to hold buttons for runs and balls
buttons_frame_runs = tk.Frame(root)
buttons_frame_runs.pack(pady=10)

buttons_frame_balls = tk.Frame(root)
buttons_frame_balls.pack(pady=10)

# Modify button creation with color scheme and arrange buttons
buttons = {
    "six": tk.Button(buttons_frame_runs, text="Six", command=lambda: update_score(6), bg="#004d00", fg="white"),  # Dark Green
    "four": tk.Button(buttons_frame_runs, text="Four", command=lambda: update_score(4), bg="#009900", fg="white"), # Transition Green
    "single": tk.Button(buttons_frame_runs, text="Single", command=lambda: update_score(1), bg="#00cc00", fg="white"), # Light Green
    "double": tk.Button(buttons_frame_runs, text="Double", command=lambda: update_score(2), bg="#33cc33", fg="white"), # Transition Green
    "triple": tk.Button(buttons_frame_runs, text="Triple", command=lambda: update_score(3), bg="#66ff66", fg="white"), # Transition Green
    "wicket": tk.Button(buttons_frame_balls, text="Wicket", command=lambda: update_score(0, is_wicket=True), bg="#ff9999", fg="black"), # Light Red
    "no_ball": tk.Button(buttons_frame_balls, text="No Ball", command=no_ball, bg="#ff6666", fg="black"),  # Medium Red
    "wide_ball": tk.Button(buttons_frame_balls, text="Wide Ball", command=lambda: update_score(1, extra=True), bg="#ff4d4d", fg="black"), # Dark Red
    "dot_ball": tk.Button(buttons_frame_balls, text="Dot Ball", command=lambda: update_score(0), bg="#e6ffe6", fg="black") # Very Light Green
}

# Arrange run-related buttons in the first horizontal line
for button in [buttons["six"], buttons["four"], buttons["single"], buttons["double"], buttons["triple"]]:
    button.pack(side=tk.LEFT, padx=5)

# Arrange ball-related buttons in the second horizontal line
for button in [buttons["wicket"], buttons["no_ball"], buttons["wide_ball"], buttons["dot_ball"]]:
    button.pack(side=tk.LEFT, padx=5)


# Run the Tkinter event loop
root.mainloop()

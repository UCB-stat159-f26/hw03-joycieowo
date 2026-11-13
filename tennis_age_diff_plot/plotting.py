import matplotlib.pyplot as plt


def plot_player_ages(matches):
    """Return a matplotlib Axes containing the career-match plot."""
    needed = {"player_age", "age_difference", "result"}
    if not needed.issubset(matches.columns):
        raise ValueError(f"DataFrame needs columns: {', '.join(sorted(needed))}")
    fig, ax = plt.subplots(figsize=(10, 6))
    for result, color, label in [("W", "royalblue", "Won"), ("L", "mediumpurple", "Lost")]:
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"],
                   color=color, s=18, alpha=0.5, label=label)
    name = matches.attrs.get("player_name", "Player")
    ax.axhline(0, color="gray", linewidth=1)
    ax.set(xlabel=f"{name}'s age", ylabel="Player age − opponent age",
           title=f"{name}: Career Matches")
    ax.legend()
    fig.tight_layout()
    return ax
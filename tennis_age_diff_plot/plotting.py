import matplotlib.pyplot as plt
import numpy as np

def _style_axes(ax, matches, name):
    low, high = matches["player_age"].agg(["min", "max"])
    ax.set_xticks(np.arange(2 * np.floor(low / 2), 2 * np.ceil(high / 2) + 1, 2))
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set(xlabel=f"{name}'s age", ylabel="Age difference (years)")
    ax.axhline(0, color="#888888", linewidth=1)
    ax.grid(color="#e6e6e6", linewidth=0.8)
    ax.spines[:].set_visible(False)
    ax.tick_params(length=0, colors="#777777")


def plot_player_ages(matches):
    """Return a matplotlib Axes containing the career-match plot."""
    needed = {"player_age", "age_difference", "result"}
    if not needed.issubset(matches.columns):
        raise ValueError(f"DataFrame needs columns: {', '.join(sorted(needed))}")
    fig, ax = plt.subplots(figsize=(10, 6))
    for result, color, label in [
        ("W", "#43bfe3", "Match won"),
        ("L", "#923b8f", "Match lost"),
    ]:
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"],
                   color=color, s=20, alpha=0.9, label=label)

    name = matches.attrs.get("player_name", "Player")
    _style_axes(ax, matches, name)
    ax.set_title(f"{name}'s Professional Matches",
                 fontsize=16, fontweight="bold", pad=80)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.12),
              ncol=2, frameon=False)
    fig.tight_layout()
    return ax

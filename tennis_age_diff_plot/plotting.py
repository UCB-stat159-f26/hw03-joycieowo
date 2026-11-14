import matplotlib.pyplot as plt
import numpy as np

def _format_x_axis(ax, matches, name):
    ages = matches["player_age"].dropna()
    first = int(2 * np.floor(ages.min() / 2))
    last = int(2 * np.floor(ages.max() / 2))
    ax.set_xticks(np.arange(first, last + 1, 2))
    ax.set_xlim(first - 0.6, max(last + 0.8, ages.max() + 0.3))
    ax.xaxis.tick_top()
    ax.text(0, 1.04, f"{name.split()[-1]}’s\nage:",
            transform=ax.transAxes, color="#777777", fontsize=11)
    return first, last


def _tick_label(value, maximum):
    if value == 0:
        return "Same age"
    if value > 0:
        return f"+{value}{' years' if value == maximum else ''}"
    return f"−{abs(value)}"


def _format_y_axis(ax):
    ticks = [-20, -10, 0, 10, 20]
    labels = ["−20", "−10", "Same age", "+10", "+20 years"]
    ax.set_yticks(ticks, labels)
    ax.set_ylim(-20, 22)

    ax.text(-0.07, 0.87, "Older\nthan\nopponent",
            transform=ax.transAxes, ha="right", va="center",
            color="#777777")

    ax.text(-0.07, 0.11, "Younger\nthan\nopponent",
            transform=ax.transAxes, ha="right", va="center",
            color="#777777")


def _style_axes(ax, matches, name):
    first, last = _format_x_axis(ax, matches, name)
    _format_y_axis(ax)
    ax.set_axisbelow(True)
    ax.grid(color="#e5e5e5", linewidth=0.8)
    ax.axhline(0, color="#888888", linewidth=1)
    ax.spines[:].set_visible(False)
    ax.tick_params(axis="both", length=0, labelcolor="#777777")
    ax.set_title(f"{name}’s Professional Matches, Age {first} to {last}",
                 fontsize=17, fontweight="bold", pad=100)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.13),
              ncol=2, frameon=False)


def plot_player_ages(matches):
    """Plot player age against opponent age difference."""
    needed = {"player_age", "age_difference", "result"}
    if not needed.issubset(matches.columns):
        raise ValueError(f"Missing columns: {sorted(needed - set(matches.columns))}")

    name = matches.attrs.get("player_name", "Player")
    surname = name.split()[-1]
    fig, ax = plt.subplots(figsize=(12, 8))

    for result, color, label in [
        ("W", "#43bfe3", f"Match {surname} won"),
        ("L", "#923b8f", "Match lost"),
    ]:
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"],
                   color=color, s=20, alpha=0.9, label=label)

    _style_axes(ax, matches, name)
    fig.subplots_adjust(left=0.16, right=0.97, bottom=0.09, top=0.78)
    return ax
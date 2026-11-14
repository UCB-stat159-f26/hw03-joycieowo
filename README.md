# Tennis Age Difference Plot

## Project Overview

This assignment builds upon the previous homework assignment by transforming the Serena Williams career match visualization into a reusable Python package.

The package retrieves professional tennis players' career match data from [Tennis Abstract](https://www.tennisabstract.com/) and generates a scatter plot showing the age difference between a player and their opponents throughout their career.

The visualization is inspired by the New York Times' Serena Williams career match visualization. It preserves the general plotting style, including colors, axis labels, and layout, while omitting the event annotations.

The package supports different tennis players, including Serena Williams and Rafael Nadal.

## Repository Structure

```text
hw03-joycieowo/
├── tennis_age_diff_plot/
│   ├── __init__.py
│   ├── data.py
│   ├── cleaning.py
│   └── plotting.py
├── tests/
│   ├── mockup_JS_content/
│   │   ├── FemalePlayerCareer.js
│   │   └── MalePlayerCareer.js
│   └── test_cleaning.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### File Descriptions

- `tennis_age_diff_plot/__init__.py`: Exposes the two main public functions.
- `tennis_age_diff_plot/data.py`: Handles player-name normalization, data retrieval, and player birth-date lookup.
- `tennis_age_diff_plot/cleaning.py`: Parses JavaScript career-match data, calculates player and opponent ages, and returns a cleaned DataFrame.
- `tennis_age_diff_plot/plotting.py`: Generates the age-difference scatter plot using Matplotlib.
- `tests/mockup_JS_content/`: Contains sample JavaScript match data for female and male players.
- `tests/test_cleaning.py`: Contains automated tests for data parsing, cleaning, and plotting.
- `pyproject.toml`: Defines package metadata, dependencies, and installation settings.
- `README.md`: Provides project documentation, usage instructions, and reflections.

## Data Sources

The primary data source is [Tennis Abstract](https://www.tennisabstract.com/), which provides professional tennis match records.

Examples include:

- [Serena Williams Career Matches](https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js)
- [Rafael Nadal Career Matches](https://www.tennisabstract.com/jsmatches/RafaelNadalCareer.js)

The match data include dates, tournament information, results, opponents, and opponent age information.

The package also uses [Wikidata](https://www.wikidata.org/) to retrieve the selected player's date of birth.

### Differences Between Female and Male Player Data

The JavaScript files for female and male players store opponent age information differently.

- **Female players:** Opponent dates of birth are provided, so their ages must be calculated using the match dates.
- **Male players:** Opponent ages are already provided as numerical values.

The cleaning functions handle these differences and produce a consistent DataFrame for plotting.

## Installation

The package can be installed directly from GitHub using pip:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-joycieowo
```

Alternatively, clone the repository and install it locally:

```bash
git clone https://github.com/UCB-stat159-f26/hw03-joycieowo
cd hw03-joycieowo
python -m pip install -e ".[test]"
```

### Dependencies

The package requires Python 3.10 or later.

The main dependencies are:

- `pandas` for data cleaning and processing.
- `matplotlib` for visualization.
- `numpy` for numerical operations and axis formatting.
- `requests` for retrieving data from external websites.
- `pytest` for automated testing.

The dependencies are specified in `pyproject.toml`.

## Package Usage

The package provides two main public functions:

1. `get_player_matches()`
2. `plot_player_ages()`

### 1. Retrieve Career Match Data

The `get_player_matches()` function accepts a tennis player's name and returns a cleaned pandas DataFrame.

For example:

```python
from tennis_age_diff_plot import get_player_matches

serena = get_player_matches("Serena Williams")

print(serena.head())
```

The function accepts different name formats, including:

```python
serena = get_player_matches("serena williams")
serena = get_player_matches("Serena Williams")
serena = get_player_matches("SerenaWilliams")
```

The cleaned DataFrame contains the following variables:

| Column | Description |
|---|---|
| `date` | Date of the match |
| `opponent` | Name of the opponent |
| `result` | Match result (`W` or `L`) |
| `player_age` | Player's age at the match |
| `opponent_age` | Opponent's age at the match |
| `age_difference` | Player's age minus opponent's age |

The age difference is calculated as:

**Age Difference = Player Age - Opponent Age**

Positive values indicate that the selected player was older than their opponent, while negative values indicate that the player was younger.

### 2. Generate the Scatter Plot

The `plot_player_ages()` function takes the cleaned DataFrame and generates a scatter plot.

**Example: Serena Williams**

```python
from tennis_age_diff_plot import get_player_matches, plot_player_ages
import matplotlib.pyplot as plt

serena = get_player_matches("Serena Williams")

ax = plot_player_ages(serena)
plt.show()
```

**Example: Rafael Nadal**

```python
rafa = get_player_matches("Rafael Nadal")

ax = plot_player_ages(rafa)
plt.show()
```

### Visualization Design

The visualization follows the general style of the original Serena Williams plot.

- **X-axis:** Player's age at the time of each match, with tick marks at two-year intervals.
- **Y-axis:** Difference between the player's age and the opponent's age.
- **Y-axis ticks:** -20, -10, 0, +10, and +20, with 0 labeled "Same age."
- **Light blue points:** Matches won by the selected player (`#43bfe3`).
- **Purple points:** Matches lost by the selected player (`#923b8f`).
- **Horizontal line at zero:** Indicates matches against opponents of the same age.
- **Additional labels:** "Older than opponent" and "Younger than opponent."

The plot title and player-specific captions are generated automatically using the selected player's name.

The plot omits the original visualization's event annotations, as permitted by the assignment.

### Saving the Plot

The plotting function returns a Matplotlib Axes object, allowing users to customize or save their results.

For example:

```python
ax = plot_player_ages(serena)

ax.figure.savefig(
    "serena_plot.png",
    dpi=300,
    bbox_inches="tight"
)
```

The package does not automatically create or save output files.

### Invalid Player Names

If a player name does not correspond to an available Tennis Abstract career file, the function raises a meaningful error.

For example:

```python
unknown_player = get_player_matches("GastonSanchez")
```

The package distinguishes unavailable player data from network or external-service errors.

## Testing

The package uses `pytest` for automated testing.

To run the tests:

```bash
python -m pytest -v
```

The automated tests use local JavaScript fixtures instead of accessing the live Tennis Abstract website.

The tests cover:

- Player-name normalization
- Parsing JavaScript match data
- Calculating opponent ages for female players
- Processing numerical opponent ages for male players
- Handling invalid JavaScript content
- Handling invalid player names
- Generating scatter plots

By separating data retrieval from data cleaning, the package can test its processing logic without depending on network availability.

Live data retrieval should be tested separately to verify compatibility with Tennis Abstract and Wikidata.

## Reproducibility

The package separates data retrieval, cleaning, and visualization into independent modules.

This structure makes it easier to maintain and test individual components without modifying the entire workflow.

The `pyproject.toml` file specifies the software dependencies required for installation. The automated tests use local fixtures to avoid unpredictable behavior caused by changes in external websites or network availability.

The package can be installed directly from its GitHub repository, allowing other users to reproduce the workflow using the two public functions.

## Personal Reflections

This assignment helped me understand how to transform an existing data analysis script into a reusable Python package. In HW2, I focused on processing Serena Williams' match data and creating a specific visualization. For this homework assignment, I needed to generalize that workflow so the same functions could work with different tennis players. This made me think more carefully about function design, naming conventions, and how to organize code into separate modules.

One important challenge was handling the differences between female and male players' career-match data. Female players' files contain opponent birth dates, while male players' files already contain opponent ages. I learned that a reusable function should account for differences in input data while still returning a consistent output format. Separating the cleaning process into smaller helper functions also made the code easier to understand and maintain.

Another important part of this assignment was learning how to write tests for a package. Rather than repeatedly downloading data from Tennis Abstract, I used sample JavaScript files to test the cleaning functions. This helped me understand the value of automated testing and why tests should not depend on external websites.

Finally, I learned more about Python package development, particularly the roles of `__init__.py` and `pyproject.toml`. I also adapted my original scatter plot into a more general function that produces consistent visualizations for different players. Overall, this assignment helped me better understand how reproducible research can be supported by reusable code, clear documentation, and automated testing.

## Acknowledgments

Career match data are provided by [Tennis Abstract](https://www.tennisabstract.com/).

Player birth-date information is retrieved from [Wikidata](https://www.wikidata.org/).

The visualization is based on the New York Times' Serena Williams career match graphic.

This package was developed as part of STAT 159 coursework at UC Berkeley.

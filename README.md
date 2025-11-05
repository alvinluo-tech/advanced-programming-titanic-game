# The Temporal Rift on the Titanic - Game System

A data-driven interactive game where players act as time travelers on the Titanic, solving mysteries using the Titanic dataset.

## Project Overview

This project generates an interactive GM (Game Master) guide based on the Titanic dataset. Players must analyze passenger data to solve challenges and escape before the ship sinks.

## Features

- **Data-driven challenges**: Automatically generates game challenges from the Titanic dataset
- **Automatic chart generation**: Creates boxplots for hints using seaborn
- **Chart caching**: Charts are saved and reused to avoid regeneration
- **Beautiful HTML output**: Modern, responsive web interface with embedded charts
- **Screenshot functionality**: One-click button to capture the entire page as PNG image
- **Answer reveal mechanism**: Click-to-reveal answers to prevent spoilers
- **Markdown support**: Also generates traditional markdown documentation
- **Randomized gameplay**: Each run generates different passenger combinations
- **One-command workflow**: Generate everything with a single script

## File Structure

```
.
├── generate_challenge.py     # Game generation logic (challenges & charts)
├── convert_to_html.py        # HTML/Markdown conversion
├── requirements.txt         # Python dependencies
├── game_challenge.json       # Generated game data (JSON)
├── gm_guide.html            # Generated HTML GM guide  
├── gm_guide.md              # Generated Markdown GM guide
├── hint/                     # Generated hint charts
│   └── challenge_1_boxplot.png
├── examples/                 # Example screenshots
│   └── gm_guide_full_page.png
├── dataset/
│   └── Titanic-Dataset.csv  # Titanic passenger data
└── README.md                # This file
```

## Preview

Here's what the generated HTML guide looks like:

![GM Guide Full Page](examples/gm_guide_full_page.png)

*The guide features:*
- 📊 Interactive box plots with statistical annotations
- 🎴 Randomized passenger cards with anomalies to detect
- 🔍 Click-to-reveal answers for GM use
- 📱 Fully responsive design

## Quick Start

**Prerequisites:** Python 3.12+

Generate the game and create both HTML and Markdown guides with one command:

```bash
python convert_to_html.py
```

This will:
1. **Automatically generate fresh game data** from the Titanic dataset (randomized each run!)
2. Create `game_challenge.json` - The game data
3. Create `gm_guide.html` - Beautiful web interface (open in browser)
4. Create `gm_guide.md` - Traditional markdown file

**Note:** Each time you run this script, it generates a NEW game with different passenger combinations for variety!

### Taking Screenshots for README

**Easy way - One-click capture:**
1. Open `gm_guide.html` in your browser
2. Click the **"📸 Capture Full Page"** button (top right)
3. PNG file `gm_guide_full_page.png` will be automatically downloaded
4. Rename it to `gm_guide_preview.png` for README

**Alternative method:**
- Use browser's built-in screenshot: **F12** → **Ctrl+Shift+P** → "Capture full size screenshot"

## How to Play

1. **Players** are time travelers stuck on the Titanic
2. **Goal**: Find 4 temporal coordinate fragments before the ship sinks
3. **Challenges**: Analyze passenger data to find anomalies
4. **Example**: In Challenge 1, players must identify which passenger card is statistically impossible based on class and fare data

## HTML Features

The generated `gm_guide.html` includes:
- 🎨 Modern gradient design
- 📱 Fully responsive (mobile-friendly)
- 🎮 Game emoji header
- 💎 Beautiful code blocks for passenger data
- 💡 Color-coded hints and answers
- 📊 Professional typography

## Game Challenge Format

Each challenge includes:
- **Title**: Challenge name and location
- **Story**: Narrative context
- **Task**: What players need to do
- **Passenger Cards**: 6 passenger records (1 is fake)
- **Hint**: For the GM to guide players
- **Answer**: Which card is the anomaly

## Development

### Code Architecture

The project uses a **separation of concerns** design:

- **`generate_challenge.py`** - Game generation logic
  - Loads Titanic dataset
  - Generates challenges with random passengers
  - Creates fake data with statistical anomalies
  - Generates hint charts (boxplots)
  
- **`convert_to_html.py`** - Output conversion
  - Converts game data to Markdown
  - Converts Markdown to HTML with styling
  - Generates final guides

### Adding New Challenges

To add more challenges:

1. Create a new `generate_challenge_N()` function in `generate_challenge.py`
2. Add the `format_challenge_N()` function in `convert_to_html.py`
3. Update the `format_functions` list in `convert_to_html.py`

### How to run

To run the program:

1. Run generate_challenge.py (This can take a few seconds)
2. Open gm_guide.html in browser

### Requirements

- **Python**: 3.12+ (Tested with 3.13.5)

Install dependencies:
```bash
pip install -r requirements.txt
```

**Required packages** (see `requirements.txt`):
```txt
pandas==2.2.3
seaborn>=0.13.0  
matplotlib==3.10.0
```

## License

Educational project for Durham University's Advanced Programming course.



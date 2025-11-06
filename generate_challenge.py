import json
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os


def load_data(filepath='./dataset/Titanic-Dataset.csv'):
    """Load Titanic dataset"""
    try:
        df = pd.read_csv(filepath)
        df['Age'] = df['Age'].dropna()
        df['Fare'] = df['Fare'].dropna()
        df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
        return df
    except FileNotFoundError:
        print(f"{filepath} not found")
        exit()


def format_passenger(passenger_data) -> dict[str, object]:
    """Format passenger data for game cards (accepts Series or dict)"""
    # Handle both pandas Series and dictionaries
    if isinstance(passenger_data, dict):
        get_val = lambda key, default: passenger_data.get(key, default)
    else:
        get_val = lambda key, default: passenger_data.get(key, default)
    
    return {
        "name": get_val('Name', "N/A"),
        "Pclass": get_val('Pclass', "N/A"),
        "Age": get_val('Age', 0),
        "Sex": get_val("Sex", "N/A"),
        "Fare": round(get_val('Fare', 0), 2),
        "Embarked": get_val('Embarked', "N/A")
    }


def generate_boxplot(df, challenge_name='challenge_1'):
    """Generate and save boxplot for fare distribution by class"""
    # Create hint directory if it doesn't exist
    hint_dir = 'hint'
    if not os.path.exists(hint_dir):
        os.makedirs(hint_dir)
    
    # File path for the chart
    chart_path = os.path.join(hint_dir, f'{challenge_name}_boxplot.png')
    
    # Check if chart already exists
    if os.path.exists(chart_path):
        print(f"[SKIP] Chart already exists: {chart_path}")
        return chart_path
    
    print(f"[GENERATING] Creating boxplot: {chart_path}")
    
    # Filter out zero fares for realistic boxplot
    df_valid = df[df['Fare'] > 0].copy()
    
    # Create the boxplot
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    ax = sns.boxplot(data=df_valid, x='Pclass', y='Fare', palette='muted', hue='Pclass', legend=False)
    
    # Get statistics for each class and add min/max labels
    for i, pclass in enumerate([1, 2, 3]):
        class_data = df_valid[df_valid['Pclass'] == pclass]['Fare']
        
        if len(class_data) > 0:
            min_val = class_data.min()
            max_val = class_data.max()
            median_val = class_data.median()
            
            # Add text annotations for min, max, and median
            ax.text(i - 0.15, min_val, f'Min: £{min_val:.2f}', 
                   ha='left', va='bottom', fontsize=9, color='darkblue', fontweight='bold')
            ax.text(i + 0.15, max_val, f'Max: £{max_val:.2f}', 
                   ha='left', va='bottom', fontsize=9, color='darkred', fontweight='bold')
            ax.text(i, median_val, f'Median: £{median_val:.2f}', 
                   ha='center', va='top', fontsize=9, color='darkgreen', fontweight='bold')
    
    plt.title('Average Fare Distribution by Class (Box Plot)', fontsize=16, fontweight='bold')
    plt.xlabel('Passenger Class', fontsize=12)
    plt.ylabel('Fare (Pounds)', fontsize=12)
    # Map Pclass values (1, 2, 3) to labels
    plt.xticks([0, 1, 2], ['1st Class\n(Pclass=1)', '2nd Class\n(Pclass=2)', '3rd Class\n(Pclass=3)'])
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"[OK] Chart saved to {chart_path}")
    return chart_path


def get_fare_statistics_by_class(df):
    """Get fare statistics for each class to generate realistic fake data"""
    stats = {}
    for pclass in [1, 2, 3]:
        # Filter out zero fares (missing data) to get realistic statistics
        class_data = df[(df['Pclass'] == pclass) & (df['Fare'] > 0)]['Fare']
        
        # If no valid data for this class, use a fallback range
        if len(class_data) == 0:
            stats[pclass] = {
                'min': 0,
                'max': 100,
                'median': 50,
                'mean': 50
            }
        else:
            stats[pclass] = {
                'min': class_data.min(),
                'max': class_data.max(),
                'median': class_data.median(),
                'mean': class_data.mean()
            }
    return stats


def generate_challenge_1(df):
    """Generate Challenge 1: Find the Anomaly"""
    # Filter out passengers with zero or missing fares for realistic data
    valid_passengers = df[df['Fare'] > 0]
    
    # Sample 5 real passengers with valid fares
    real_passengers = valid_passengers.sample(5)
    
    challenge_cards = [format_passenger(row) for _, row in real_passengers.iterrows()]
    
    # Get fare statistics by class
    fare_stats = get_fare_statistics_by_class(df)
    
    # Create fake data - randomly select class and generate mismatched fare
    fake_pclass = random.choice([1, 2, 3])
    
    # Generate a fake name from a random real passenger (also with valid fare)
    fake_template = valid_passengers.sample(1).iloc[0].copy()
    fake_name = fake_template['Name']
    
    # Generate mismatched fare based on class
    # Make fake fares closer to real values but still anomalous
    if fake_pclass == 3:
        # 3rd class with unusually high fare (between 3rd class max and 2nd class min)
        min_fake_fare = fare_stats[3]['max'] * 1.05  # 5% above 3rd class max
        max_fake_fare = fare_stats[2]['min'] * 0.95  # 5% below 2nd class min
        # Ensure valid range
        min_fake_fare = min(min_fake_fare, max_fake_fare - 1)
        fake_fare = round(random.uniform(min_fake_fare, max_fake_fare), 2)
        expected_fare_range = f"£{fare_stats[3]['min']:.2f}-{fare_stats[3]['max']:.2f}"
        actual_fare_range = f"£{fake_fare:.2f}"
        anomaly_description = f"3rd class (Pclass={fake_pclass}) but paying {actual_fare_range}, which is slightly higher than typical 3rd class fares ({expected_fare_range})"
    elif fake_pclass == 2:
        # 2nd class with unusually high or low fare
        if random.random() > 0.5:
            # Too high for 2nd class (between 2nd class max and 1st class min)
            min_fake_fare = fare_stats[2]['max'] * 1.05
            max_fake_fare = fare_stats[1]['min'] * 0.95
            min_fake_fare = min(min_fake_fare, max_fake_fare - 1)
            fake_fare = round(random.uniform(min_fake_fare, max_fake_fare), 2)
            expected_range = f"£{fare_stats[2]['min']:.2f}-{fare_stats[2]['max']:.2f}"
        else:
            # Too low for 2nd class (should be below 2nd class min)
            # Range: just above 3rd class max to just below 2nd class min
            if fare_stats[3]['max'] < fare_stats[2]['min']:
                # There's a gap between 3rd class max and 2nd class min
                min_fake_fare = fare_stats[3]['max'] + 2
                max_fake_fare = fare_stats[2]['min'] - 0.5
            else:
                # No gap, use the border range
                min_fake_fare = fare_stats[3]['max'] * 1.05
                max_fake_fare = fare_stats[2]['min'] * 0.99
            # Ensure valid range
            if min_fake_fare >= max_fake_fare:
                # Fallback: slightly below 2nd class min
                max_fake_fare = fare_stats[2]['min'] * 0.90
                min_fake_fare = max_fake_fare - 5
            fake_fare = round(random.uniform(min_fake_fare, max_fake_fare), 2)
            expected_range = f"£{fare_stats[2]['min']:.2f}-{fare_stats[2]['max']:.2f}"
        actual_range = f"£{fake_fare:.2f}"
        anomaly_description = f"2nd class (Pclass={fake_pclass}) but paying {actual_range}, which doesn't quite match typical 2nd class fares ({expected_range})"
    else:  # Pclass == 1
        # 1st class with unusually low fare (should be below 1st class min)
        if fare_stats[2]['max'] < fare_stats[1]['min']:
            # There's a gap between 2nd class max and 1st class min
            min_fake_fare = fare_stats[2]['max'] + 1
            max_fake_fare = fare_stats[1]['min'] - 0.5
        else:
            # No gap, use the border range
            min_fake_fare = fare_stats[2]['max'] * 1.02
            max_fake_fare = fare_stats[1]['min'] * 0.99
        # Ensure valid range
        if min_fake_fare >= max_fake_fare:
            # Fallback: slightly below 1st class min
            max_fake_fare = fare_stats[1]['min'] * 0.90
            min_fake_fare = max_fake_fare - 5
        fake_fare = round(random.uniform(min_fake_fare, max_fake_fare), 2)
        expected_range = f"£{fare_stats[1]['min']:.2f}-{fare_stats[1]['max']:.2f}"
        actual_range = f"£{fake_fare:.2f}"
        anomaly_description = f"1st class (Pclass={fake_pclass}) but paying {actual_range}, which is slightly lower than typical 1st class fares ({expected_range})"
    
    # Create fake card
    fake_card_data = {
        'Name': fake_name,
        'Pclass': fake_pclass,
        'Age': fake_template['Age'],
        'Sex': fake_template['Sex'],
        'Fare': fake_fare,
        'Embarked': fake_template.get('Embarked', 'S'),
        '_is_fake': True
    }
    
    fake_card = format_passenger(fake_card_data)
    fake_card["_is_fake"] = True  # Mark as fake in JSON (GM only)
    challenge_cards.append(fake_card)
    random.shuffle(challenge_cards)
    
    # Generate boxplot for the hint
    chart_path = generate_boxplot(df, 'challenge_1')
    
    return {
        "title": "Challenge 1: Purser's Office (Find the Anomaly)",
        "story": "You've just boarded and been caught as stowaways. On the desk is a stack of passenger registration cards. You must identify the 'forged' card among them.",
        "task": "Out of the following 6 passenger cards, which one is statistically impossible?",
        "passenger_cards": challenge_cards,
        "hint": "GM Hint: Refer to the box plot above. The forged card has a fare that doesn't match its class - either much higher or much lower than typical for that card's class. Players should compare each card's fare with the distribution shown in the chart for that card's class.",
        "hint_chart": chart_path,  # Add chart path
        "answer": f"The forged card: {anomaly_description}."
    }


def find_intersection(word1, word2):
    """Find if two words share a common letter and return the position"""
    for i, char1 in enumerate(word1):
        for j, char2 in enumerate(word2):
            if char1 == char2:
                return (i, j)
    return None


def try_place_word(grid, word, placed_words, max_tries=50):
    """Try to place a word on the grid, attempting intersections"""
    word = word.upper()

    for placed_word_info in placed_words:
        intersection = find_intersection(word, placed_word_info["word"])

        if intersection:
            word_idx, placed_idx = intersection

            # Try placing perpendicular to the existing word
            if placed_word_info["direction"] == "across":
                # Place current word DOWN
                try:
                    new_row = placed_word_info["row"] - word_idx
                    new_col = placed_word_info["col"] + placed_idx

                    # Check boundaries and conflicts
                    if new_row >= 0 and new_col >= 0 and new_row + len(word) < len(grid) and new_col < len(grid[0]):
                        # Check for conflicts
                        valid = True
                        for i, char in enumerate(word):
                            if grid[new_row + i][new_col] != '' and grid[new_row + i][new_col] != char:
                                valid = False
                                break

                        if valid:
                            for i, char in enumerate(word):
                                grid[new_row + i][new_col] = char

                            return {
                                "word": word,
                                "row": new_row,
                                "col": new_col,
                                "direction": "down"
                            }
                except (IndexError, TypeError):
                    continue
            else:
                # Place current word ACROSS
                try:
                    new_row = placed_word_info["row"] + placed_idx
                    new_col = placed_word_info["col"] - word_idx

                    if new_col >= 0 and new_row >= 0 and new_row < len(grid) and new_col + len(word) <= len(grid[0]):
                        valid = True
                        for i, char in enumerate(word):
                            if grid[new_row][new_col + i] != '' and grid[new_row][new_col + i] != char:
                                valid = False
                                break

                        if valid:
                            for i, char in enumerate(word):
                                grid[new_row][new_col + i] = char

                            return {
                                "word": word,
                                "row": new_row,
                                "col": new_col,
                                "direction": "across"
                            }
                except (IndexError, TypeError):
                    continue

    return None


def save_crossword_answer(grid, placed_words, output_path):
    """Save crossword answer as an image"""
    if not grid or len(grid) == 0:
        return

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, len(grid[0]))
    ax.set_ylim(0, len(grid))
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw cells
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != '':
                # Draw cell
                rect = patches.Rectangle((j, len(grid) - i - 1), 1, 1,
                                        linewidth=2, edgecolor='#667eea',
                                        facecolor='#fef3c7', zorder=1)
                ax.add_patch(rect)

                # Add letter
                ax.text(j + 0.5, len(grid) - i - 0.5, cell,
                       ha='center', va='center', fontsize=16,
                       fontweight='bold', color='#000000', zorder=2)

    # Draw numbers for word starts
    for word_info in placed_words:
        row = word_info["row"]
        col = word_info["col"]
        word = word_info["word"]

        # Place number at start of word
        ax.text(col + 0.2, len(grid) - row - 0.2,
               str(placed_words.index(word_info) + 1),
               ha='left', va='top', fontsize=10,
               fontweight='bold', color='#667eea', zorder=3)

    plt.title('Crossword Answer', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_crossword_grid(words):
    """Generate a compact, interconnected crossword grid"""
    if len(words) == 0:
        return [], [], []

    # Convert to uppercase
    words = [w.upper() for w in words]

    # Create larger grid
    grid_size = 25
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    placed_words = []

    # Place first word in center, horizontally
    center_row = grid_size // 2
    center_col = grid_size // 2
    first_word = words[0]

    # Place first word
    for i, char in enumerate(first_word):
        grid[center_row][center_col + i] = char

    placed_words.append({
        "word": first_word,
        "row": center_row,
        "col": center_col,
        "direction": "across"
    })

    # Try to place remaining words with intersections
    for word in words[1:]:
        placed = False

        # Try each already placed word
        for target_word_info in placed_words:
            target_word = target_word_info["word"]

            # Find intersection
            for i, char1 in enumerate(word):
                for j, char2 in enumerate(target_word):
                    if char1 == char2:
                        # IMPORTANT: New word must be perpendicular to target word
                        # char1 is at position i in the new word, char2 is at position j in target
                        # We want to place the new word so that its char i aligns with target's char j
                        if target_word_info["direction"] == "across":
                            # Target is horizontal, so place new word DOWN (vertical)
                            # The new word's i-th character should align with target's j-th position
                            new_row = target_word_info["row"] - i  # Start i positions before the intersection
                            new_col = target_word_info["col"] + j  # Align at target's column j

                            # Check if valid placement
                            if new_row >= 0 and new_col >= 0 and new_row + len(word) < grid_size:
                                # Check for conflicts
                                valid = True

                                # Check all cells
                                for k in range(len(word)):
                                    cell = grid[new_row + k][new_col]
                                    if cell != '' and cell != word[k]:
                                        valid = False
                                        break

                                # Additional check: ensure neighboring cells (before and after) are empty
                                # to prevent word concatenation AND ensure no cells adjacent (left/right)
                                if valid:
                                    # Check cell before word
                                    if new_row > 0:
                                        if grid[new_row - 1][new_col] != '':
                                            valid = False
                                    # Check cell after word
                                    if new_row + len(word) < len(grid):
                                        if grid[new_row + len(word)][new_col] != '':
                                            valid = False
                                    # Check LEFT and RIGHT adjacent cells for any position of the word
                                    for k in range(len(word)):
                                        # Check left side (except at intersection point)
                                        if new_col > 0 and (new_row + k != target_word_info["row"]):
                                            if grid[new_row + k][new_col - 1] != '':
                                                valid = False
                                                break
                                        # Check right side (except at intersection point)
                                        if new_col < len(grid[0]) - 1 and (new_row + k != target_word_info["row"]):
                                            if grid[new_row + k][new_col + 1] != '':
                                                valid = False
                                                break

                                if valid:
                                    # Place word DOWN (vertical)
                                    for k, char in enumerate(word):
                                        grid[new_row + k][new_col] = char

                                    placed_words.append({
                                        "word": word,
                                        "row": new_row,
                                        "col": new_col,
                                        "direction": "down"
                                    })
                                    placed = True
                                    break
                        else:
                            # Target is DOWN, so place current word ACROSS (horizontal)
                            new_row = target_word_info["row"] + j  # Intersect at target's position j
                            new_col = target_word_info["col"] - i  # Start i positions before intersection

                            if new_col >= 0 and new_row >= 0 and new_col + len(word) < grid_size:
                                valid = True

                                # Check all cells
                                for k in range(len(word)):
                                    cell = grid[new_row][new_col + k]
                                    if cell != '' and cell != word[k]:
                                        valid = False
                                        break

                                # Additional check: ensure neighboring cells are empty
                                if valid:
                                    # Check cell before word
                                    if new_col > 0:
                                        if grid[new_row][new_col - 1] != '':
                                            valid = False
                                    # Check cell after word
                                    if new_col + len(word) < len(grid[0]):
                                        if grid[new_row][new_col + len(word)] != '':
                                            valid = False
                                    # Check TOP and BOTTOM adjacent cells for any position of the word
                                    for k in range(len(word)):
                                        # Check top side (except at intersection point)
                                        if new_row > 0 and (new_col + k != target_word_info["col"]):
                                            if grid[new_row - 1][new_col + k] != '':
                                                valid = False
                                                break
                                        # Check bottom side (except at intersection point)
                                        if new_row < len(grid) - 1 and (new_col + k != target_word_info["col"]):
                                            if grid[new_row + 1][new_col + k] != '':
                                                valid = False
                                                break

                                if valid:
                                    # Place word ACROSS (horizontal)
                                    for k, char in enumerate(word):
                                        grid[new_row][new_col + k] = char

                                    placed_words.append({
                                        "word": word,
                                        "row": new_row,
                                        "col": new_col,
                                        "direction": "across"
                                    })
                                    placed = True
                                    break

                if placed:
                    break

            if placed:
                break

        # If couldn't place with intersection, try standalone
        if not placed:
            # Find a good position (near existing words)
            for attempt in range(20):
                direction = random.choice(["across", "down"])
                if direction == "across":
                    row = random.randint(0, grid_size - 5)
                    col = random.randint(0, grid_size - len(word))
                else:
                    row = random.randint(0, grid_size - len(word))
                    col = random.randint(0, grid_size - 5)

                # Check if space is available
                valid = True
                if direction == "across":
                    for i, char in enumerate(word):
                        if grid[row][col + i] != '' and grid[row][col + i] != char:
                            valid = False
                            break
                else:
                    for i, char in enumerate(word):
                        if grid[row + i][col] != '' and grid[row + i][col] != char:
                            valid = False
                            break

                if valid:
                    if direction == "across":
                        for i, char in enumerate(word):
                            grid[row][col + i] = char
                    else:
                        for i, char in enumerate(word):
                            grid[row + i][col] = char

                    placed_words.append({
                        "word": word,
                        "row": row,
                        "col": col,
                        "direction": direction
                    })
                    placed = True
                    break

    # Trim grid to content
    # Find bounds
    min_row, max_row = grid_size, -1
    min_col, max_col = grid_size, -1

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell != '':
                min_row = min(min_row, i)
                max_row = max(max_row, i)
                min_col = min(min_col, j)
                max_col = max(max_col, j)

    if min_row > max_row or min_col > max_col:
        return [], [], []

    # Trim grid
    trimmed_grid = []
    for i in range(min_row, max_row + 1):
        trimmed_grid.append(grid[i][min_col:max_col + 1])

    # Adjust word positions
    adjusted_words = []
    for word_info in placed_words:
        adjusted_words.append({
            "word": word_info["word"],
            "row": word_info["row"] - min_row,
            "col": word_info["col"] - min_col,
            "direction": word_info["direction"]
        })

    directions = [w["direction"] for w in adjusted_words]

    return trimmed_grid, adjusted_words, directions


def is_valid_crossword(grid, placed_words):
    """Check if the crossword is valid - allows some disconnected words"""
    if not grid or len(placed_words) < 3:
        return False

    # Count how many words have intersections
    connected_count = 0

    for word_info in placed_words:
        has_intersection = False

        for other_word_info in placed_words:
            if other_word_info == word_info:
                continue

            # Two words must have different directions to intersect
            if word_info['direction'] == other_word_info['direction']:
                continue

            # Check if they actually cross
            if word_info['direction'] == "down":
                if (word_info['col'] == other_word_info['col'] and
                    other_word_info['row'] <= word_info['row'] < other_word_info['row'] + len(other_word_info['word'])):
                    has_intersection = True
                    break
            else:
                if (word_info['row'] == other_word_info['row'] and
                    other_word_info['col'] <= word_info['col'] < other_word_info['col'] + len(other_word_info['word'])):
                    has_intersection = True
                    break

        if has_intersection:
            connected_count += 1

    # Accept if at least 3 words are connected (out of 5)
    return connected_count >= 3


def generate_challenge_2(df):
    """Generate Challenge 2: Crossword puzzle using dataset column names"""
    # Available column names from Titanic dataset
    columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age',
               'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']

    # Filter to words of reasonable length (4-8 letters) for better crossword
    suitable_words = [col for col in columns if 4 <= len(col) <= 8]

    # Try to generate a valid crossword by retrying with different word combinations
    max_attempts = 100
    crossword_words = None
    grid = None
    placed_words = []

    for attempt in range(max_attempts):
        # Randomly select 5 different words
        current_words = random.sample(suitable_words, min(5, len(suitable_words)))

        # Generate crossword grid
        grid, placed_words, directions = generate_crossword_grid(current_words)

        # Check if all words were successfully placed
        if grid and len(placed_words) == len(current_words):
            # Check if the crossword is valid (most words connected)
            if is_valid_crossword(grid, placed_words):
                crossword_words = current_words
                print(f"[SUCCESS] Generated valid crossword after {attempt + 1} attempts")
                break

    if not crossword_words:
        # Fallback: use the last generated grid even if not fully connected
        print("[WARNING] Could not generate fully connected crossword, using generated grid")
        crossword_words = current_words if 'current_words' in locals() else random.sample(suitable_words, min(5, len(suitable_words)))
        if not grid or len(placed_words) != len(crossword_words):
            grid, placed_words, directions = generate_crossword_grid(crossword_words)

    # Save answer image with the FULL grid (not trimmed)
    answer_dir = 'answer'
    answer_path = os.path.join(answer_dir, 'challenge_2_answer.png')
    save_crossword_answer(grid, placed_words, answer_path)
    print(f"[OK] Crossword answer saved to {answer_path}")

    # Create blank grid by replacing all letters with spaces
    blank_grid = [[' ' if cell != '' else '' for cell in row] for row in grid]

    # Return both filled and blank grids
    return {
        "title": "Challenge 2: Decoding Station (Crossword Puzzle)",
        "story": "You find a security terminal that requires decoding. The system displays a crossword puzzle that must be solved to access temporal coordinates.",
        "task": "Complete the crossword puzzle using the column names from the Titanic dataset.",
        "crossword_words": crossword_words,
        "crossword_grid": blank_grid,  # Blank grid for user to fill
        "crossword_grid_filled": grid,  # Filled grid for structure reference
        "placed_words": placed_words,  # Contains adjusted positions
        "directions": directions,
        "answer_image": answer_path,
        "hint": "GM Hint: Think about the column headers from the Titanic passenger database. The words are related to passenger information.",
        "answer": f"The words to complete are: {', '.join(crossword_words).upper()}."
    }


def generate_challenge_3(df):
    """
    Generate Challenge 3 - Titanic Lifeboat Code
    Produces structured data consistent with Challenge 1 format.
    """
    NUM_PASSENGERS = 4
    MIN_SURVIVORS = 1
    MIN_DECEASED = 1

    # randomly select passengers ensuring at least one survivor and one deceased
    survivors = df[df['Survived'] == 1]
    deceased = df[df['Survived'] == 0]

    num_survivors = random.randint(MIN_SURVIVORS, NUM_PASSENGERS - MIN_DECEASED)
    num_deceased = NUM_PASSENGERS - num_survivors

    selected_survivors = survivors.sample(n=num_survivors, replace=False)
    selected_deceased = deceased.sample(n=num_deceased, replace=False)

    challenge_passengers_df = pd.concat([selected_survivors, selected_deceased]).sample(frac=1).reset_index(drop=True)

    passengers_list = []
    correct_code = ""
    for i, row in challenge_passengers_df.iterrows():
        correct_code += str(row['Survived'])

        age_value = row['Age']
        if pd.isna(age_value):
            age_value = random.randint(20, 50)

        fare_value = row['Fare']
        if pd.isna(fare_value):
            fare_value = 30 + (3 - row['Pclass']) * 20

        passengers_list.append({
            "Name": row['Name'] if 'Name' in row and pd.notna(row['Name']) else f"Passenger {i+1}",
            "Pclass": int(row['Pclass']),
            "Age": round(age_value),
            "Sex": row['Sex'],
            "Fare": round(fare_value, 2),
            "Embarked": row['Embarked'] if pd.notna(row['Embarked']) else 'S'
        })


    # generate static clues and charts
    try:
        sex_pclass_survival = (
            df.groupby(['Sex', 'Pclass'])['Survived']
            .mean().unstack().fillna(0)
        )

        age_bins = [0, 10, 20, 40, 60, 100]
        age_labels = ['<10', '10-20', '20-40', '40-60', '60+']
        df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
        age_survival = df.groupby('AgeGroup', observed=False)['Survived'].mean()

        sex_pclass_texts = [
            f"{sex.capitalize()} (Class {pclass}): {rate*100:.1f}%"
            for sex in sex_pclass_survival.index
            for pclass, rate in sex_pclass_survival.loc[sex].items()
        ]
        age_texts = [f"{age}: {rate*100:.1f}%" for age, rate in age_survival.items()]

        static_clues = [
            {"heading": "Survival Probability: Sex vs. Pclass", "content": "; ".join(sex_pclass_texts)},
            {"heading": "Survival Probability: Age Groups", "content": "; ".join(age_texts)}
        ]

        # 生成图表generate charts
        hint_dir = "hint"
        os.makedirs(hint_dir, exist_ok=True)

        # 性别+舱位生还率热图sex + pclass survival heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            sex_pclass_survival,
            annot=True,
            fmt=".2f",
            cmap="YlGnBu",
            cbar_kws={'label': 'Survival Rate'}
        )
        plt.title("Survival Rate by Sex and Pclass")
        plt.tight_layout()
        chart1_path = os.path.join(hint_dir, "challenge_3_sex_pclass.png")
        plt.savefig(chart1_path, dpi=300, bbox_inches="tight")
        plt.close()

        # 年龄段生还率柱状图age group survival bar chart
        plt.figure(figsize=(8, 6))
        sns.barplot(x=age_survival.index, y=age_survival.values, palette="coolwarm", hue=age_survival.index, legend=False)
        plt.title("Survival Rate by Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Survival Rate")
        plt.tight_layout()
        chart2_path = os.path.join(hint_dir, "challenge_3_age_group.png")
        plt.savefig(chart2_path, dpi=300, bbox_inches="tight")
        plt.close()

        hint_charts = [chart1_path, chart2_path]

    except Exception as e:
        print(f"⚠️ Error generating clues or charts: {e}")
        static_clues = []
        hint_charts = []

    # generate return data
    challenge_data = {
        "id": 3,
        "title": "Decipher the Lifeboat Code",
        "story": "The lifeboat lock requires a 4-digit code based on passengers' survival predictions.",
        "instructions": "Predict which of the 4 passengers survived (1) or perished (0). Use the survival clues provided.",
        "passengers": passengers_list,
        "static_clues": static_clues,
        "hint_chart": hint_charts,   # new: for HTML chart display
        "correct_code": correct_code
    }

    # save JSON file
    try:
        os.makedirs("src", exist_ok=True)
        with open("src/challenge_3_generated.json", "w", encoding="utf-8") as f:
            json.dump(challenge_data, f, ensure_ascii=False, indent=4)
        print("Challenge 3 JSON saved to src/challenge_3_generated.json")
    except Exception as e:
        print(f"Could not save Challenge 3 JSON: {e}")

    return challenge_data


def generate_game_data():
    """Generate fresh game data from dataset"""
    print("Loading Titanic dataset...")
    df = load_data()
    
    print("Generating challenge 1...")
    # Pass the full DataFrame so it can generate the boxplot
    challenge_1 = generate_challenge_1(df)
    
    print("Generating challenge 2...")
    challenge_2 = generate_challenge_2(df)
    print("Generating challenge 3...")
    challenge_3 = generate_challenge_3(df)

    game_data = {
        "story_background": {
            "theme": "The Temporal Rift on the Titanic",
            "role": "You are a team of time travelers.",
            "goal": "Before the ship sinks, find 5 missing 'temporal coordinate fragments'."
        },
        "challenges": [
            challenge_1,
            challenge_2,

            challenge_3
        ]
    }
    
    return game_data


def save_game_data(game_data, filename='game_challenge.json'):
    """Save game data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(game_data, f, ensure_ascii=False, indent=4)
    print(f"Game data saved to {filename}")


if __name__ == '__main__':
    # If run as standalone, generate and save game data
    game_data = generate_game_data()
    save_game_data(game_data)
    print("\n[SUCCESS] Game data generated successfully!")


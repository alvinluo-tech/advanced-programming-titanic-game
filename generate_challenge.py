import json
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
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
    if fake_pclass == 3:
        # 3rd class with unusually high fare
        fake_fare = round(random.uniform(
            fare_stats[1]['median'] * 0.8,  # Higher than 1st class median
            fare_stats[1]['max'] * 1.2
        ), 2)
        expected_fare_range = f"£{fare_stats[3]['min']:.2f}-{fare_stats[3]['max']:.2f}"
        actual_fare_range = f"£{fake_fare:.2f}"
        anomaly_description = f"3rd class (Pclass={fake_pclass}) but paying {actual_fare_range}, which is much higher than typical 3rd class fares ({expected_fare_range})"
    elif fake_pclass == 2:
        # 2nd class with unusually high or low fare
        if random.random() > 0.5:
            # Too high for 2nd class
            fake_fare = round(random.uniform(
                fare_stats[1]['median'] * 0.9,
                fare_stats[1]['max'] * 1.1
            ), 2)
            expected_range = f"£{fare_stats[2]['min']:.2f}-{fare_stats[2]['max']:.2f}"
        else:
            # Too low for 2nd class
            fake_fare = round(random.uniform(1, fare_stats[3]['min'] * 0.5), 2)
            expected_range = f"£{fare_stats[2]['min']:.2f}-{fare_stats[2]['max']:.2f}"
        actual_range = f"£{fake_fare:.2f}"
        anomaly_description = f"2nd class (Pclass={fake_pclass}) but paying {actual_range}, which doesn't match typical 2nd class fares ({expected_range})"
    else:  # Pclass == 1
        # 1st class with unusually low fare
        fake_fare = round(random.uniform(1, fare_stats[2]['median'] * 0.8), 2)
        expected_range = f"£{fare_stats[1]['min']:.2f}-{fare_stats[1]['max']:.2f}"
        actual_range = f"£{fake_fare:.2f}"
        anomaly_description = f"1st class (Pclass={fake_pclass}) but paying {actual_range}, which is much lower than typical 1st class fares ({expected_range})"
    
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
        "hint": "GM Hint: Refer to the box plot above. The forged card has a fare that doesn't match its class - either much higher or much lower than typical for that class. Players should compare each card's fare with the distribution shown in the chart for that card's class.",
        "hint_chart": chart_path,  # Add chart path
        "answer": f"The forged card: {anomaly_description}."
    }


def _pclass_to_text(pclass: int) -> str:
    mapping = {1: "first-class", 2: "second-class", 3: "third-class"}
    return mapping.get(int(pclass) if pd.notna(pclass) else 3, "third-class")


def _last_name(full_name: str) -> str:
    try:
        return str(full_name).split(',')[0].strip()
    except Exception:
        return str(full_name)


def generate_challenge_2(df):
    """Challenge 2: Echoes of the Passengers (Timeline Synchronization)

    Generates 5 one-line narrative echoes (A–E) that players must order
    chronologically using known facts:
    - Boarding order by port: S → C → Q
    - "boarded at" is pre-impact
    - "tilted/helping/chaos" is post-impact (onboard)
    - "escaped/lifeboat" is final
    """

    # Ensure we have embarkation groups
    ports = ['S', 'C', 'Q']
    port_groups = {p: df[df['Embarked'] == p] for p in ports}

    def pick_by_port(p):
        g = port_groups.get(p)
        if g is not None and len(g) > 0:
            return g.sample(1).iloc[0]
        # Fallback to any passenger if port not found
        return df.sample(1).iloc[0]

    # Three boarding echoes: S, then C, then Q (true order). We'll shuffle when presenting.
    s_row = pick_by_port('S')
    c_row = pick_by_port('C')
    q_row = pick_by_port('Q')

    def boarding_text(row, port_label):
        name = _last_name(row.get('Name', 'Unknown'))
        pclass_txt = _pclass_to_text(row.get('Pclass', 3))
        return f"{name} boards at {port_label} ({row.get('Embarked','?')}); a {pclass_txt} ticket rustles in hand."

    echo_board_s = {
        'stage': 'boarding',
        'port': 'S',
        'text': boarding_text(s_row, 'Southampton')
    }
    echo_board_c = {
        'stage': 'boarding',
        'port': 'C',
        'text': boarding_text(c_row, 'Cherbourg')
    }
    echo_board_q = {
        'stage': 'boarding',
        'port': 'Q',
        'text': boarding_text(q_row, 'Queenstown')
    }

    # One post-impact onboard echo
    post_row = df.sample(1).iloc[0]
    post_text = f"Lanterns sway as the deck tilts; {_last_name(post_row.get('Name','A passenger'))} steadies a stranger amid rising alarm."
    echo_post = {
        'stage': 'post_impact',
        'port': None,
        'text': post_text
    }

    # One escape echo (final stage)
    esc_row = df.sample(1).iloc[0]
    esc_text = f"In the final chaos, {_last_name(esc_row.get('Name','A passenger'))} finds space in a lifeboat and slips into the night."
    echo_escape = {
        'stage': 'escape',
        'port': None,
        'text': esc_text
    }

    echoes = [echo_board_s, echo_board_c, echo_board_q, echo_post, echo_escape]

    # Assign letters A–E in a random display order
    random.shuffle(echoes)
    letters = ['A', 'B', 'C', 'D', 'E']
    for i, e in enumerate(echoes):
        e['id'] = letters[i]

    # Determine the true chronological order for the solution
    stage_rank = {'boarding': 1, 'post_impact': 2, 'escape': 3}
    port_rank = {'S': 1, 'C': 2, 'Q': 3, None: 0}
    sorted_true = sorted(echoes, key=lambda e: (stage_rank.get(e['stage'], 99), port_rank.get(e.get('port'), 0)))
    solution_letters = [e['id'] for e in sorted_true]

    # Known facts presented to players
    known_facts = [
        "Boarding order by port: Southampton (S) → Cherbourg (C) → Queenstown (Q).",
        "Phrases like 'boarded at' are before the iceberg impact.",
        "Words like 'tilted', 'helping', or 'chaos' are after impact but still onboard.",
        "Mentions of 'escaped' or 'lifeboat' happen last."
    ]

    # Build final structure
    return {
        "title": "Challenge 2: Echoes of the Passengers (Timeline Synchronization)",
        "story_intro": "Time ripples carry brief echoes of five travelers aboard the Titanic. Align their moments to restore the timeline.",
        "echoes": [{"letter": e['id'], "text": e['text']} for e in echoes],
        "known_facts": known_facts,
        "task": "Arrange the echoes (A–E) in correct chronological order.",
        "solution": ", ".join(solution_letters),
        "explanation": (
            "Boarding echoes come first and follow port order S → C → Q; "
            "post-impact echoes (tilted/helping/chaos) follow; the lifeboat escape is last."
        )
    }


def generate_game_data():
    """Generate fresh game data from dataset"""
    print("Loading Titanic dataset...")
    df = load_data()
    
    print("Generating challenge 1...")
    # Pass the full DataFrame so it can generate the boxplot
    challenge_1 = generate_challenge_1(df)
    print("Generating challenge 2...")
    challenge_2 = generate_challenge_2(df)

    game_data = {
        "story_background": {
            "theme": "The Temporal Rift on the Titanic",
            "role": "You are a team of time travelers.",
            "goal": "Before the ship sinks, find 4 missing 'temporal coordinate fragments'."
        },
        "challenges": [
            challenge_1,
            challenge_2,
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


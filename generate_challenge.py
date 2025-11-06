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

# Generate a key for the substitution cipher
def generate_key():
    letters = list("abcdefhijklmnopqrstuvwxyz")
    random.shuffle(letters)

    cipher_key = ''.join(letters)
    print(cipher_key)
    return cipher_key

# Encryption algorithm for monoalphabetic substitution cipher
# Key is a string of 26 characters
def encrypt(plain_text, key):
    cipher_text = ""
    plain_text = plain_text.lower()
    for char in plain_text:
        if ord(char) >= ord('a') and ord(char) <= ord('z'):
            # Get index of plain text within alphabet (start from 0)
            pos = ord(char) - ord('a')
            cipher_text += key[pos]
        else:
            cipher_text += char
        
    return cipher_text

# Decryption algorithm for monoalphabetic substitution cipher
def decrypt(cipher_text, key):
    # Have to invert key to decrypt
    pass

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
        age_survival = df.groupby('AgeGroup')['Survived'].mean()

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
        sns.barplot(x=age_survival.index, y=age_survival.values, palette="coolwarm")
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

def generate_challenge_4(df):
    """Generate challenge 4 - Letters from a Stowaway"""
    stowaway = df.sample(1)

    cipher_key = generate_key()

    # Intercepted letter is not to be encrypted as it is to be used to help decrypt the other letter
    intercepted_letter = """   
R.M.S. TITANIC  
MARCONI WIRELESS SERVICE  
APRIL 12, 1912
To Mr. David Smith
Good afternoon, I have snuck aboard this mighty vessel. 
Now time to implement my darstardly plan!
Yours Sincerely,

A Guest of the Deep"""
    # Plaintext letter should not contain numbers.
    plaintext_letter = """
R.M.S. TITANIC  
MARCONI WIRELESS SERVICE  
APRIL 12, 1912
My secret alias is Mr James Moran

A Guest of the Deep"""

    story_text = """
    
    The Captain has called you and your group to the deck of the ship with an 
    urgent mission. Telegrams have been intercepted from the ship's Marconi machine
    and it appears there is a stowaway on board! Unfortunately, the dastardly 
    stowaway has managed to scramble one of the telegrams using a mysterious code. 
    The Captain has created a list of 10 suspects. Can you decipher the letter and
    obtain the identity of the suspect before they get away?!
    
    """

    ciphertext_letter = encrypt(plaintext_letter, cipher_key)

    challenge_data = {
        "id": 4,
        "title": "Letters from a Stowaway",
        "story": story_text,
        "instructions": "Decode the encrypted letter and select the name from the list of suspects.",
        "intercepted_letter" : intercepted_letter,
        "ciphertext_letter" : ciphertext_letter
    }

    return challenge_data


def generate_game_data():
    """Generate fresh game data from dataset"""
    print("Loading Titanic dataset...")
    df = load_data()
    
    print("Generating challenge 1...")
    # Pass the full DataFrame so it can generate the boxplot
    challenge_1 = generate_challenge_1(df)
    
    print("Generating challenge 3...")
    challenge_3 = generate_challenge_3(df)

    print("Generating challenge 4...")
    challenge_4 = generate_challenge_4(df)

    game_data = {
        "story_background": {
            "theme": "The Temporal Rift on the Titanic",
            "role": "You are a team of time travelers.",
            "goal": "Before the ship sinks, find 5 missing 'temporal coordinate fragments'."
        },
        "challenges": [
            challenge_1,
            challenge_3,
            challenge_4
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


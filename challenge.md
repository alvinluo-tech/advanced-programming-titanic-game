# The Titanic Time-Rift Escape Room
## A Data Science Adventure Game

---

## � Live Demo

**[View Game Master Guide (Live Demo)](https://sharp-cloud-uploader-nine.vercel.app/gm_guide.html)**

*Click the link above to see the interactive HTML version of the game with all challenges, visualizations, and examples.*

---

## �🌌 Story Background

### Theme: The Titanic Time-Rift

**Your Role:** You are a group of time-travelers. During a routine jump, your temporal engines malfunctioned, causing an emergency ejection. You've landed on the RMS Titanic on April 14, 1912, just hours before it sinks.

**Your Goal:** Your time machine is "phased," and to bring it back into your timeline, you must find **4 "Temporal Coordinate Fragments"** that were scattered across the ship during your crash-landing. You must collect all 4 and get to the rendezvous point before the ship sinks.

**The Challenge:** Each fragment is hidden behind a data analysis puzzle. Only by applying real data science skills can you unlock them and escape your fate.

---

## 🧩 Challenge 1: The Purser's Office
### Finding the Forged Passenger Card

### Story
You've just boarded and been caught as stowaways. You're locked in the **Purser's Office**. On the desk is a stack of passenger registration cards. To prove your intelligence and earn your freedom, you must identify the **forged card** among them.

### Challenge
- **Task:** Identify 1 forged card among 6 passenger registration cards
- **Data:** 5 cards contain authentic passenger data from the Titanic dataset
- **Anomaly:** 1 card is statistically impossible - a cleverly generated anomaly

### Technical Details

#### Data Processing
1. Load authentic Titanic dataset (891 passengers)
2. Filter passengers with valid fare data (Fare > 0)
3. Randomly sample 5 authentic passengers
4. Calculate fare statistics by passenger class:
   - **1st Class:** £5.00 - £512.33 (median: £61.98)
   - **2nd Class:** £10.50 - £73.50 (median: £15.02)
   - **3rd Class:** £4.01 - £69.55 (median: £8.05)

#### Forged Data Generation
The algorithm creates **statistically impossible combinations** where the fare completely falls outside the valid range for that class:

**6 Possible Anomaly Types:**
- **1st Class:** Too high (£522-£666) OR too low (£0.50-£4.50)
- **2nd Class:** Too high (£74-£110) OR too low (£0.50-£10.00)
- **3rd Class:** Too high (£70-£90) OR too low (£0.50-£3.51)

**Design Principle:** Zero overlap ensures the anomaly is always detectable through statistical analysis.

### Player Experience
- **Display:** 6 passenger cards (Name, Class, Age, Sex, Fare, Embarked)
- **Hint:** Box plot showing authentic fare distributions by class (min, max, median)
- **Solution:** Compare each card's fare against the box plot to find which falls outside the expected range

### Visual Examples

**Box Plot Hint Chart:**

![Challenge 1 Box Plot - Fare Distribution by Class](./hint/challenge_1_boxplot.png)

*Caption: Statistical visualization showing min, max, and median fares for each passenger class*

---

**Game Interface Screenshot:**

![Challenge 1 Game Interface](./examples/challenge_1.JPG)

*Caption: Players see 6 passenger cards and must identify the forged one*

---

### Example from Generated Game

**Real Passenger Cards (5):**
1. West, Mrs. Edwy Arthur - 2nd Class, £27.75
2. Charters, Mr. David - 3rd Class, £7.73
3. Asplund, Miss. Lillian Gertrud - 3rd Class, £31.39
4. Rice, Master. Eugene - 3rd Class, £29.12
5. Maisner, Mr. Simon - 3rd Class, £8.05

**Forged Card (1):**
- **Ryerson, Miss. Emily Borie - 2nd Class, £100.76** ❌
- **Why it's impossible:** 2nd class fares range from £10.50-£73.50, but this card shows £100.76, which is **far above the maximum**

### Reward
**✨ Temporal Coordinate Fragment 1 ✨** - Hidden beneath the forged card

---

## 🧩 Challenge 3: Decipher the Lifeboat Code
### Survival Probability Analysis

### Story
You've reached the **Lifeboat Control Room**. The control console demands a mysterious **4-digit binary code** to activate the final escape system. You must deduce the code based on passenger survival analysis from Titanic dataset clues.

### Challenge
- **Task:** Predict which of 4 passengers survived (1) or perished (0)
- **Data:** 4 passenger cards with Name, Pclass, Age, Sex, Fare, Embarked
- **Output:** A 4-bit binary code (e.g., "1001")

### Technical Details

#### Data Analysis
Players are provided with two analytical tools:

**1. Survival Probability by Sex & Pclass**

| Sex | Class | Survival Rate |
|------|-------|----------------|
| Female | 1st | 96.8% |
| Female | 2nd | 92.1% |
| Female | 3rd | 50.0% |
| Male | 1st | 36.9% |
| Male | 2nd | 15.7% |
| Male | 3rd | 13.5% |

**Insight:** Female passengers and higher-class travelers had a strong survival advantage.

**2. Survival Probability by Age Group**

| Age Group | Survival Rate |
|------------|----------------|
| < 10 | 61.3% |
| 10–20 | 40.2% |
| 20–40 | 38.8% |
| 40–60 | 39.4% |
| 60+ | 26.9% |

**Insight:** Younger passengers had slightly higher chances of survival.

#### Code Generation Logic
- At least 1 survivor and 1 deceased among the 4 passengers
- Players analyze each passenger using survival statistics
- Form binary code: `1` = likely survived, `0` = likely did not survive

### Player Experience
- **Display:** 4 passenger cards
- **Hints:** Interactive survival rate charts (heatmap + bar chart)
- **Solution:** Apply statistical reasoning to predict each passenger's fate

### Visual Examples

**Survival Rate Heatmap (Sex vs Pclass):**

![Challenge 3 Heatmap - Survival Rate by Sex and Pclass](./hint/challenge_3_sex_pclass.png)

*Caption: Heatmap showing survival probabilities based on gender and passenger class*

---

**Survival Rate Bar Chart (Age Groups):**

![Challenge 3 Bar Chart - Survival Rate by Age Group](./hint/challenge_3_age_group.png)

*Caption: Bar chart displaying survival rates across different age groups*

---

**Game Interface Screenshot:**

![Challenge 3 Game Interface](./examples/challenge_3.png)

*Caption: Players analyze 4 passenger cards with survival statistics to deduce the binary code*

---

### Example from Generated Game

**Passenger Cards:**
1. **Fox, Mr. Stanley Hubert** - 2nd Class, Male, Age 36
   - Prediction: `0` (Male, 2nd Class = 15.7% survival rate)
   
2. **Goldsmith, Mrs. Frank John** - 3rd Class, Female, Age 31
   - Prediction: `1` (Female, 3rd Class = 50.0% survival rate)
   
3. **Warren, Mrs. Frank Manley** - 1st Class, Female, Age 60
   - Prediction: `1` (Female, 1st Class = 96.8% survival rate)
   
4. **Nye, Mrs. (Elizabeth Ramell)** - 2nd Class, Female, Age 29
   - Prediction: `1` (Female, 2nd Class = 92.1% survival rate)

**Correct Code:** `0111` ✅

### Reward
**✨ Temporal Coordinate Fragment 2 ✨** - Unlocked from the lifeboat console

---

## 🧩 Challenge 4: Letters from a Stowaway
### Monoalphabetic Cipher Decryption

### Story
The Captain has called you to the deck with an urgent mission. Telegrams have been intercepted from the ship's Marconi machine—there's a **stowaway** on board! The dastardly stowaway has scrambled one telegram using a mysterious code. The Captain has created a list of 10 suspects. Can you decipher the letter and identify the stowaway before they get away?

### Challenge
- **Task:** Decode an encrypted letter and identify the stowaway from a list of suspects
- **Given to Player:**
  - An unencrypted intercepted letter
  - An encrypted letter (same sender, different content)
  - A list of 10 possible suspect names
  - An automatic decoder (optional hint)
- **Goal:** Decrypt the message to reveal passenger information (class, fare, age), then match to the correct suspect

### Technical Details

#### Encryption Method
- **Type:** Monoalphabetic substitution cipher
- **Key Generation:** Randomly shuffled 26-letter alphabet
- **Example Mapping:**
  - Plain:  `abcdefghijklmnopqrstuvwxyz`
  - Cipher: `qwertyuiopasdfghjklzxcvbnm`

#### Algorithms Required
1. **Encryption algorithm** - Substitute each letter according to cipher key
2. **Key generation algorithm** - Randomly shuffle alphabet to create cipher key
3. **Passenger selection algorithm** - Ensure selected passenger is unique in the dataset
4. **Message splicing algorithm** - Embed passenger information into the encrypted letter
5. **Decoder algorithm** (optional hint) - Help players break the cipher

#### How to Solve
1. **Compare** the unencrypted letter to the encrypted letter
2. **Find common phrases** between the two (big hint: "R.M.S. TITANIC" and "APRIL 12, 1912" at the top of both)
3. **Map letters** - Determine which cipher letter corresponds to which plaintext letter
4. **Decrypt the message** - Use the discovered mapping to decode the encrypted letter
5. **Extract information** - Find passenger details (class, fare, age) in the decrypted message
6. **Match to suspect** - Select the correct name from the list of 10 suspects

### Player Experience
- **Display:** Two letters side-by-side (one encrypted, one not)
- **Hint:** Optional automatic decoder tool
- **Solution:** Pattern matching and frequency analysis to break the cipher

### Visual Examples

**Game Interface Screenshot:**

![Challenge 4 Game Interface - Cipher Letters](./examples/challenge_4.JPG)

*Caption: Players compare the intercepted letter with the encrypted letter to break the cipher*


---

### Example from Generated Game

**Intercepted Letter (Plaintext):**
```
R.M.S. TITANIC  
MARCONI WIRELESS SERVICE  
APRIL 12, 1912
To Mr. David Smith
Good afternoon, I have snuck aboard this mighty vessel. 
Now time to implement my darstardly plan!
Yours Sincerely,

A Guest of the Deep
```

**Encrypted Letter (Ciphertext):**
```
c.s.r. yfytbfd  
stcdibf lfckhkrr rkcufdk  
tecfh 12, 1912
sq rkdcky thftr fr sc jtskr sictb

t mxkry ia yvk okke
```

**Solution Process:**
1. Notice "R.M.S. TITANIC" → "c.s.r. yfytbfd"
2. Map letters: R→c, M→s, S→r, T→y, I→f, etc.
3. Build complete cipher key
4. Decrypt hidden message revealing passenger identity
5. Match to suspect list

### Reward
**✨ Temporal Coordinate Fragment 3 ✨** - Hidden in the decoded message

---

## 🧩 Challenge 5: Identify the Saboteurs
### LLM-Generated Cryptic Clues & Outlier Detection

### Story
Two time-traveling imposters have taken the final temporal fragment and hidden it. A friend at Time Traveling HQ sent a transmission naming these imposters. However, enemy time travelers intercepted and warped the transmission. Now it only contains cryptic hints. Furthermore, the imposters added hints to non-saboteur passengers. Your task has two parts.

### Challenge Part 1: Decode Cryptic Messages

#### Task
- **Given:** 4 cryptic messages generated by LLM
- **Data:** 2 real passengers + 2 fake passengers from a suspect list
- **Goal:** Identify which passenger each cryptic hint refers to

#### Example Clues
- **Clue 1:** "She moves quietly through folded hours, stitching torn timelines with grace. Her touch repairs what the centuries unravel, though she herself remains a patch upon the fabric of memory."
  - **Answer:** Rugg, Miss. Emily

- **Clue 2:** "He pens the minutes like chapters, his words binding moments that refuse to stay still. Yet even he cannot edit the fate that writes itself between his lines."
  - **Answer:** Novel, Mr. Mansouer

- **Clue 3:** "A gentleman who counts shadows instead of stars, claiming to chart constellations no one else can see. His maps lead only in circles, drawn with ink that fades before dawn."
  - **Answer:** Cartwright, Mr. Silas (FAKE)

- **Clue 4:** "Her laughter rings like chimes at the edge of perception—sweet at first, then hollow. Those who follow her melody find themselves wandering through echo instead of song."
  - **Answer:** Bellamy, Miss. Cora (FAKE)

### Challenge Part 2: Expose Data Anomalies

#### Task
The enemy time-travelers forged database entries for the imposters, but entered anomalous family data values for siblings/spouses (`SibSp`) and parents/children (`Parch`).

#### How to Solve
- **Display:** Box-and-whisker plots for both `SibSp` and `Parch`
- **Analysis:** Compare each suspect's family counts with the rest of the Titanic passengers
- **Detection:** Passengers whose values lie far outside the normal range (outliers on box plots) are the forged, fake records (the imposters)
- **Conclusion:** The others, whose data fall within typical ranges, are real passengers

### Player Experience
- **Part 1:** LLM-generated riddles requiring creative interpretation
- **Part 2:** Data visualization analysis (box plots)
- **Solution:** Combine linguistic reasoning with statistical outlier detection



### Reward
**✨ Temporal Coordinate Fragment 4 ✨** - Recovered from the imposters

---

## 🎯 Game Summary

### Learning Objectives
This escape room teaches essential data science skills through immersive gameplay:

1. **Anomaly Detection** (Challenge 1) - Statistical distributions and data validation
2. **Predictive Analysis** (Challenge 3) - Probability and correlation analysis
3. **Pattern Recognition** (Challenge 4) - Cryptography and string manipulation
4. **Outlier Detection** (Challenge 5) - Box plot interpretation and NLP reasoning

### Technical Stack
- **Language:** Python
- **Libraries:** Pandas, Seaborn, Matplotlib
- **Data:** Titanic dataset (891 passengers)
- **Output:** JSON data + HTML visualization
- **AI:** LLM integration for cryptic clue generation

### Success Criteria
Collect all **4 Temporal Coordinate Fragments** by solving data challenges, repair the time machine, and escape before the Titanic sinks!

---

**🚢 The clock is ticking... Can you escape in time? ⏰**

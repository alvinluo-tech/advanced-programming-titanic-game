# 🧩 Challenge 3: Decipher the Lifeboat Code

## Overview

This is the third escape challenge of the group project **“The Temporal Rift on the Titanic”**, designed and implemented by **[Your Name]**.

In this stage, players must **analyze Titanic passenger survival data** to deduce a hidden **4-bit binary lifeboat code**.  
This code unlocks the final lifeboat control system and advances the team toward temporal escape.

This challenge integrates **real statistical reasoning** and **data visualization** into the game narrative.

---

## Story Background


Here, the control console demands a mysterious **4-digit binary code** to activate the final escape system.

Players must deduce the code based on **passenger survival analysis** from Titanic dataset clues.

---

## Challenge Task

> **Objective:**  
> Using the passenger cards provided and the GM’s analytical hints, deduce the **correct 4-bit lifeboat code**.

Players will be given:
- **4 passenger cards** ,
- Each with **Name, Pclass, Age, Sex, Fare, Embarked**,
- The GM provides **survival rate analysis charts** for guidance.

From the data, players reason who would have likely survived (`1`) or not (`0`), forming the final binary sequence.

---

## 📊 Data Analysis Design

This challenge builds on real Titanic survival statistics.  
To make the analysis immersive, I designed **two hint charts** that mimic GM’s analysis panels:

### 1. Survival Probability by Sex & Pclass
A visual breakdown of survival likelihood depending on both **gender** and **ticket class**.

| Sex | Class | Survival Rate |
|------|-------|----------------|
| Female | 1st | 96.8% |
| Female | 2nd | 92.1% |
| Female | 3rd | 50% |
| Male | 1st | 36.9% |
| Male | 2nd | 15.7% |
| Male | 3rd | 13.5% |

**Insight:** female passengers and higher-class travelers have a strong survival advantage.

---

### 2. Survival Probability by Age Group

| Age Group | Survival Rate |
|------------|----------------|
| < 10 | 61.3% |
| 10–20 | 40.2% |
| 20–40 | 38.8% |
| 40–60 | 39.4% |
| 60+ | 26.9% |

**Insight:** younger passengers had slightly higher chances of survival.

---

## Code Generation Logic

From the analysis above, we define the 4-bit binary lifeboat code as:

> `1` = likely survived  
> `0` = likely did not survive  

Each bit corresponds to one **age group** in order:  
`<10`, `10–20`, `20–40`, `40–60`.

A bit is `1` if the group’s survival rate > 0.5, else `0`.

For example:

| Age Group | Survival Rate | Binary Bit |
|------------|----------------|-------------|
| <10 | 0.59 | 1 |
| 10–20 | 0.48 | 0 |
| 20–40 | 0.39 | 0 |
| 40–60 | 0.37 | 0 |

**✅ Final Lifeboat Code: `1000`**

---

## Implementation Summary

The challenge was implemented in **`generate_challenge_3()`**, integrated into the main game generation script `generate_challenge.py`.

Key implementation steps:
1. **Sample passenger data** .
2. **Generate analytical hints** using Pandas grouped survival statistics.  
3. **Build interactive GM HTML hint** .  
4. **Store challenge data** as a JSON object (`challenge_3_generated.json`).  
5. **Render to Markdown & HTML** through `convert_to_html.py`.
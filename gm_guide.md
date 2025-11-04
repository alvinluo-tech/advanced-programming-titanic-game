# The Temporal Rift on the Titanic: GM Guide

**Player Role:** You are a team of time travelers.
**Final Goal:** Before the ship sinks, find 5 missing 'temporal coordinate fragments'.

--- 
## Challenge 1: Purser's Office (Find the Anomaly)

**Story:** You've just boarded and been caught as stowaways. On the desk is a stack of passenger registration cards. You must identify the 'forged' card among them.

**Task:** Out of the following 6 passenger cards, which one is statistically impossible?

![Box Plot](hint\challenge_1_boxplot.png)

### Passenger Cards (Show to Players)

**Card 1**
```
name: Sawyer, Mr. Frederick Charles
Pclass: 3
Age: 24.5
Sex: male
Fare: 8.05
Embarked: S
```
**Card 2**
```
name: O'Driscoll, Miss. Bridget
Pclass: 3
Age: nan
Sex: female
Fare: 7.75
Embarked: Q
```
**Card 3**
```
name: Palsson, Miss. Stina Viola
Pclass: 3
Age: 3.0
Sex: female
Fare: 21.07
Embarked: S
```
**Card 4**
```
name: McEvoy, Mr. Michael
Pclass: 3
Age: nan
Sex: male
Fare: 497.75
Embarked: Q
```
**Card 5**
```
name: Newell, Miss. Marjorie
Pclass: 1
Age: 23.0
Sex: female
Fare: 113.28
Embarked: C
```
**Card 6**
```
name: McDermott, Miss. Brigdet Delia
Pclass: 3
Age: nan
Sex: female
Fare: 7.79
Embarked: Q
```

---
### GM Guide

> **Hint:** GM Hint: Refer to the box plot above. The forged card has a fare that doesn't match its class - either much higher or much lower than typical for that class. Players should compare each card's fare with the distribution shown in the chart for that card's class.
> **Answer:** [[REVEAL_ANSWER]]The forged card: 3rd class (Pclass=3) but paying £497.75, which is much higher than typical 3rd class fares (£4.01-69.55). **(In this game, this card is Card 4)**[[END_REVEAL]]
> **Obtain:** **Temporal Coordinate Fragment 1** hidden under the forged card.

---
## Decipher the Lifeboat Code

**Story:** The lifeboat lock requires a 4-digit code based on passengers' survival predictions.

**Task:** Predict which of the 4 passengers survived (1) or perished (0). Use the survival clues provided.

![Hint Chart 1](hint/challenge_3_sex_pclass.png)

![Hint Chart 2](hint/challenge_3_age_group.png)

### Passenger Cards (Show to Players)

**Card 1**
```
Name: Razi, Mr. Raihed
Pclass: 3
Age: 23
Sex: male
Fare: 7.23
Embarked: C
```
**Card 2**
```
Name: Graham, Mr. George Edward
Pclass: 1
Age: 38
Sex: male
Fare: 153.46
Embarked: S
```
**Card 3**
```
Name: Allison, Miss. Helen Loraine
Pclass: 1
Age: 2
Sex: female
Fare: 151.55
Embarked: S
```
**Card 4**
```
Name: Hocking, Mrs. Elizabeth (Eliza Needs)
Pclass: 2
Age: 54
Sex: female
Fare: 23.0
Embarked: S
```

---
### GM Guide

> **Hint:** Use the survival charts above to infer the 4-digit lifeboat code.
> **Answer:** [[REVEAL_ANSWER]]0001[[END_REVEAL]]
> **Obtain:** **Temporal Coordinate Fragment 3** hidden within the lifeboat control panel.

---
## Letters from a Stowaway

**Story:** Story

**Task:** Instructions

### Letters from the Stowaway 

**Plaintext Letter**```Hello, this is unencrypted text
```
**Encrypted Letter**```3his is going 3o be encryp3ed
```
### Possible suspects 

---
## Game End

Congratulations! You've collected all 5 coordinate fragments, restarted the time machine, and successfully escaped from 1912 at the moment the Titanic sank.

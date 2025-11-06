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
name: Carter, Rev. Ernest Courtenay
Pclass: 2
Age: 54.0
Sex: male
Fare: 270.29
Embarked: S
```
**Card 2**
```
name: Andersson, Mr. Anders Johan
Pclass: 3
Age: 39.0
Sex: male
Fare: 31.27
Embarked: S
```
**Card 3**
```
name: Tikkanen, Mr. Juho
Pclass: 3
Age: 32.0
Sex: male
Fare: 7.92
Embarked: S
```
**Card 4**
```
name: Carr, Miss. Helen "Ellen"
Pclass: 3
Age: 16.0
Sex: female
Fare: 7.75
Embarked: Q
```
**Card 5**
```
name: Bishop, Mr. Dickinson H
Pclass: 1
Age: 25.0
Sex: male
Fare: 91.08
Embarked: C
```
**Card 6**
```
name: Berriman, Mr. William John
Pclass: 2
Age: 23.0
Sex: male
Fare: 13.0
Embarked: S
```

---
### GM Guide

> **Hint:** GM Hint: Refer to the box plot above. The forged card has a fare that doesn't match its class - either much higher or much lower than typical for that class. Players should compare each card's fare with the distribution shown in the chart for that card's class.
> **Answer:** [[REVEAL_ANSWER]]The forged card: 2nd class (Pclass=2) but paying £270.29, which doesn't match typical 2nd class fares (£10.50-73.50). **(In this game, this card is Card 1)**[[END_REVEAL]]
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
Name: Reeves, Mr. David
Pclass: 2
Age: 36
Sex: male
Fare: 10.5
Embarked: S
```
**Card 2**
```
Name: Foo, Mr. Choong
Pclass: 3
Age: 50
Sex: male
Fare: 56.5
Embarked: S
```
**Card 3**
```
Name: Zabour, Miss. Thamine
Pclass: 3
Age: 22
Sex: female
Fare: 14.45
Embarked: C
```
**Card 4**
```
Name: Lobb, Mrs. William Arthur (Cordelia K Stanlick)
Pclass: 3
Age: 26
Sex: female
Fare: 16.1
Embarked: S
```

---
### GM Guide

> **Hint:** Use the survival charts above to infer the 4-digit lifeboat code.
> **Answer:** [[REVEAL_ANSWER]]0100[[END_REVEAL]]
> **Obtain:** **Temporal Coordinate Fragment 3** hidden within the lifeboat control panel.

---
## Game End

Congratulations! You've collected all 5 coordinate fragments, restarted the time machine, and successfully escaped from 1912 at the moment the Titanic sank.

# The Temporal Rift on the Titanic: GM Guide

**Player Role:** You are a team of time travelers.
**Final Goal:** Before the ship sinks, find 4 missing 'temporal coordinate fragments'.

--- 
## Challenge 1: Purser's Office (Find the Anomaly)

**Story:** You've just boarded and been caught as stowaways. On the desk is a stack of passenger registration cards. You must identify the 'forged' card among them.

**Task:** Out of the following 6 passenger cards, which one is statistically impossible?

![Box Plot](hint/challenge_1_boxplot.png)

### Passenger Cards (Show to Players)

**Card 1**
```
<<<<<<< HEAD
name: Harris, Mrs. Henry Birkhardt (Irene Wallach)
Pclass: 1
Age: 35.0
Sex: female
Fare: 83.47
=======
name: Palsson, Master. Gosta Leonard
Pclass: 3
Age: 2.0
Sex: male
Fare: 21.07
>>>>>>> d35cc1da5de3adcb311aa6835ef158b2f4143131
Embarked: S
```
**Card 2**
```
<<<<<<< HEAD
name: Frauenthal, Dr. Henry William
Pclass: 1
Age: 50.0
Sex: male
Fare: 133.65
=======
name: Maioni, Miss. Roberta
Pclass: 2
Age: 16.0
Sex: female
Fare: 82.71
>>>>>>> d35cc1da5de3adcb311aa6835ef158b2f4143131
Embarked: S
```
**Card 3**
```
<<<<<<< HEAD
name: Rouse, Mr. Richard Henry
Pclass: 3
Age: 50.0
Sex: male
Fare: 8.05
=======
name: Hawksford, Mr. Walter James
Pclass: 1
Age: nan
Sex: male
Fare: 30.0
>>>>>>> d35cc1da5de3adcb311aa6835ef158b2f4143131
Embarked: S
```
**Card 4**
```
<<<<<<< HEAD
name: Sunderland, Mr. Victor Francis
Pclass: 3
Age: 16.0
Sex: male
Fare: 8.05
Embarked: S
```
**Card 5**
```
name: Moussa, Mrs. (Mantoura Boulos)
Pclass: 3
Age: nan
Sex: female
Fare: 91.78
=======
name: Canavan, Miss. Mary
Pclass: 3
Age: 21.0
Sex: female
Fare: 7.75
Embarked: Q
```
**Card 5**
```
name: Fleming, Miss. Margaret
Pclass: 1
Age: nan
Sex: female
Fare: 110.88
>>>>>>> d35cc1da5de3adcb311aa6835ef158b2f4143131
Embarked: C
```
**Card 6**
```
<<<<<<< HEAD
name: Bowerman, Miss. Elsie Edith
Pclass: 1
Age: 22.0
Sex: female
Fare: 55.0
=======
name: Lindell, Mr. Edvard Bengtsson
Pclass: 3
Age: 36.0
Sex: male
Fare: 15.55
>>>>>>> d35cc1da5de3adcb311aa6835ef158b2f4143131
Embarked: S
```

---
### GM Guide

> **Hint:** GM Hint: Refer to the box plot above. The forged card has a fare that doesn't match its class - either much higher or much lower than typical for that class. Players should compare each card's fare with the distribution shown in the chart for that card's class.
<<<<<<< HEAD
> **Answer:** [[REVEAL_ANSWER]]The forged card: 3rd class (Pclass=3) but paying £91.78, which is much higher than typical 3rd class fares (£4.01-69.55). **(In this game, this card is Card 5)**[[END_REVEAL]]
=======
> **Answer:** [[REVEAL_ANSWER]]The forged card: 2nd class (Pclass=2) but paying £82.71, which doesn't match typical 2nd class fares (£10.50-73.50). **(In this game, this card is Card 2)**[[END_REVEAL]]
>>>>>>> d35cc1da5de3adcb311aa6835ef158b2f4143131
> **Obtain:** **Temporal Coordinate Fragment 1** hidden under the forged card.

---
## Challenge 2: Echoes of the Passengers (Timeline Synchronization)

**Story:** Time ripples carry brief echoes of five travelers aboard the Titanic. Align their moments to restore the timeline.

**Known Facts**
- Boarding order by port: Southampton (S) → Cherbourg (C) → Queenstown (Q).
- Phrases like 'boarded at' are before the iceberg impact.
- Words like 'tilted', 'helping', or 'chaos' are after impact but still onboard.
- Mentions of 'escaped' or 'lifeboat' happen last.

### Echoes (Show to Players)

- Echo A: O'Dwyer boards at Queenstown (Q); a third-class ticket rustles in hand.
- Echo B: Endres boards at Cherbourg (C); a first-class ticket rustles in hand.
- Echo C: In the final chaos, Behr finds space in a lifeboat and slips into the night.
- Echo D: Wiklund boards at Southampton (S); a third-class ticket rustles in hand.
- Echo E: Lanterns sway as the deck tilts; Pengelly steadies a stranger amid rising alarm.

**Task:** Arrange the echoes (A–E) in correct chronological order.

---
### GM Guide

> **Answer:** [[REVEAL_ANSWER]]Correct order: D, B, A, E, C. Boarding echoes come first and follow port order S → C → Q; post-impact echoes (tilted/helping/chaos) follow; the lifeboat escape is last.[[END_REVEAL]]
> **Obtain:** **Temporal Coordinate Fragment 2** revealed when the order is correct.

---
## Game End

Congratulations! You've collected all 4 coordinate fragments, restarted the time machine, and successfully escaped from 1912 at the moment the Titanic sank.

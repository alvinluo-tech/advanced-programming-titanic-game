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
name: West, Mrs. Edwy Arthur (Ada Mary Worth)
Pclass: 2
Age: 33.0
Sex: female
Fare: 27.75
Embarked: S
```
**Card 2**
```
name: Charters, Mr. David
Pclass: 3
Age: 21.0
Sex: male
Fare: 7.73
Embarked: Q
```
**Card 3**
```
name: Asplund, Miss. Lillian Gertrud
Pclass: 3
Age: 5.0
Sex: female
Fare: 31.39
Embarked: S
```
**Card 4**
```
name: Rice, Master. Eugene
Pclass: 3
Age: 2.0
Sex: male
Fare: 29.12
Embarked: Q
```
**Card 5**
```
name: Maisner, Mr. Simon
Pclass: 3
Age: nan
Sex: male
Fare: 8.05
Embarked: S
```
**Card 6**
```
name: Ryerson, Miss. Emily Borie
Pclass: 2
Age: 18.0
Sex: female
Fare: 100.76
Embarked: C
```

---
### GM Guide

> **Hint:** GM Hint: Refer to the box plot above. The forged card has a fare that doesn't match its class - either much higher or much lower than typical for that class. Players should compare each card's fare with the distribution shown in the chart for that card's class.
> **Answer:** [[REVEAL_ANSWER]]The forged card: 2nd class (Pclass=2) but paying £100.76, which is much higher than typical 2nd class fares (£10.50-73.50). **(In this game, this card is Card 6)**[[END_REVEAL]]
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
Name: Fox, Mr. Stanley Hubert
Pclass: 2
Age: 36
Sex: male
Fare: 13.0
Embarked: S
```
**Card 2**
```
Name: Goldsmith, Mrs. Frank John (Emily Alice Brown)
Pclass: 3
Age: 31
Sex: female
Fare: 20.52
Embarked: S
```
**Card 3**
```
Name: Warren, Mrs. Frank Manley (Anna Sophia Atkinson)
Pclass: 1
Age: 60
Sex: female
Fare: 75.25
Embarked: C
```
**Card 4**
```
Name: Nye, Mrs. (Elizabeth Ramell)
Pclass: 2
Age: 29
Sex: female
Fare: 10.5
Embarked: S
```

---
### GM Guide

> **Hint:** Use the survival charts above to infer the 4-digit lifeboat code.
> **Answer:** [[REVEAL_ANSWER]]0111[[END_REVEAL]]
> **Obtain:** **Temporal Coordinate Fragment 3** hidden within the lifeboat control panel.

---
## Letters from a Stowaway

**Story:** 
    
    The Captain has called you and your group to the deck of the ship with an 
    urgent mission. Telegrams have been intercepted from the ship's Marconi machine
    and it appears there is a stowaway on board! Unfortunately, the dastardly 
    stowaway has managed to scramble one of the telegrams using a mysterious code. 
    The Captain has created a list of 10 suspects. Can you decipher the letter and
    obtain the identity of the suspect before they get away?!
    
    

**Task:** Decode the encrypted letter and select the name from the list of suspects.

### Letters from the Stowaway 

**Plaintext Letter**```   
R.M.S. TITANIC  
MARCONI WIRELESS SERVICE  
APRIL 12, 1912
To Mr. David Smith
Good afternoon, I have snuck aboard this mighty vessel. 
Now time to implement my darstardly plan!
Yours Sincerely,

A Guest of the Deep
```
**Encrypted Letter**```
c.s.r. yfytbfd  
stcdibf lfckhkrr rkcufdk  
tecfh 12, 1912
sq rkdcky thftr fr sc jtskr sictb

t mxkry ia yvk okke
```
### Possible suspects 

---
## Game End

Congratulations! You've collected all 5 coordinate fragments, restarted the time machine, and successfully escaped from 1912 at the moment the Titanic sank.

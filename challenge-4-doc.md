# Challenge Four

# Story

The Captain has called you and your group to the deck of the ship with an 
urgent mission. Telegrams have been intercepted from the ship's Marconi machine
and it appears there is a stowaway on board! Unfortunately, the dastardly 
stowaway has managed to scramble one of the telegrams using a mysterious code. 
The Captain has created a list of 10 suspects. Can you decipher the letter and
obtain the identity of the suspect before they get away?!

# Instructions

Decode the encrypted letter and select the name from the list of suspects.

# Documents given to the player

- An unencrypted letter
- An encrypted letter
- A list of names of possible suspects
- A automatic decoder (might include this as a hint)

# How to solve

1. Compare the unencrypted letter to the encrypted letter. It is a simple monoalphabetical substitution cipher
2. Find common phrases between the two (big hint is the date and RMS Titanic at the top of both letters)
3. Find which letter corresponds to which letter in the decrypted message
4. Using the information obtained from the decrypted letter (such as class, fare and age), select the name of the stowaway from the list of suspects.

# Algorithms required

- Encryption algorithm
- Key generation algorithm
- Algorithm to check that the passenger selected is unique
- Algorithm to take the passenger information and splice it into the letter
- Decoder algorithm (should this be included)
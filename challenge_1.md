# Challenge 1: The Purser's Office - Anomaly Detection
## 2-Minute Presentation Script

---

## Introduction (20 seconds)

Good afternoon. I'll present **Challenge 1** from our Titanic Escape Room project - **"Finding the Forged Passenger Card."**

**Story**: Players are time travelers crash-landed on the Titanic. They're caught as stowaways and locked in the Purser's Office. To escape, they must identify **one forged card among 6 passenger registration cards**.

Success means finding **Temporal Coordinate Fragment 1** - needed to repair their time machine.

---

## Technical Implementation (50 seconds)

### Data Processing
1. **Load** authentic Titanic dataset (891 passengers)
2. **Select** 5 real passengers with valid fare data
3. **Calculate** fare statistics per class:
   - 1st Class: £5.00 - £512.33 (median: £61.98)
   - 2nd Class: £10.50 - £73.50 (median: £15.02)
   - 3rd Class: £4.01 - £69.55 (median: £8.05)

### Forged Data Generation - Key Innovation
Generate **statistically impossible** fare that **completely falls outside** the valid range:

**6 Possible Anomalies** (random selection):
- **1st Class**: Too high (£522-£666) OR too low (£0.50-£4.50)
- **2nd Class**: Too high (£74-£110) OR too low (£0.50-£10.00)
- **3rd Class**: Too high (£70-£90) OR too low (£0.50-£3.51)

**Critical Design**: Zero overlap ensures the anomaly is always detectable through statistical analysis.

---

## Player Experience (30 seconds)

**Challenge**: 6 passenger cards displayed (Name, Class, Age, Sex, Fare, Embarked)

**Hint**: Box plot showing authentic fare distributions by class (min, max, median)

**Solution**: Players compare each card's fare against the box plot to find which one falls outside the expected range

---



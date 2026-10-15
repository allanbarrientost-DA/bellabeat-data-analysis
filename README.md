# BellaBeat: Discovering Daily Activity Patterns

## Project Overview

This case study explores daily activity patterns recorded by Fitbit fitness trackers to identify insights that could help BellaBeat improve user engagement and inform its marketing strategy.

The goal is to understand how users move throughout the day, how activity relates to recorded calories, and whether differences in daily routines could inform more personalized wellness experiences.

## Business Questions

- What types of activity are most common in the observed data?
- Is there an association between daily steps and recorded calories?
- Do activity patterns vary across the days of the week?
- Is lower daily step activity associated with more sedentary time?
- How could these findings inform potential BellaBeat features and marketing strategies?

## Dataset

The analysis uses the public **Fitbit Fitness Tracker Data** dataset, published on Kaggle by Mobius.

- **Observation period:** March 12 – May 12, 2016
- **Daily activity records analyzed:** 1,373
- **Distinct user IDs observed:** 35
- **Daily activity columns:** 15
- **Missing values in the consolidated daily activity table:** 0

The data reflects observed Fitbit user behavior during a limited historical period. It should not be assumed to represent all consumers or BellaBeat customers.

## Tools and Skills

- **Python:** data inspection, preparation, exploratory analysis, correlations, and visualizations
- **pandas:** data manipulation and aggregation
- **Excel / PowerPoint:** reviewing findings and communicating insights
- **Data analysis:** trend identification, descriptive statistics, interpretation, and business recommendations
- **Data communication:** translating analytical findings into actionable hypotheses

## Key Findings

### 1. Light activity was the most common activity category

Average daily activity minutes were approximately:

- Light activity: **188.1 minutes**
- Very active minutes: **19.9 minutes**
- Fairly active minutes: **13.6 minutes**

This suggests an opportunity to explore flexible goals that recognize everyday movement, rather than focusing exclusively on intense exercise.

### 2. Daily steps and calories showed a positive association

The Pearson correlation between daily steps and recorded calories was **0.58**, indicating a moderate positive association in the analyzed data.

This does not establish that additional steps directly cause a specific increase in calories burned.

### 3. Daily step counts varied by weekday

Saturday had the highest average daily step count, at approximately **7,752 steps**, while Sunday had the lowest, at approximately **6,607 steps**.

This pattern could inform experiments with day-specific goals or messaging, while recognizing that individual routines may differ.

### 4. Step counts and sedentary time showed a negative association

At the user level, the correlation between average steps and sedentary minutes was **-0.411**, indicating a moderate negative association with considerable variation between users.

This supports investigating optional movement reminders and personalized routines, rather than assuming a single intervention will work for everyone.

## Business Recommendations

Based on these exploratory findings, BellaBeat could test:

1. **Personalized activity goals** that adapt to individual behavior and progress.
2. **Flexible movement reminders** that encourage users to interrupt long sedentary periods.
3. **Day-aware engagement strategies** informed by observed weekly activity patterns.
4. **Progress visualizations** that help users understand their activity trends over time.

These recommendations are hypotheses to validate, not proven outcomes.

## Limitations

- The dataset covers a limited historical period and a relatively small group of observed users.
- Data coverage and the number of recorded days can vary between users.
- Correlation does not establish causation.
- Fitbit activity records may not reflect the behavior, preferences, or needs of BellaBeat customers.
- The analysis identifies opportunities for further investigation; it does not demonstrate that a particular marketing strategy will increase engagement.

## Next Steps

- Test personalized goals and optional reminders with actual users.
- Measure engagement, feature usage, and retention before and after changes.
- Gather user feedback to understand preferences and barriers.
- Analyze additional data over a longer period to validate whether these patterns persist.

## Project Deliverables

- **Presentation:** `presentation/BellaBeat_Analisis_de_Datos.pptx`
- **Visualizations:** `results/Graficas/`

## Conclusion

This case study illustrates how exploratory data analysis can turn activity records into practical business questions. The findings suggest opportunities for personalized goals, flexible reminders, and day-aware engagement. Further testing with BellaBeat users would be necessary to determine whether these ideas improve the user experience.

---

*Portfolio project created for data analytics learning and practice.*
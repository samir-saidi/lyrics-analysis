# Lyrical Complexity Analysis: Comparing Pop and Alternative Artists

## Overview
This project analyzes the lexical complexity of lyrics from 20 popular artists (10 pop, 10 alternative/singer-songwriter) to examine whether different musical genres exhibit distinct linguistic characteristics. Using statistical methods, the study compares multiple complexity metrics and investigates relationships between different types of lyrical complexity.

## Research Questions
1. Do pop artists exhibit different lexical complexity than alternative artists?
2. Which specific complexity metrics show the strongest differences?
3. Are different types of complexity related within songs?
4. Are there significant differences in readability between groups?

## Artists Analyzed
**Pop Artists (n=10):**
- Michael Jackson, Taylor Swift, The Beatles, Prince, Beyoncé, Madonna, Britney Spears, Adele, Whitney Houston, Elton John

**Alternative/Singer-Songwriter Artists (n=10):**
- Bob Dylan, Neil Young, Nick Cave & The Bad Seeds, Joanna Newsom, Joni Mitchell, Sufjan Stevens, Fiona Apple, Kate Bush, Tori Amos, Carole King

## Data Collection


398 songs in total were analysed. 20 songs were chosen per artist, and 2 songs failed to retrieve. The Genius.com API was used to retrieve the song lyrics. For processing, the lyrics were cleaned for encoding issues and headers such as [Verse], [Chorus], etc., were removed.

## Methodology

### Complexity Metrics Calculated
1. **Readability scores:** Flesch-Kincaid Grade Level, Gunning Fog Index, Coleman-Liau Index, Automated Readability Index, Dale-Chall Score
2. **Lexical diversity:** Type-Token Ratio (TTR)
3. **Text statistics:** Average sentence length, word count

### Statistical Analysis
- **Assumption checking:** Shapiro-Wilk test for normality, Levene's test for homogeneity of variance
- **Group comparisons:** Independent t-tests or Mann-Whitney U tests depending on assumptions
- **Effect sizes:** Cohen's d for parametric tests, rank-biserial correlation for non-parametric
- **Correlation analysis:** Pearson and Spearman correlations between metrics

## Results
**1. Do pop artists exhibit different lexical complexity than alternative artists?**

   2/4 metrics show significant differences:
   - **Type Token Ratio**: pop > alt (p=0.0000)
   - **Coleman Liau**: pop > alt (p=0.0352)

**2. Which specific complexity metrics show the strongest differences?**

   Ranked by effect size (strongest first):
   - **Type Token Ratio**: Rank-biserial r = 0.49 (medium effect)
   - **Coleman Liau**: Rank-biserial r = 0.12 (small effect)
   - **Flesch Kincaid Grade**: Rank-biserial r = -0.01 (small effect)
   - **Gunning Fog**: Rank-biserial r = -0.01 (small effect)

**3. Are different types of complexity related within songs?**

   Key correlations between metrics:
   - **Flesch Kincaid Grade & Gunning Fog**: r = 1.00 (strong positive correlation)
   - **Flesch Kincaid Grade & Type Token Ratio**: r = -0.31 (moderate negative correlation)
   - **Type Token Ratio & Gunning Fog**: r = -0.31 (moderate negative correlation)

**4. Are there significant differences in readability between groups?**

   1/3 readability metrics differ:
   - **Coleman Liau**: pop > alt (p=0.0352)

## Installation & Usage
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Genius API token in `.env` file in the root of the repository. This must include your Genius API access token, secret and ID.
4. Run data collection: `python scripts/get_lyrics.py` and processing script `python scripts/process_lyrics.py`.
5. Open analysis notebook: `jupyter notebook notebooks/04_analysis.ipynb`.

## Dependencies
pandas, numpy, matplotlib, seaborn, lyricsgenius, textstat, ftfy, scipy

## Limitations
- Sample size: 398 songs total. Retrieving a larger collection of songs from many more artists would provide better statistical power. 
- Genre classification is subjective. Many artists listed in either "pop" or "alternative" have frequently explored many other genres as well, and there is no clear cut definition for what defines either genre. I chose these artists based off of general popularity, personal preference, and which I thought represented the most "poetic" lyrics within the alternative scene (hence, more popular alternative artists are not as represented, but adding more artists will fix this.)
- Readability formulas are designed for prose, not poetry or song lyrics. The idea is that song lyrics can be *like* prose, hence we can attempt to analyse them as such. However, better metrics and formulas are required that fit in a songwriting/lyricism specific context.
- Lyrics are sourced from Genius.com, and anyone can edit it, so song lyrics may be incorrect or missing for smaller/lesser known artists. For the artists I chose this is no problem, as all have correct, complete lyrics.

## Future Work
1. Increase sample size for more statistical power
2. Include more artists in each genre category
3. Analyze trends over time within artists' careers
4. Include additional linguistic features (syntactic complexity, semantic analysis)
5. Compare with broader music genres for context

## Author
Samir Saidi
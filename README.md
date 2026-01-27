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

## Conclusions
While some clear differences emerge, the picture is more complex than a simple dichotomy between the genres.

For RQ1, the findings show a mixed pattern. Pop lyrics demonstrate higher lexical diversity, measured by the Type-Token Ratio, suggesting they employ a wider range of vocabulary within individual songs. This challenges the common perception that pop music relies on repetitive or simple language structures. The Coleman-Liau index also shows pop lyrics as slightly more complex, though this effect is modest. 

However, when examining readability through established formulas like Flesch-Kincaid and Gunning Fog, no significant differences appear between the genres. This suggests that while pop lyrics may use more varied vocabulary, their overall syntactic structure and sentence complexity do not differ substantially from alternative lyrics.

The relationships between different complexity metrics reveal an interesting pattern: vocabulary diversity shows a moderate negative correlation with syntactic complexity measures. In practical terms, songs with more varied word choices tend to have simpler sentence structures, and vice versa. This pattern holds across both genres, suggesting it may reflect a general characteristic of songwriting rather than a genre-specific feature.

The strongest correlation in the analysis between Flesch-Kincaid and Gunning Fog scores indicates these two readability formulas are measuring essentially the same underlying dimension of text complexity. This can provide confidence in the reliability of these metrics for lyrical analysis, despite their original design for prose.

These findings complicate straightforward narratives about genre differences in lyrical sophistication. They suggest that what distinguishes pop from alternative lyrics may be more about vocabulary choice and lexical richness than about overall text complexity or readability. The absence of strong differences in most readability metrics points to shared conventions in songwriting that transcend genre boundaries, particularly regarding sentence structure and grammatical complexity.

The study also highlights methodological considerations for future research. The moderate effect sizes and mixed significance across metrics underscore the value of examining multiple dimensions of complexity rather than relying on single measures. The consistency of certain patterns across genres, like the inverse relationship between vocabulary diversity and syntactic complexity, suggests fruitful avenues for investigating universal characteristics of songwriting across musical styles.

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
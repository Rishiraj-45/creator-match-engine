# Evaluation and Sanity Check

The final scoring engine was evaluated against four different campaign briefs. Each campaign was scored against the same creator dataset, and the top five ranked creators were saved to `evaluation/results.csv` together with the numerical score breakdown.

## 1. Mumbai Fashion Campaign

**Top result:** Neha Sharma — 99.33/100

Neha ranks first because she receives full scores for engagement quality, exact Fashion niche match, exact Mumbai location match, and profile completeness. Her follower count of 120,000 is also very close to the midpoint of the requested 50,000–200,000 follower range.

Aisha Yadav ranks second with 94.00. She also exactly matches the niche and location and has strong engagement, but her 80,000 followers are farther from the requested range midpoint.

The ranking is intuitive because the two exact Fashion and Mumbai matches occupy the top two positions.

## 2. Bangalore Fitness Campaign

**Top result:** Sneha Iyer — 94.29/100

Sneha ranks first because she exactly matches the Fitness niche and Bangalore location, meets the engagement requirement, and has a complete profile. Her follower count also fits the requested range.

Arjun Mehta ranks second with 90.71. He also exactly matches the niche and location and has excellent engagement, but his follower count of 45,000 is close to the lower edge of the requested range, reducing his follower-fit score.

The ranking is intuitive because both exact Fitness and Bangalore matches clearly outperform less relevant creators.

## 3. Delhi Beauty Campaign

**Top result:** Priya Singh — 93.34/100

Priya ranks first because she exactly matches the Beauty niche and Delhi location, meets the engagement requirement, and falls within the requested follower range. Her score is slightly reduced because her contact email is missing.

Meera Joshi ranks second with 90.00. She exactly matches the Delhi location and has a strong follower fit and engagement score. Her Fashion niche receives partial credit because Fashion is defined as related to Beauty.

The ranking is intuitive because the exact Beauty and Delhi creator ranks first, while a geographically strong creator from a related niche ranks second.

## 4. Mumbai Technology Campaign

**Top result:** Karan Patel — 95.67/100

Karan ranks first because he exactly matches the Technology niche and Mumbai location, has strong engagement, and has a follower count close to the midpoint of the requested range. His score is slightly reduced because his bio is missing.

The remaining creators score lower because they lose points for niche or location mismatch. Vikram Rao is a Technology creator, but his 600,000 followers are outside the requested 50,000–150,000 range and he is located in Bangalore, which significantly lowers his final score.

The ranking is intuitive because the creator who best matches the campaign across niche, location, engagement, and follower fit ranks clearly first.

## Overall Evaluation

Across all four campaign briefs, the results behave as intended:

- Exact niche and location matches generally rank highest.
- Creators near the midpoint of the requested follower range are rewarded more than creators near the range edges.
- Related niches receive partial credit without outperforming stronger exact matches.
- Creators outside the requested follower range lose the full follower-fit component.
- Missing profile fields reduce the score without overwhelming stronger campaign-match signals.

The evaluation therefore provides a reasonable sanity check that the scoring engine produces explainable and intuitively consistent rankings for the current prototype dataset.

The complete reproducible ranking output and factor-level score breakdowns are stored in `evaluation/results.csv`.
# Creator Match Engine

An explainable creator recommendation system that ranks creators for a campaign brief using a weighted 100-point scoring model.

## Features

- Accepts campaign requirements through a web interface
- Scores creators out of 100
- Ranks creators from highest to lowest match
- Returns the top 5 creator recommendations
- Explains why each creator received the score
- Evaluates the engine across four different campaign briefs
- Saves evaluation results to CSV

## Scoring Model

The final score is calculated using five components:

| Component | Maximum Score |
|---|---:|
| Engagement Rate | 40 |
| Follower Range | 20 |
| Niche Match | 20 |
| Location Match | 10 |
| Profile Completeness | 10 |
| **Total** | **100** |

## Project Structure

```text
creator-match-engine/
├── app.py
├── data/
│   └── creators.csv
├── evaluation/
│   ├── campaigns.csv
│   ├── evaluate.py
│   └── results.csv
├── src/
│   └── scoring.py
├── IMPROVEMENTS.md
├── INTEGRATION.md
├── README.md
└── requirements.txt
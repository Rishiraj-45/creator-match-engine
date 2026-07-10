# Creator Match Engine

An explainable creator recommendation system that ranks creators against a campaign brief using a deterministic, weighted 100-point scoring model.

The prototype was built for an AI-native CRM use case where talent and influencer agencies need to identify the creators who best match a campaign while also understanding why each creator received their score.

## Features

* Accepts campaign requirements through a Streamlit web interface
* Scores every creator from 0 to 100
* Returns the top 5 ranked creator matches
* Provides a numerical score breakdown for every recommendation
* Uses niche-specific engagement benchmarks
* Considers the campaign's minimum engagement requirement
* Rewards creators near the midpoint of the requested follower range
* Supports exact and related niche matches
* Supports exact-city and same-region location matches
* Measures profile completeness using bio, category, and contact email
* Evaluates the scoring engine across four sample campaign briefs
* Saves reproducible factor-level evaluation results to CSV
* Includes automated tests for scoring behavior and edge cases

## Scoring Model

The final score is calculated using five components:

| Component               | Maximum Score |
| ----------------------- | ------------: |
| Engagement Rate Quality |            40 |
| Follower Count Fit      |            20 |
| Niche Match             |            20 |
| Location Match          |            10 |
| Profile Completeness    |            10 |
| **Total**               |       **100** |

### Engagement Rate Quality — 40 points

The creator's engagement rate is compared against both:

* the benchmark average for the creator's niche
* the campaign's minimum engagement requirement

The higher of these two values becomes the required engagement rate.

A creator who meets or exceeds the requirement receives the full 40 points. Creators below the requirement receive proportional partial credit.

The prototype benchmark values are stored in `data/niche_benchmarks.csv`. These values are assumptions created for the challenge dataset and are not presented as universal industry statistics.

### Follower Count Fit — 20 points

Follower fit is based on the creator's position within the campaign's requested follower range:

* midpoint of the range: 20 points
* either range edge: 10 points
* between an edge and midpoint: proportional score from 10 to 20
* outside the requested range: 0 points

An equal minimum and maximum follower range is also handled as an edge case.

### Niche Match — 20 points

* exact niche match: 20 points
* related niche: 10 points
* unrelated niche: 0 points

Related niches are defined using a small prototype mapping documented in `SCORING.md`.

### Location Match — 10 points

* exact city match: 10 points
* different city in the same prototype region: 5 points
* unrelated region: 0 points

The prototype regional mapping is documented in `SCORING.md`.

### Profile Completeness — 10 points

Profile completeness checks the three challenge-required fields:

* bio
* category
* contact email

The 10 points are divided equally across the three fields.

For the complete scoring formulas, assumptions, mappings, and limitations, see `SCORING.md`.

## Main Scoring Function

The main scoring function is:

`scoreCreator(campaign, creator, benchmarks)`

It returns:

```python
{
    "total": 95.67,
    "breakdown": {
        "engagementRate": 40.0,
        "followerFit": 19.0,
        "nicheMatch": 20.0,
        "location": 10.0,
        "completeness": 6.67
    }
}
```

This structure makes every recommendation deterministic and explainable.

## Project Structure

```text
creator-match-engine/
|-- .gitignore
|-- app.py
|-- data/
|   |-- creators.csv
|   `-- niche_benchmarks.csv
|-- evaluation/
|   |-- campaigns.csv
|   |-- evaluate.py
|   `-- results.csv
|-- src/
|   `-- scoring.py
|-- tests/
|   `-- test_scoring.py
|-- EVALUATION.md
|-- IMPROVEMENTS.md
|-- INTEGRATION.md
|-- README.md
|-- SCORING.md
`-- requirements.txt
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rishiraj-45/creator-match-engine.git
cd creator-match-engine
```

### 2. Install dependencies

```bash
py -m pip install -r requirements.txt
```

## Run the Web App

From the project root, run:

```bash
py -m streamlit run app.py
```

The interface allows the user to enter:

* minimum followers
* maximum followers
* minimum engagement rate
* campaign niche
* campaign location

After clicking **Find Top Creators**, the app displays the top five ranked creators and the numerical breakdown of each score.

## Run the Automated Tests

From the project root, run:

```bash
py -m pytest -v
```

The test suite covers benchmark lookup, engagement scoring, follower midpoint and edge behavior, equal follower ranges, niche matching, regional location matching, profile completeness, perfect matches, score totals, and the 100-point maximum.

## Reproduce the Evaluation

Run:

```bash
py -m evaluation.evaluate
```

This evaluates all creators against four sample campaign briefs:

1. Mumbai Fashion Campaign
2. Bangalore Fitness Campaign
3. Delhi Beauty Campaign
4. Mumbai Technology Campaign

The command regenerates:

`evaluation/results.csv`

The results file contains:

* campaign name
* rank
* creator name
* total score
* engagement score
* follower-fit score
* niche-match score
* location score
* completeness score

This makes the evaluation results reproducible and preserves the explanation behind every ranking.

For the written sanity-check of the four rankings, see `EVALUATION.md`.

## Documentation

* `SCORING.md` — scoring formulas, assumptions, related-niche mapping, regional mapping, design reasoning, and limitations
* `EVALUATION.md` — ranking sanity-check across four sample campaign briefs
* `INTEGRATION.md` — how the prototype could connect to an existing production CRM
* `IMPROVEMENTS.md` — what could be improved with more time

## Technology Stack

* Python 3.12
* Pandas
* Streamlit
* pytest

## Evaluation Summary

The final evaluation shows that:

* exact niche and location matches generally rank highest
* creators near the follower-range midpoint are rewarded
* related niches receive partial credit
* creators outside the requested follower range lose follower-fit points
* incomplete profiles lose completeness points without overwhelming stronger campaign-match signals

The full factor-level results are stored in `evaluation/results.csv`.

## Design Approach

This prototype intentionally uses a deterministic rule-based scoring engine rather than a trained machine-learning model.

For the current challenge dataset, this approach provides:

* explainable rankings
* predictable behavior
* easy testing
* transparent assumptions
* straightforward integration into a production service

With historical campaign performance and outcome data, a future version could learn or optimize parts of the ranking model.

## Team Contributions

The project was developed collaboratively with work divided across the scoring engine, automated tests, scoring documentation, application interface, evaluation, and integration.

The repository commit and pull-request history preserves the team's contributions throughout the sprint.

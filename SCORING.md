# Creator Match Engine — Scoring Methodology

The Creator Match Engine uses a deterministic 100-point scoring system to rank creators against a campaign brief. The total score is divided across five factors:

| Scoring Factor | Maximum Points |
|---|---:|
| Engagement Rate Quality | 40 |
| Follower Count Fit | 20 |
| Niche Match | 20 |
| Location Match | 10 |
| Profile Completeness | 10 |
| **Total** | **100** |

Each factor is calculated independently, and the final creator score is the sum of all five factor scores. The engine also returns a numerical breakdown so that every ranking can be explained and inspected.
## 1. Engagement Rate Quality — 40 Points

The engagement score compares the creator's engagement rate against both the benchmark for the creator's niche and the campaign's minimum engagement-rate requirement.

The engine first looks up the creator's niche in the benchmark dataset. If the niche is not available, a fallback benchmark of **3.0%** is used.

The required engagement rate is defined as the higher of:

- the creator's niche benchmark; and
- the campaign's minimum engagement rate.

In other words:

```text
required engagement = max(niche benchmark, campaign minimum engagement rate)

## 2. Follower Count Fit — 20 Points

The follower-fit score measures how close a creator's follower count is to the midpoint of the campaign's requested follower range.

The midpoint is calculated as:

`midpoint = (minimum followers + maximum followers) / 2`

Scoring behavior:

- A creator exactly at the midpoint receives **20 points**.
- A creator at either range edge receives **10 points**.
- A creator between an edge and the midpoint receives a proportional score between **10 and 20 points**.
- A creator outside the requested follower range receives **0 points**.

Example for a campaign requesting 50,000 to 150,000 followers:

| Creator Followers | Score |
|---:|---:|
| 50,000 | 10 |
| 75,000 | 15 |
| 100,000 | 20 |
| 125,000 | 15 |
| 150,000 | 10 |
| Outside the range | 0 |

The implementation also handles the edge case where the minimum and maximum follower values are equal. In that case, a creator with exactly that follower count receives the full score, while any other follower count receives zero.

This approach rewards creators closest to the campaign's ideal audience size while still giving partial credit to valid creators near the range boundaries.

## 3. Niche Match — 20 Points

The niche-match score measures how closely the creator's niche aligns with the campaign's target niche.

Scoring behavior:

- Exact niche match: **20 points**
- Related or adjacent niche: **10 points**
- Unrelated niche: **0 points**

The prototype uses the following explicit related-niche mapping:

| Campaign Niche | Related Creator Niches |
|---|---|
| Fashion | Beauty, Fitness |
| Beauty | Fashion |
| Fitness | Fashion |
| Technology | Gaming |
| Gaming | Technology |
| Food | None |

Examples:

- A Fashion creator for a Fashion campaign receives 20 points.
- A Beauty creator for a Fashion campaign receives 10 points.
- A Food creator for a Fashion campaign receives 0 points.

The mapping is explicitly defined in the scoring engine so that the result is deterministic and testable. These relationships are prototype assumptions for the current dataset rather than universal industry rules.

## 4. Location Match — 10 Points

The location-match score measures geographic alignment between the creator and the campaign.

Scoring behavior:

- Exact city match: **10 points**
- Different city in the same prototype region: **5 points**
- Unrelated region: **0 points**

The prototype uses the following city-region mapping:

| Region | Cities |
|---|---|
| West | Mumbai, Pune, Ahmedabad |
| North | Delhi, Jaipur, Chandigarh |
| South | Bangalore, Chennai, Hyderabad |
| East | Kolkata, Bhubaneswar, Guwahati |

Examples:

- Mumbai creator for a Mumbai campaign receives 10 points.
- Pune creator for a Mumbai campaign receives 5 points because both cities are in the West region.
- Delhi creator for a Mumbai campaign receives 0 points.

This mapping is intentionally limited to the prototype dataset and a small set of additional cities needed to demonstrate regional matching. It is not intended to represent a complete geographic classification system.

## 5. Profile Completeness — 10 Points

The profile-completeness score checks the three fields required by the challenge:

- bio
- category
- contact email

The 10 available points are shared equally across the three fields.

Scoring behavior:

- All 3 fields complete: **10.00 points**
- 2 fields complete: **6.67 points**
- 1 field complete: **3.33 points**
- No fields complete: **0.00 points**

A bio is considered complete when its value is `Yes`. A category is considered complete when it contains a non-empty value. Contact email availability is considered complete when its value is `Yes`.

The final score is rounded to two decimal places and cannot exceed 10 points.

## Design Justification

The scoring engine is designed to be deterministic, explainable, and suitable for a prototype creator-matching system.

### Deterministic

The same campaign, creator data, and benchmark data always produce the same score. The engine does not use randomness or hidden model behavior.

### Explainable

Each creator receives a numerical breakdown across five factors. A user can inspect exactly how engagement, follower fit, niche, location, and profile completeness contributed to the final score.

### Testable

Each scoring factor is implemented as a focused function with predictable inputs and outputs. Automated tests cover benchmark lookup, engagement scoring, follower-fit cases, niche relationships, location relationships, profile completeness, and final score consistency.

### Suitable for a Prototype

A rule-based approach is appropriate for the current challenge because the dataset is small and the scoring requirements are explicitly defined. It avoids adding unnecessary machine-learning complexity while still producing transparent and repeatable rankings.

## Known Limitations

The current implementation has several prototype limitations:

- The niche benchmark values are challenge-specific prototype data and are not claimed to be universal industry statistics.
- Related-niche relationships are manually defined and may not represent every real-world creator category.
- The city-region mapping covers only a limited set of cities and is not a complete geographic model.
- The profile-completeness score checks field availability but does not validate the quality or accuracy of the information.
- The scoring weights are fixed according to the current challenge requirements and are not dynamically configurable.

With more production data, these assumptions could be expanded using validated industry benchmarks, configurable campaign weights, broader taxonomy mappings, and more complete geographic data.
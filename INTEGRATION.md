# Production Integration Plan

## Current Prototype

The current prototype is a standalone Python scoring engine with a Streamlit interface. Creator data and niche benchmarks are stored in CSV files, and the `scoreCreator()` function calculates a 0–100 match score with a factor-level breakdown.

In a real AI-native CRM, the scoring logic would remain a separate, testable service or module, while creator and campaign data would come from the production system.

## Where and When the Scoring Engine Would Run

The most useful trigger would be event-based.

The scoring engine would run when:

* a campaign brief is created
* an existing campaign brief is updated
* a user explicitly requests or refreshes creator recommendations

For the minimum viable version, scoring could run synchronously inside the backend request. When a campaign manager asks for recommendations, the backend would retrieve eligible creators, call the scoring engine, rank the results, and return the top matches immediately.

A scheduled job would not be necessary for the first version because the main use case is generating recommendations for a specific campaign. However, scheduled rescoring could be added later when creator statistics, engagement rates, or profile information change regularly.

## What Must Exist First

Before integrating the prototype, the production system would need:

* a campaign record containing niche, follower range, minimum engagement rate, and target location
* a creator table containing follower count, engagement rate, niche, location, bio, category, and contact information
* a source for niche benchmark data
* a backend service capable of retrieving campaign and creator records

The minimum version would not require a job queue. The existing Python scoring module could be called directly from the backend.

## Minimum Viable Integration

The simplest integration flow would be:

1. A campaign manager creates or opens a campaign brief.
2. The frontend sends a recommendation request to the backend.
3. The backend loads the campaign, eligible creators, and niche benchmarks.
4. The backend calls `scoreCreator()` for each creator.
5. The results are sorted by total score.
6. The API returns the top creators with the numerical score breakdown.
7. The frontend displays the ranked recommendations and explanations.

For a small creator dataset, this could run synchronously through a REST API endpoint without additional infrastructure.

A practical stack could be:

* React frontend
* FastAPI backend
* PostgreSQL database
* existing Python scoring module
* Docker-based deployment

## More Ambitious Production Version

As the number of creators and campaigns grows, scoring could move to an asynchronous workflow.

A campaign-created or campaign-updated event could place a scoring task on a job queue. A worker would retrieve eligible creators, calculate rankings, and store the results in a recommendation table. The frontend could then read precomputed rankings instead of recalculating every request.

A larger production version could also include:

* automatic rescoring when important creator statistics change
* cached recommendations for frequently viewed campaigns
* versioned scoring rules and benchmark data
* audit logs showing how every recommendation was calculated
* monitoring for scoring failures and unusual score distributions
* configurable weights for different agencies or campaign types
* historical campaign outcomes to validate or improve the ranking model

This approach keeps the minimum integration simple while providing a clear path from the current standalone prototype to a scalable production recommendation system.

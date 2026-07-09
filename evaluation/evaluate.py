import pandas as pd

from src.scoring import scoreCreator


# Load data
creators = pd.read_csv("data/creators.csv")
campaigns = pd.read_csv("evaluation/campaigns.csv")
benchmarks = pd.read_csv("data/niche_benchmarks.csv")


allResults = []


# Evaluate every sample campaign
for campaignIndex, campaign in campaigns.iterrows():

    creators["score_result"] = creators.apply(
        lambda creator: scoreCreator(
            campaign,
            creator,
            benchmarks
        ),
        axis=1
    )

    creators["score"] = creators["score_result"].apply(
        lambda result: result["total"]
    )

    creators["breakdown"] = creators["score_result"].apply(
        lambda result: result["breakdown"]
    )


    # Rank and select top five creators
    topCreators = creators.sort_values(
        by="score",
        ascending=False
    ).head(5)


    # Save results as data
    for rank, (_, creator) in enumerate(
        topCreators.iterrows(),
        start=1
    ):

        breakdown = creator["breakdown"]

        allResults.append({
            "campaign_name": campaign["campaign_name"],
            "rank": rank,
            "creator_name": creator["name"],
            "score": creator["score"],
            "engagement_score": breakdown["engagementRate"],
            "follower_fit_score": breakdown["followerFit"],
            "niche_match_score": breakdown["nicheMatch"],
            "location_score": breakdown["location"],
            "completeness_score": breakdown["completeness"]
        })

    print(f"\n{campaign['campaign_name']}")

    print(
        topCreators[
            ["name", "score"]
        ]
    )

results = pd.DataFrame(allResults)

results.to_csv(
    "evaluation/results.csv",
    index=False
)

print(
    "\nEvaluation results saved to evaluation/results.csv"
)
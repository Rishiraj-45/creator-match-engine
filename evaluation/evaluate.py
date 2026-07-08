import pandas as pd

from src.scoring import calcTotalScore


creators = pd.read_csv("data/creators.csv")
campaigns = pd.read_csv("evaluation/campaigns.csv")

allResults = []

for campaignIndex, campaign in campaigns.iterrows():

    creators["score"] = creators.apply(
        lambda creator: calcTotalScore(
            creator["engagement_rate"],
            creator["followers"],
            creator["niche"],
            creator["location"],
            creator["bio"],
            creator["profile_picture"],
            campaign["min_followers"],
            campaign["max_followers"],
            campaign["niche"],
            campaign["location"]
        ),
        axis=1
    )

    topCreators = creators.sort_values(
        by="score",
        ascending=False
    ).head(5)
   
    for rank, (_, creator) in enumerate(topCreators.iterrows(),start=1):
        allResults.append({
        "campaign_name": campaign["campaign_name"],
        "rank": rank,
        "creator_name": creator["name"],
        "score": creator["score"]
    })
    print(f"\n{campaign['campaign_name']}")
    print(topCreators[["name", "score"]])

results = pd.DataFrame(allResults)

results.to_csv(
    "evaluation/results.csv",
    index=False
)

print("\nEvaluation results saved to evaluation/results.csv")
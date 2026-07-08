import pandas as pd

from src.scoring import calcTotalScore


creators = pd.read_csv("data/creators.csv")

campaign = {
    "minFollowers": 50000,
    "maxFollowers": 200000,
    "niche": "Fashion",
    "location": "Mumbai"
}
creators["score"] = creators.apply(
    lambda row: calcTotalScore(
        row["engagement_rate"],
        row["followers"],
        row["niche"],
        row["location"],
        row["bio"],
        row["profile_picture"],
        campaign["minFollowers"],
        campaign["maxFollowers"],
        campaign["niche"],
        campaign["location"]
    ),
    axis=1
)
rankedCreators=creators.sort_values(by='score',ascending=False)
print(rankedCreators[['name','score']])
import streamlit as st
import pandas as pd

from src.scoring import calcTotalScore, getScoreExplanation


creators = pd.read_csv("data/creators.csv")

st.title("Creator Match Engine")

st.write(
    "Find and rank the best creators for your campaign."
)

st.subheader("Campaign Brief")

minFollowers = st.number_input(
    "Minimum Followers",
    min_value=0,
    value=50000,
    step=10000
)

maxFollowers = st.number_input(
    "Maximum Followers",
    min_value=0,
    value=200000,
    step=10000
)
minimumEngagementRate = st.number_input(
    "Minimum Engagement Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=3.0,
    step=0.1
)
campaignNiche = st.selectbox(
    "Campaign Niche",
    ["Fashion", "Fitness", "Beauty", "Technology", "Gaming"]
)

campaignLocation = st.selectbox(
    "Campaign Location",
    ["Mumbai", "Delhi", "Bangalore"]
)

findButton = st.button("Find Top Creators")


if findButton:
    if minFollowers > maxFollowers:
        st.error(
            "Minimum followers cannot be greater than maximum followers."
        )
        st.stop()

    creators["score"] = creators.apply(
        lambda row: calcTotalScore(
            row["engagement_rate"],
            row["followers"],
            row["niche"],
            row["location"],
            row["bio"],
            row["profile_picture"],
            minFollowers,
            maxFollowers,
            campaignNiche,
            campaignLocation
        ),
        axis=1
    )

    creators["explanation"] = creators.apply(
        lambda row: getScoreExplanation(
            row["engagement_rate"],
            row["followers"],
            row["niche"],
            row["location"],
            row["bio"],
            row["profile_picture"],
            minFollowers,
            maxFollowers,
            campaignNiche,
            campaignLocation
        ),
        axis=1
    )

    topCreators = creators.sort_values(
        by="score",
        ascending=False
    ).head(5)

    st.subheader("Top 5 Creator Matches")

    st.dataframe(
        topCreators[["name", "score"]],
        hide_index=True
    )

    for index, row in topCreators.iterrows():

        st.markdown(
            f"### {row['name']} — {row['score']}/100"
        )

        for reason in row["explanation"]:
            st.write(f"- {reason}")
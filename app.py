import streamlit as st
import pandas as pd

from src.scoring import scoreCreator


# Load creator and benchmark data
creators = pd.read_csv("data/creators.csv")
benchmarks = pd.read_csv("data/niche_benchmarks.csv")


# Page title
st.title("Creator Match Engine")

st.write(
    "Find and rank the best creators for your campaign."
)

st.subheader("Campaign Brief")


# Minimum followers input
minFollowers = st.number_input(
    "Minimum Followers",
    min_value=0,
    value=50000,
    step=10000
)


# Maximum followers input
maxFollowers = st.number_input(
    "Maximum Followers",
    min_value=0,
    value=200000,
    step=10000
)


# Minimum engagement rate input
minimumEngagementRate = st.number_input(
    "Minimum Engagement Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=3.0,
    step=0.1
)


# Campaign niche input
campaignNiche = st.selectbox(
    "Campaign Niche",
    [
        "Fashion",
        "Fitness",
        "Beauty",
        "Technology",
        "Gaming",
        "Food"
    ]
)


# Campaign location input
campaignLocation = st.selectbox(
    "Campaign Location",
    [
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Kolkata"
    ]
)


# Find creators button
findButton = st.button("Find Top Creators")


if findButton:

    # Validate follower range
    if minFollowers > maxFollowers:
        st.error(
            "Minimum followers cannot be greater than maximum followers."
        )

    else:

        # Create campaign brief
        campaign = {
            "min_followers": minFollowers,
            "max_followers": maxFollowers,
            "minimum_engagement_rate": minimumEngagementRate,
            "niche": campaignNiche,
            "location": campaignLocation
        }


        # Score every creator
        creators["score_result"] = creators.apply(
            lambda row: scoreCreator(
                campaign,
                row,
                benchmarks
            ),
            axis=1
        )


        # Extract total score
        creators["score"] = creators["score_result"].apply(
            lambda result: result["total"]
        )


        # Extract numerical score breakdown
        creators["breakdown"] = creators["score_result"].apply(
            lambda result: result["breakdown"]
        )


        # Rank creators and select top five
        topCreators = creators.sort_values(
            by="score",
            ascending=False
        ).head(5)


        # Display ranking
        st.subheader("Top 5 Creator Matches")

        st.dataframe(
            topCreators[["name", "score"]],
            hide_index=True
        )


        # Display score breakdown for each creator
        for index, row in topCreators.iterrows():

            breakdown = row["breakdown"]

            st.markdown(
                f"### {row['name']} — {row['score']}/100"
            )

            st.write(
                f"Engagement Rate: "
                f"{breakdown['engagementRate']}/40"
            )

            st.write(
                f"Follower Fit: "
                f"{breakdown['followerFit']}/20"
            )

            st.write(
                f"Niche Match: "
                f"{breakdown['nicheMatch']}/20"
            )

            st.write(
                f"Location Match: "
                f"{breakdown['location']}/10"
            )

            st.write(
                f"Profile Completeness: "
                f"{breakdown['completeness']}/10"
            )

            st.divider()
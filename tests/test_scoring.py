import pandas as pd

from src.scoring import (
    getNicheBenchmark,
    calcEngagementScore,
    calFollowerScr,
    calNicheScr,
    calcLocationScr,
    calProfileScr,
    scoreCreator
)


benchmarks = pd.DataFrame({
    "niche": [
        "Fashion",
        "Beauty",
        "Fitness",
        "Technology",
        "Gaming",
        "Food"
    ],
    "average_engagement_rate": [
        3.5,
        3.0,
        4.0,
        2.5,
        3.5,
        4.0
    ]
})

def test_existing_niche_benchmark():
    assert getNicheBenchmark("Fashion", benchmarks) == 3.5


def test_missing_niche_uses_fallback():
    assert getNicheBenchmark("Travel", benchmarks) == 3.0


def test_engagement_meeting_requirement_gets_full_score():
    score = calcEngagementScore(
        4.5,
        "Fashion",
        4.0,
        benchmarks
    )

    assert score == 40.0


def test_engagement_below_requirement_is_proportional():
    score = calcEngagementScore(
        2.0,
        "Fashion",
        4.0,
        benchmarks
    )

    assert score == 20.0


def test_niche_benchmark_can_set_higher_requirement():
    score = calcEngagementScore(
        3.0,
        "Fitness",
        2.0,
        benchmarks
    )

    assert score == 30.0

def test_follower_scoring_cases():
    assert calFollowerScr(100000, 50000, 150000) == 20.0
    assert calFollowerScr(50000, 50000, 150000) == 10.0
    assert calFollowerScr(150000, 50000, 150000) == 10.0
    assert calFollowerScr(75000, 50000, 150000) == 15.0
    assert calFollowerScr(40000, 50000, 150000) == 0.0
    assert calFollowerScr(160000, 50000, 150000) == 0.0


def test_niche_scoring_cases():
    assert calNicheScr("Fashion", "Fashion") == 20.0
    assert calNicheScr("Beauty", "Fashion") == 10.0
    assert calNicheScr("Gaming", "Technology") == 10.0
    assert calNicheScr("Food", "Fashion") == 0.0


def test_location_scoring_cases():
    assert calcLocationScr("Mumbai", "Mumbai") == 10.0
    assert calcLocationScr("Pune", "Mumbai") == 5.0
    assert calcLocationScr("Delhi", "Mumbai") == 0.0


def test_profile_completeness_cases():
    assert calProfileScr("Yes", "Fashion", "Yes") == 10.0
    assert calProfileScr("Yes", "Fashion", "No") == 6.67
    assert calProfileScr("Yes", "", "No") == 3.33
    assert calProfileScr("No", "", "No") == 0.0

def test_perfect_creator_match():
    campaign = {
        "minimum_engagement_rate": 3.0,
        "min_followers": 50000,
        "max_followers": 150000,
        "niche": "Fashion",
        "location": "Mumbai"
    }

    creator = {
        "engagement_rate": 5.0,
        "followers": 100000,
        "niche": "Fashion",
        "location": "Mumbai",
        "bio": "Yes",
        "category": "Fashion",
        "contact_email": "Yes"
    }

    result = scoreCreator(campaign, creator, benchmarks)

    assert result["total"] == 100.0
    assert result["breakdown"]["engagementRate"] == 40.0
    assert result["breakdown"]["followerFit"] == 20.0
    assert result["breakdown"]["nicheMatch"] == 20.0
    assert result["breakdown"]["location"] == 10.0
    assert result["breakdown"]["completeness"] == 10.0


def test_total_equals_breakdown_sum_and_never_exceeds_100():
    campaign = {
        "minimum_engagement_rate": 4.0,
        "min_followers": 50000,
        "max_followers": 150000,
        "niche": "Fashion",
        "location": "Mumbai"
    }

    creator = {
        "engagement_rate": 2.0,
        "followers": 75000,
        "niche": "Beauty",
        "location": "Pune",
        "bio": "Yes",
        "category": "Beauty",
        "contact_email": "No"
    }

    result = scoreCreator(campaign, creator, benchmarks)

    assert result["total"] == round(
        sum(result["breakdown"].values()),
        2
    )
    assert result["total"] <= 100.0
import pandas as pd

def getNicheBenchmark(creatorNiche, benchmarks):
    matchingNiche = benchmarks[
        benchmarks["niche"].str.lower() == creatorNiche.lower()
    ]

    if matchingNiche.empty:
        return 3.0

    return matchingNiche.iloc[0]["average_engagement_rate"]
def calcEngagementScore(
    engagementRate,
    creatorNiche,
    minimumEngagementRate,
    benchmarks
):
    nicheBenchmark = getNicheBenchmark(creatorNiche, benchmarks)

    requiredEngagement = max(
        nicheBenchmark,
        minimumEngagementRate
    )

    if engagementRate >= requiredEngagement:
        return 40.0

    score = (engagementRate / requiredEngagement) * 40

    return float(round(max(0.0, score), 2))
def calcEngageScore(engagRate):
    if engagRate>=6:
        return 40
    elif engagRate >=4:
        return 32
    elif engagRate >=2:
        return 24
    else:
        return 12

def calFollowerScr(followers, minFollowers, maxFollowers):
    if followers < minFollowers or followers > maxFollowers:
        return 0.0
    if minFollowers == maxFollowers:
     return 20.0


    midpoint = (minFollowers + maxFollowers) / 2
    halfRange = (maxFollowers - minFollowers) / 2

    if followers <= midpoint:
        distanceFromMidpoint = midpoint - followers
    else:
        distanceFromMidpoint = followers - midpoint

    score = 20 - (distanceFromMidpoint / halfRange) * 10

    return float(round(score, 2))

def calNicheScr(creatorNiche, campaignNiche):
    creatorNiche = creatorNiche.lower()
    campaignNiche = campaignNiche.lower()

    if creatorNiche == campaignNiche:
        return 20.0

    relatedNiches = {
        "fashion": ["beauty", "fitness"],
        "beauty": ["fashion"],
        "fitness": ["fashion"],
        "technology": ["gaming"],
        "gaming": ["technology"],
        "food": []
    }

    if creatorNiche in relatedNiches.get(campaignNiche, []):
        return 10.0

    return 0.0

def calcLocationScr(creatorLocation, campaignLocation):
    creatorLocation = creatorLocation.lower()
    campaignLocation = campaignLocation.lower()

    if creatorLocation == campaignLocation:
        return 10.0

    regions = {
        "west": ["mumbai", "pune", "ahmedabad"],
        "north": ["delhi", "jaipur", "chandigarh"],
        "south": ["bangalore", "chennai", "hyderabad"],
        "east": ["kolkata", "bhubaneswar", "guwahati"]
    }

    creatorRegion = None
    campaignRegion = None

    for region, cities in regions.items():
        if creatorLocation in cities:
            creatorRegion = region

        if campaignLocation in cities:
            campaignRegion = region

    if creatorRegion is not None and creatorRegion == campaignRegion:
        return 5.0

    return 0.0

def calProfileScr(bio, category, contactEmail):
    completedFields = 0

    if str(bio).lower() == "yes":
        completedFields += 1

    if str(category).strip() != "":
        completedFields += 1

    if str(contactEmail).lower() == "yes":
        completedFields += 1

    score = (completedFields / 3) * 10

    return float(round(score, 2))

def scoreCreator(campaign, creator, benchmarks):
    engagementScore = calcEngagementScore(
        creator["engagement_rate"],
        creator["niche"],
        campaign["minimum_engagement_rate"],
        benchmarks
    )

    followerScore = calFollowerScr(
        creator["followers"],
        campaign["min_followers"],
        campaign["max_followers"]
    )

    nicheScore = calNicheScr(
        creator["niche"],
        campaign["niche"]
    )

    locationScore = calcLocationScr(
        creator["location"],
        campaign["location"]
    )

    completenessScore = calProfileScr(
        creator["bio"],
        creator["category"],
        creator["contact_email"]
    )

    breakdown = {
        "engagementRate": engagementScore,
        "followerFit": followerScore,
        "nicheMatch": nicheScore,
        "location": locationScore,
        "completeness": completenessScore
    }

    totalScore = sum(breakdown.values())

    return {
        "total": float(round(totalScore, 2)),
        "breakdown": breakdown
    }

def calcTotalScore(
    engagementRate,
    followers,
    creatorNiche,
    creatorLocation,
    bio,
    profilePicture,
    minFollowers,
    maxFollowers,
    campaignNiche,
    campaignLocation
):
    engagementScore = calcEngageScore(engagementRate)
    followerScore = calFollowerScr(followers, minFollowers, maxFollowers)
    nicheScore = calNicheScr(creatorNiche, campaignNiche)
    locationScore = calcLocationScr(creatorLocation, campaignLocation)
    profileScore = calProfileScr(bio, profilePicture)

    totalScore = (
        engagementScore
        + followerScore
        + nicheScore
        + locationScore
        + profileScore
    )

    return totalScore

def getScoreExplanation(
    engagementRate,
    followers,
    creatorNiche,
    creatorLocation,
    bio,
    profilePicture,
    minFollowers,
    maxFollowers,
    campaignNiche,
    campaignLocation
):
    explanations = []

    if engagementRate >= 6:
        explanations.append("Excellent engagement rate")
    elif engagementRate >= 4:
        explanations.append("Good engagement rate")
    elif engagementRate >= 2:
        explanations.append("Average engagement rate")
    else:
        explanations.append("Low engagement rate")

    if minFollowers <= followers <= maxFollowers:
        explanations.append("Follower count fits the campaign")
    else:
        explanations.append("Follower count is outside the campaign range")

    if creatorNiche.lower() == campaignNiche.lower():
        explanations.append("Niche matches the campaign")
    else:
        explanations.append("Niche does not match the campaign")

    if creatorLocation.lower() == campaignLocation.lower():
        explanations.append("Location matches the campaign")
    else:
        explanations.append("Location does not match the campaign")

    if bio.lower() == "yes" and profilePicture.lower() == "yes":
        explanations.append("Profile is complete")
    else:
        explanations.append("Profile is incomplete")

    return explanations
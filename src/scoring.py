def calcEngageScore(engagRate):
    if engagRate>=6:
        return 40
    elif engagRate >=4:
        return 32
    elif engagRate >=2:
        return 24
    else:
        return 12

def calFollowerScr(followers,minFollowers,maxFollowers):
    if followers>=minFollowers and followers<=maxFollowers:
        return 20
    else:
        return 0

def calNicheScr(creatorNiche, campaignNiche):
    if creatorNiche.lower() == campaignNiche.lower():
        return 20
    else:
        return 0

def calcLocationScr(creatorLocation, campaignLocation):
    if creatorLocation.lower() == campaignLocation.lower():
        return 10
    else:
        return 0

def calProfileScr(bio, profilePicture):
    score = 0

    if bio.lower() == "yes":
        score += 5

    if profilePicture.lower() == "yes":
        score += 5

    return score

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
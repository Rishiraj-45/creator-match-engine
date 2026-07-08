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


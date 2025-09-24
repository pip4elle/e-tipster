from config import *
from datetime import datetime
import pytz, json, requests
from tqdm import tqdm
from collections import OrderedDict


def getTodayMatches():
    print("PRENDENDO PARTITE...")

    todayDate = datetime.now(pytz.timezone('Europe/Rome')).strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?timezone={TZ}&date={todayDate}&status=NS"

    response = requests.request("GET", url, headers=HEADERS)

    matchesList = json.loads(response.text)

    fixtures = []

    for match in matchesList["response"]:
        # checks if any of the values in LEAGUES matches the league name of the match ;)
        if LEAGUES_ENABLED:
            if any(league in match["league"]["name"] for league in LEAGUES):
                fixtures.append(match)
            continue

        fixtures.append(match)

    return fixtures


def filterMatches(matchesList):
    filteredMatches = []

    for match in tqdm(matchesList, desc="FILTRANDO PARTITE", unit="match"):
        playingTeams = match["teams"]

        homeTeamID = playingTeams["home"]["id"]
        awayTeamID = playingTeams["away"]["id"]

        if checkTeam(homeTeamID) and checkTeam(awayTeamID):
            filteredMatches.append(match)

    return filteredMatches

        
def checkTeam(teamID):
    url = f"https://v3.football.api-sports.io/fixtures?team={teamID}&last={LAST_MATCHES_NUM}"

    response = requests.request("GET", url, headers=HEADERS)

    matchesList = json.loads(response.text)

    for match in matchesList["response"]:
        try:
            totalGoals = getTotalGoals(match)
        except:
            return False

        if totalGoals >= MIN_TOT_GOALS:
            continue

        return False

    return True


def getTotalGoals(match):
    return match["goals"]["home"] + match["goals"]["away"]


def createTicket(matchesList):
    matchOddsDict = {}

    for match in matchesList:
        fixtureID = match["fixture"]["id"]

        url = f"https://v3.football.api-sports.io/odds?bet={BET_TYPE}&fixture={fixtureID}&bookmaker={BOOKMAKER}"

        response = requests.request("GET", url, headers=HEADERS)
        
        oddsList = json.loads(response.text)
        
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        matchKey = f"{home} VS {away}"   

        for resp in oddsList["response"]:
            for bookmaker in resp["bookmakers"]:
                for bet in bookmaker["bets"]:
                    for odd in bet["values"]:
                        if "Over 1.5" in odd["value"]:
                            matchOddsDict[matchKey] = float(odd["odd"])

    return createTicketFromMultiplier(matchOddsDict, MULTIPLIER)


def createTicketFromMultiplier(matchOddsDict, multiplier):
    orderedDict = dict(sorted(matchOddsDict.items(), key=lambda x: x[1], reverse=True))

    finalDict = {}

    multiplierCount = 1

    for match, odd in orderedDict.items():
        multiplierCount *= odd

        finalDict[match] = odd

        if multiplierCount < multiplier:
            continue

        break

    return finalDict

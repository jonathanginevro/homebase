from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.
def index(request):

    response=requests.get('https://statsapi.mlb.com/api/v1/standings?leagueId=103,104').json()

    records = []

    abb_dict = {}
    teams=requests.get('https://statsapi.mlb.com/api/v1/teams?sportId=1').json()
    for team in teams['teams']:
        abb_dict[team["id"]] = team["abbreviation"]

    div_dict = {201: "AL East", 204: "NL East", 202: "AL Central", 205: "NL Central", 200: "AL West", 203: "NL West"}

    for division in response['records']:

        division_dict = {}
        division_dict["name"] = div_dict[division['division']['id']]
        division_dict["teamRecords"] = []

        for team in division['teamRecords']:
            team_dict = {}

            team_dict["abb_name"] = abb_dict[team['team']['id']]
            team_dict["id"] = team['team']['id']
            team_dict["W"] = team["wins"]
            team_dict["L"] = team["losses"]
            team_dict["Pct"] = team["winningPercentage"]
            team_dict["GB"] = team["wildCardGamesBack"]
            team_dict["L10"] = str(team["records"]["splitRecords"][8]["wins"]) + "-" + str(team["records"]["splitRecords"][8]["losses"])
            team_dict["DIFF"] = team["runDifferential"]

            division_dict['teamRecords'].append(team_dict)

        div_dict[division['division']['id']] = division_dict

    for key in div_dict.keys():
        records.append(div_dict[key])

    raw = requests.get('https://www.mlb.com/feeds/news/rss.xml')
    soup = BeautifulSoup(raw.content, 'xml')
    articles = soup.findAll('item')

    article_collect = []
    for article in articles:
        art={
            "title" : article.title.text,
            "date" : article.pubDate.text[5:],
            "author" : article.creator.text if article.creator.text != "" else "Anonymous",
            "link" : article.link.text,
            "img" : article.image['href'],
        }
        article_collect.append(art)

    return render(request,'index.html',{
                                'response': records,
                                'stories': article_collect
                            })

def index2(request, team_id):

    team = requests.get('https://statsapi.mlb.com/api/v1/teams/' + str(team_id)).json()
    roster = requests.get('https://statsapi.mlb.com/api/v1/teams/' + str(team_id) + '/roster/Active?hydrate=person(stats(type=season))').json()
    standings = requests.get('https://statsapi.mlb.com/api/v1/standings?leagueId=103,104').json()

    division = requests.get('https://statsapi.mlb.com/api/v1/divisions/' + str(team['teams'][0]["division"]["id"])).json()

    hitters = []
    pitchers = []

    sorted_standing = {}

    for player in roster['roster']:
        player_dict = {}

        player_dict['Id'] = player["person"]["id"]
        player_dict['Pos'] = player["position"]["abbreviation"]
        player_dict['Num'] = player["jerseyNumber"]
        player_dict['First'] = player["person"]["firstName"]
        player_dict['Last'] = player["person"]["lastName"]
        player_dict['Age'] = player["person"]["currentAge"]

        if player["position"]["abbreviation"] == "P":
            stats = player["person"]["stats"][0]["splits"][0]["stat"] if "stats" in player["person"] else "N/A"
            stats2 = player["person"]["stats"][0]["splits"][0] if "stats" in player["person"] else "N/A"

            player_dict['T'] = stats2["gameType"] if "gameType" in stats2 else "N/A"
            player_dict['IP'] = stats["inningsPitched"] if "inningsPitched" in stats else "N/A"
            player_dict['ERA'] = stats["era"] if "era" in stats else "N/A"
            player_dict['SO'] = stats["strikeOuts"] if "strikeOuts" in stats else "N/A"
            player_dict['BB'] = stats["baseOnBalls"] if "baseOnBalls" in stats else "N/A"
            player_dict['SOPer'] = round((stats["strikeOuts"] / stats["battersFaced"]) * 100, 1) if "atBats" and "strikeOuts" in stats else "N/A"
            player_dict['BBPer'] = round((stats["baseOnBalls"] / stats["battersFaced"]) * 100, 1) if "atBats" and "baseOnBalls" in stats else "N/A"
            player_dict['HRPer9'] = stats["homeRunsPer9"] if "homeRunsPer9" in stats else "N/A"
            player_dict['OPS'] = stats["ops"] if "ops" in stats else "N/A"
            pitchers.append(player_dict)
        else:
            stats = player["person"]["stats"][0]["splits"][0]["stat"] if "stats" in player["person"] else "N/A"

            player_dict['B'] = player["person"]["batSide"]["code"]
            player_dict['T'] = player["person"]["pitchHand"]["code"]

            player_dict['PA'] = stats["plateAppearances"] if "plateAppearances" in stats else "N/A"
            player_dict['H'] = stats["hits"] if "hits" in stats else "N/A"
            player_dict['2B'] = stats["doubles"] if "doubles" in stats else "N/A"
            player_dict['3B'] = stats["triples"] if "triples" in stats else "N/A"
            player_dict['HR'] = stats["homeRuns"] if "homeRuns" in stats else "N/A"
            player_dict['SB'] = stats["stolenBases"] if "stolenBases" in stats else "N/A"
            player_dict['SOPer'] = round((stats["strikeOuts"] / stats["atBats"]) * 100, 1) if "atBats" and "strikeOuts" in stats else "N/A"
            player_dict['BBPer'] = round((stats["baseOnBalls"] / stats["atBats"]) * 100, 1) if "atBats" and "baseOnBalls" in stats else "N/A"
            player_dict['AVG'] = stats["avg"] if "avg" in stats else "N/A"
            player_dict['OBP'] = stats["obp"] if "obp" in stats else "N/A"
            player_dict['OPS'] = stats["ops"] if "ops" in stats else "N/A"
            hitters.append(player_dict)

    for a in standings["records"]:
        for b in a['teamRecords']:
            sorted_standing[b['team']['id']] = b

    return render(request,'team.html', {
                                            'team': team['teams'][0],
                                            'hitters': hitters,
                                            'pitchers': pitchers,
                                            'standings': sorted_standing[int(team_id)],
                                            'division': division["divisions"][0]["nameShort"],
                                            'ending': ending(sorted_standing[int(team_id)]['divisionRank'])
                                        })

def index3(request, team_id, player_id):
    player = requests.get('https://statsapi.mlb.com/api/v1/people/' + str(player_id) + '?hydrate=stats(group=[hitting,pitching,fielding],type=[yearByYear])').json()
    team = requests.get('https://statsapi.mlb.com/api/v1/teams/' + str(team_id)).json()
    allteams = requests.get('https://statsapi.mlb.com/api/v1/teams?sportId=1').json()

    abb_dict = {}

    for team1 in allteams["teams"]:
        abb_dict[team1["id"]] = team1["abbreviation"]

    player_dict = {}
    yearbook = []

    player_dict["Name"] = player["people"][0]["fullName"]
    player_dict["Id"] = player["people"][0]["id"]
    player_dict["Team"] = team["teams"][0]["name"]
    player_dict["TeamId"] = team["teams"][0]["id"]
    player_dict["B"] = player["people"][0]["batSide"]["code"]
    player_dict["T"] = player["people"][0]["pitchHand"]["code"]
    player_dict["Age"] = player["people"][0]["currentAge"]
    player_dict["H"] = player["people"][0]["height"]
    player_dict["W"] = player["people"][0]["weight"]
    player_dict["Drafted"] = player["people"][0]["draftYear"] if "draftYear" in player["people"][0] else "N/A"
    player_dict["Position"] = player["people"][0]["primaryPosition"]["abbreviation"]

    if player_dict["Position"] == "P" and "stats" in player["people"][0]:

        for group in player["people"][0]["stats"]:

            if group["group"]["displayName"] == "pitching":

                splits = group['splits']
                for year in splits:
                    stat_dict = {}

                    stat_dict["Year"] = year["season"] if "season" in year else "N/A"
                    stat_dict["TeamId"] = year["team"]["id"] if "team" in year else "Combined"
                    stat_dict["Team"] = abb_dict[year["team"]["id"]] if "team" in year else "Combined"
                    stat_dict["G"] = year['stat']["gamesPlayed"] if "gamesPlayed" in year['stat'] else "N/A"
                    stat_dict["IP"] = year['stat']["inningsPitched"] if "inningsPitched" in year['stat'] else "N/A"
                    stat_dict["W"] = year['stat']["wins"] if "wins" in year['stat'] else "N/A"
                    stat_dict["L"] = year['stat']["losses"] if "losses" in year['stat'] else "N/A"
                    stat_dict["SV"] = year['stat']["saves"] if "saves" in year['stat'] else "N/A"
                    stat_dict["ERA"] = year['stat']["era"] if "era" in year['stat'] else "N/A"
                    stat_dict["WHIP"] = year['stat']["whip"] if "whip" in year['stat'] else "N/A"
                    stat_dict["H"] = year['stat']["hits"] if "hits" in year['stat'] else "N/A"
                    stat_dict["R"] = year['stat']["runs"] if "runs" in year['stat'] else "N/A"
                    stat_dict["SO"] = year['stat']["strikeOuts"] if "strikeOuts" in year['stat'] else "N/A"
                    stat_dict["BB"] = year['stat']["baseOnBalls"] if "baseOnBalls" in year['stat'] else "N/A"
                    stat_dict["HRPer9"] = year['stat']["homeRunsPer9"] if "homeRunsPer9" in year['stat'] else "N/A"
                    stat_dict["OPS"] = year['stat']["ops"] if "ops" in year['stat'] else "N/A"

                    yearbook.append(stat_dict)

    elif "stats" in player["people"][0]:

        for group in player["people"][0]["stats"]:

            if group["group"]["displayName"] == "hitting":

                splits = group['splits']
                for year in splits:
                    stat_dict = {}

                    stat_dict["Year"] = year["season"] if "season" in year else "N/A"
                    stat_dict["TeamId"] = year["team"]["id"] if "team" in year else "Combined"
                    stat_dict["Team"] = abb_dict[year["team"]["id"]] if "team" in year else "Combined"
                    stat_dict["G"] = year['stat']["gamesPlayed"] if "gamesPlayed" in year['stat'] else "N/A"
                    stat_dict["PA"] = year['stat']["plateAppearances"] if "plateAppearances" in year['stat'] else "N/A"
                    stat_dict["AB"] = year['stat']["atBats"] if "atBats" in year['stat'] else "N/A"
                    stat_dict["R"] = year['stat']["runs"] if "runs" in year['stat'] else "N/A"
                    stat_dict["H"] = year['stat']["hits"] if "hits" in year['stat'] else "N/A"
                    stat_dict["2B"] = year['stat']["doubles"] if "doubles" in year['stat'] else "N/A"
                    stat_dict["3B"] = year['stat']["triples"] if "triples" in year['stat'] else "N/A"
                    stat_dict["HR"] = year['stat']["homeRuns"] if "homeRuns" in year['stat'] else "N/A"
                    stat_dict["RBI"] = year['stat']["rbi"] if "rbi" in year['stat'] else "N/A"
                    stat_dict["SB"] = year['stat']["stolenBases"] if "stolenBases" in year['stat'] else "N/A"
                    stat_dict["BB"] = year['stat']["baseOnBalls"] if "baseOnBalls" in year['stat'] else "N/A"
                    stat_dict["SO"] = year['stat']["strikeOuts"] if "strikeOuts" in year['stat'] else "N/A"
                    stat_dict["OBP"] = year['stat']["obp"] if "obp" in year['stat'] else "N/A"
                    stat_dict["SLG"] = year['stat']["slg"] if "slg" in year['stat'] else "N/A"
                    stat_dict["OPS"] = year['stat']["ops"] if "ops" in year['stat'] else "N/A"

                    yearbook.append(stat_dict)
    
    return render(request,'player.html', {
                                            'player': player_dict,
                                            'stats': yearbook
                                            })

def ending(input: str):
    
    if input == "1":
        return "st"
    elif input == "2":
        return "nd"
    elif input == "3":
        return "rd"
    else:
        return "th"

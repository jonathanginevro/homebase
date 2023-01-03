from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    response=requests.get('https://statsapi.mlb.com/api/v1/teams?sportId=1').json()

    AL_EAST = []
    AL_WEST = []

    for item in response['teams']:
        if item['division']['id'] == 201:
            AL_EAST.append(item)

    return render(request,'index.html',{'response':AL_EAST})

def index2(request, team_id):
    team = requests.get('https://statsapi.mlb.com/api/v1/teams/' + str(team_id)).json()
    roster = requests.get('https://statsapi.mlb.com/api/v1/teams/' + str(team_id) + '/roster').json()

    return render(request,'team.html', {
                                            'team': team['teams'][0],
                                            'roster':roster['roster']
                                          })

def index3(request, player_id):
    player = requests.get('https://statsapi.mlb.com/api/v1/people/' + str(player_id)).json()
    
    return render(request,'player.html', {'player': player['people'][0]})


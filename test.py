import requests

BASE_URL = "https://api.server.nbaapi.com/api/playertotals"
ADVANCED_URL = "https://api.server.nbaapi.com/api/playeradvancedstats"


def find_player_id(player_name, season=2025):
    """Find player ID by searching all players in the season"""
    BASE_URL = "https://api.server.nbaapi.com/api/playertotals"
    headers = {"accept": "application/json"}
    
    page = 1
    while page <= 20:  # Safety limit
        params = {
            "page": page,
            "pageSize": 1000,
            "season": season,
        }
        
        response = requests.get(BASE_URL, params=params, headers=headers)
        if response.status_code != 200:
            break
            
        data = response.json()
        players = data.get("data", [])
        
        if not players:
            break
            
        for player in players:
            if player.get('playerName', '').lower() == player_name.lower():
                return player.get('playerId')
                
        page += 1
    
    return None

def test_find_specific_player():
    """Test to find a specific player's ID - CHANGE THE NAME HERE"""
    
    # *** CHANGE THIS PLAYER NAME TO WHOEVER YOU WANT TO TEST ***
    player_name = "Kevin Durant"
    
    player_id = find_player_id(player_name)
    
    print(f"\nPlayer: {player_name}")
    print(f"Player ID: {player_id}")
    
    assert player_id is not None, f"Could not find player ID for {player_name}"


###################################################################################################33

def buildPlayerIdStart(player_name):
        names = player_name.split(" ")
        first_name = names[0]
        last_name = names[1]

        if len(first_name) > 2:
            first_name_id = first_name[0:2]
        else:
            first_name_id = first_name

        if len(last_name) > 5:
            last_name_id = last_name[0:5]
        else:
            last_name_id = last_name

        id = last_name_id.lower() + first_name_id.lower()
        return id

def get_player_stats_test(player_name, season=2025):
    headers = {"accept": "application/json"}

    # These store all potential matches
    player_stats = {}
    advanced_stats = {}

    looking_for_player = True
    iteration = 1

    playerId = ''

    while looking_for_player:
        startingId = buildPlayerIdStart(player_name)
        id = f"{startingId}0{iteration}"

        params = {
            "page": 1,
            "pageSize": 1000,
            "season": season,
            "playerId": id,
        }

        response = requests.get(BASE_URL, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            player_data_list = data.get('data', [])
            if player_data_list:
                player_data = player_data_list[0]  # Will get 2 responses for 1 player, first is regular season, second is playoffs
                if player_data['playerName'] == player_name:
                    player_stats = player_data
                    playerId = id
                    looking_for_player = False
                else:
                    iteration += 1
            else:
                iteration += 1
        else:
            iteration += 1

    # Player data 
    params = {
            "page": 1,
            "pageSize": 1000,
            "season": season,
            "playerId": playerId,
        }
    advanced_response = requests.get(ADVANCED_URL, params=params, headers=headers)
    if advanced_response.status_code == 200:
        advanced_data = advanced_response.json()
        player_advanced_data_list = advanced_data.get('data', [])
        if player_advanced_data_list:
            player_advanced_data = player_advanced_data_list[0]
            advanced_stats = player_advanced_data


    relevant_stats = {
        "position": player_stats['position'],
        "minutespg": player_stats['minutesPg'],
        "fg%": player_stats['fieldPercent'],
        "3%": player_stats['threePercent'],
        "ft%": player_stats['ftPercent'],
        "efg%": player_stats['effectFgPercent'],
        "2attempts": player_stats['twoAttempts'],
        "2made": player_stats['twoFg'],
        "3attempts": player_stats['threeAttempts'],
        "3made": player_stats['threeFg'],
        "ftAttempts": player_stats['ftAttempts'],
        "ft": player_stats['ft'],
        "points": player_stats['points'],
        "rebounds": player_stats['totalRb'],
        "offensiveRebounds": player_stats['offensiveRb'],
        "defensiveRebounds": player_stats['defensiveRb'],
        "assists": player_stats['assists'],
        "steals": player_stats['steals'],
        "blocks": player_stats['blocks'],
        "turnovers": player_stats['turnovers'],
        "fouls": player_stats['personalFouls'],
        "games": player_stats['games'],
    }

    if advanced_stats:
            relevant_stats.update({
                "total_minutes": advanced_stats['minutesPlayed'],
                "ts%": advanced_stats['tsPercent'],
                "rebound%": advanced_stats['totalRBPercent'],
                "offensiveRbPercent": advanced_stats['offensiveRBPercent'],
                "defensiveRbPercent": advanced_stats['defensiveRBPercent'],
                "usage%": advanced_stats['usagePercent'],
                "offensePlusMinus": advanced_stats['offensiveBox'],
                "defensivePlusMinus": advanced_stats['defensiveBox'],
                "plusMinus": advanced_stats['box'],
                "steal%": advanced_stats['stealPercent'],
                "block%": advanced_stats['blockPercent'],
                "turnover%": advanced_stats['turnoverPercent'],
            })

    return relevant_stats


if __name__ == "__main__":
    #test_find_specific_player()
    print(get_player_stats_test('LeBron James'))
import requests

BASE_URL = "https://api.server.nbaapi.com/api/playertotals"
ADVANCED_URL = "https://api.server.nbaapi.com/api/playeradvancedstats"

class grabPlayerData:

    # Returns a list of potential player IDs with the first 5 digits of last name + first 2 digits 
    # of first name, adding 01,02,03,04, and 05 to the end and hoping one of those is the correct player.
    # Handles if multiple players have similar ID in get_player_stats function
    def get_potential_player_ids(self, player_name):
        names = player_name.split(" ")
        first_name = names[0]
        last_name = names[1]
        
        if len(last_name) > 5:
            last_name_id = last_name[0:5]
        else:
            last_name_id = last_name

        if len(first_name) > 2:
            first_name_id = first_name[0:2]
        else:
            first_name_id = first_name

        id = last_name_id.lower() + first_name_id.lower()

        potential_ids = []
        potential_ids.append(id + '01')
        potential_ids.append(id + '02')
        potential_ids.append(id + '03')
        potential_ids.append(id + '04')
        potential_ids.append(id + '05')

        return potential_ids

    def get_player_stats(self, player_name, season=2025):
        headers = {"accept": "application/json"}

        potential_player_ids = self.get_potential_player_ids(player_name)

        # These store all potential matches
        potential_player_stats = {}
        potential_player_advanced_stats = {}

        for playerId in potential_player_ids:

            params = {
                "page": 1,
                "pageSize": 1000,
                "season": season,
                "playerId": playerId,
            }
            
            # Get the season totals
            response = requests.get(BASE_URL, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                players_list = data.get("data", [])
                for player in players_list:
                    potential_player_stats[player['playerName']] = player
            else:
                print(f'No player matches the playerId of: {playerId}')

            # Get the advanced stats
            advancedResponse = requests.get(ADVANCED_URL, params=params, headers=headers)
            if advancedResponse.status_code == 200:
                data = advancedResponse.json()
                advanced_player_list = data.get("data", [])
                for player in advanced_player_list:
                    potential_player_advanced_stats[player['playerName']] = player
            else:
                print(f"No advanced stats found for playerId: {playerId}")


        # If there are no matches
        if not potential_player_stats:
            print(f"No stats found for any potential ID for the player {player_name}")
            return {}
        
        # If there is exactly one match (the correct player)
        if len(potential_player_stats) == 1:
            player_name_key = list(potential_player_stats.keys())[0]
            playerStats = potential_player_stats[player_name_key]
        
        # If there is more than one match, find the correct player by name
        else:
            playerStats = None
            player_name_key = None
            for pname, player in potential_player_stats.items():
                if pname.lower() == player_name.lower():
                    playerStats = player
                    player_name_key = pname
                    break
            if not playerStats:
                print('issue finding player based on the id')
                return {}
            
        advanced_stats = potential_player_advanced_stats.get(player_name_key, {})
        if not advanced_stats:
            print(f"Warning: No advanced stats found for {player_name_key}")

        relevant_stats = {
                    "position": playerStats['position'],
                    "minutespg": playerStats['minutesPg'],
                    "fg%": playerStats['fieldPercent'],
                    "3%": playerStats['threePercent'],
                    "ft%": playerStats['ftPercent'],
                    "efg%": playerStats['effectFgPercent'],
                    "2attempts": playerStats['twoAttempts'],
                    "2made": playerStats['twoFg'],
                    "3attempts": playerStats['threeAttempts'],
                    "3made": playerStats['threeFg'],
                    "ftAttempts": playerStats['ftAttempts'],
                    "ft": playerStats['ft'],
                    "points": playerStats['points'],
                    "rebounds": playerStats['totalRb'],
                    "offensiveRebounds": playerStats['offensiveRb'],
                    "defensiveRebounds": playerStats['defensiveRb'],
                    "assists": playerStats['assists'],
                    "steals": playerStats['steals'],
                    "blocks": playerStats['blocks'],
                    "turnovers": playerStats['turnovers'],
                    "fouls": playerStats['personalFouls'],
                    "games": playerStats['games'],
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


    def get_team_stats(self, players, season=2025):

        if len(players) != 5:
            return "Enter 5 players"

        teamStats = {}

        for player in players:
            player_stats = self.get_player_stats(player)
            if player_stats:
                teamStats[player] = player_stats
            else:
                return "Problem with one of the players stats"

        return teamStats
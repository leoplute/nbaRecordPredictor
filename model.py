import requests
import json
import math
import itertools

BASE_URL = "https://api.server.nbaapi.com/api/playertotals"

class FantasyModel:

    def predict_record(self, team_fingerprint):

        total_score = 0
        for player_name,fingerprint in team_fingerprint.items():
            for ability, score in fingerprint.items():
                total_score += score

        normalized_score = total_score / 20

        # Map normalized_score [0..1] to wins [20..60]
        wins = int(normalized_score * (70 - 10) + 10)

        return wins

    def check_redundancy(self, team_fingerprints, threshold = 0.2):

        warnings = []

        player_pairs = itertools.combinations(team_fingerprints.items(), 2)
    
        for (player1_name, fp1), (player2_name, fp2) in player_pairs:
            # Calculate Euclidean distance between their fingerprints
            sum_sq = 0
            for ability in fp1:
                diff = fp1[ability] - fp2[ability]
                sum_sq += diff * diff
            distance = math.sqrt(sum_sq)
        
            if distance < threshold:
                warnings.append(f"Players '{player1_name}' and '{player2_name}' have very similar playing styles (distance: {distance:.3f})")

        return warnings

    def check_synergy(self, team_fingerprints):
        # Take in 5 'fingerprints'

        synergy_statement = "Thank you for inputting you team."

        team_abilities = {
            'scoring_ability': 0,
            'playmaking': 0,
            'rebounding': 0,
            'defense': 0,
        }
        # Add up everyones stats to get collective strengths + weaknesses
        for player_name, fingerprint in team_fingerprints.items():
            for ability, score in fingerprint.items():
                team_abilities[ability] += score

        synergy_statement += '\nHere is a breakdown of your team: '
        
        # Check to make sure scoring is in the sweet spot
        if team_abilities['scoring_ability'] <= 2:
            synergy_statement += '\n - The teams scoring ability is not good enough'

        if team_abilities['scoring_ability'] >= 3.5:
            synergy_statement += '\n - Too many scorers on the team'

        # Check to make sure playmaking is in the sweet spot
        if team_abilities['playmaking'] <= 2:
            synergy_statement += '\n - The teams playmaking is not good enough'

        if team_abilities['playmaking'] >= 3.5:
            synergy_statement += '\n - Too much playmaking'


        # !!!!! MAKE SURE THAT HIGH REBOUNDING/DEFENSE DOESN'T MEAN A TRADEOFF

        # Never too much rebounding
        if team_abilities['rebounding'] <= 2:
            synergy_statement += '\n - The teams rebounding is not good enough'

        # Never too much defense
        if team_abilities['defense'] <= 2:
            synergy_statement += '\n - The teams defense is not good enough'

        redundancies = self.check_redundancy(team_fingerprints)
        if redundancies:
            synergy_statement += "\nHere are some players who might be redundant to have on the team:"
            for warning in redundancies:
                synergy_statement += f"\n - {warning}"


        # Look for concerning player profiles ( ex : no player w/ high playmaking/scoring )

        synergy_statement += "\nHere is a breakdown of any player with unique player profiles:"

        high = 0.6
        mid = 0.4
        low = 0.2

        elite_scorers = 0
        elite_playmakers = 0
        elite_rebounders = 0
        elite_defenders = 0

        for player_name, fingerprint in team_fingerprints.items():
            scoring = fingerprint['scoring_ability']
            playmaking = fingerprint['playmaking']
            rebounding = fingerprint['rebounding']
            defense = fingerprint['defense']
            
            if scoring >= high:
                elite_scorers += 1

            if playmaking >= high:
                elite_playmakers += 1

            if rebounding >= high:
                elite_rebounders += 1

            if defense >= high:
                elite_defenders += 1

            if scoring <= low and playmaking <= low and rebounding <= low and defense <= low:
                synergy_statement += f"\n - {player_name}, Not a good player. Low on everything"

            if scoring >= high and playmaking <= low and rebounding <= low and defense <= low:
                synergy_statement += f"\n - {player_name}, High volume scorer, but thats all."

            if scoring <= low and playmaking <= low and rebounding <= low and defense >= high:
                synergy_statement += f"\n - {player_name}, Great defender, thats about it"

            if scoring > low and playmaking > low and rebounding > low and defense > low and scoring < high and playmaking < high and rebounding < high and defense < high:
                synergy_statement += f"\n - {player_name}, Very average, not bad at anything, but not great at anything either"


        # Make sure the team has an elite scorer, playmaker, rebounder, and defender
        synergy_statement += "\nLets make sure the team has an elite player for everything:"

        if elite_scorers == 0:
            synergy_statement +="\n - The team is lacking an elite scorer"

        if elite_playmakers == 0:
            synergy_statement +="\n - The team is lacking an elite playmaker"

        if elite_rebounders == 0:
            synergy_statement +="\n - The team is lacking an elite rebounder"

        if elite_defenders == 0:
            synergy_statement +="\n - The team is lacking an elite defender"

        
        # Predict a record out of 82 games
        wins = self.predict_record(team_fingerprints)
        losses = 82 - wins
        synergy_statement += "\nNow, here is a record prediction for this team: "
        synergy_statement += f"\n - Wins: {wins}, Losses: {losses}, {wins} - {losses}"

        return synergy_statement
    
    def normalize(self, value, min_val, max_val):
        return max(0, min(1, (value - min_val) / (max_val - min_val)))


    def fingerprint(self, player_stats):

        player_fingerprint = {}

        # Generate scoring ability score
        points_score = self.normalize(player_stats['points'] / player_stats['games'], 0, 38)
        fgPercent_score = self.normalize(player_stats['fg%'], 0.2, 0.8)
        threePercent_score = self.normalize(player_stats['3%'], 0.2, 0.5)
        threeAttempts_score = self.normalize(player_stats['3attempts'] / player_stats['games'], 0, 12)
        twoAttempts_score = self.normalize(player_stats['2attempts'] / player_stats['games'], 0, 11)
        overall_scoring_ability = (
            (points_score * 0.55) +
            (fgPercent_score * 0.20) +
            (threePercent_score * 0.10) +
            (threeAttempts_score * 0.05) +
            (twoAttempts_score * 0.10)
        )
        player_fingerprint['scoring_ability'] = overall_scoring_ability

        # Generate playmaking score
        assists_score = self.normalize(player_stats['assists'] / player_stats['games'], 0, 12)
        turnover_score = self.normalize(player_stats['turnovers'] / player_stats['games'], 0, 5)
        overall_playmaking_ability = ( (assists_score * 0.5) + (turnover_score * 0.5) )
        player_fingerprint['playmaking'] = overall_playmaking_ability

        # Generate rebounding ability
        rebounding_score = self.normalize(player_stats['rebounds'] / player_stats['games'], 0, 15)
        overall_rebounding_ability = ( (rebounding_score * 1) )
        player_fingerprint['rebounding'] = overall_rebounding_ability

        # Generate defenive ability
        steals_score = self.normalize(player_stats['steals'] / player_stats['games'], 0, 3)
        blocks_score = self.normalize(player_stats['blocks'] / player_stats['games'], 0, 4)
        overall_defensive_ability = ((steals_score * 0.5) + (blocks_score * 0.5))
        player_fingerprint['defense'] = overall_defensive_ability

        return player_fingerprint

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

        potential_player_stats = {}

        for playerId in potential_player_ids:

            params = {
                "page": 1,
                "pageSize": 1000,
                "season": season,
                "playerId": playerId,
            }
            
            response = requests.get(BASE_URL, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                players_list = data.get("data", [])
                for player in players_list:
                    potential_player_stats[player['playerName']] = player
            else:
                print(f'No player matches the playerId of: {playerId}')

        # If there are no matches
        if not potential_player_stats:
            return {}
        
        # If there is exactly one match (the correct player)
        if len(potential_player_stats) == 1:
            playerStats = list(potential_player_stats.values())[0]
        
        # If there is more than one match, find the correct player by name
        else:
            playerStats = None
            for pname, player in potential_player_stats.items():
                if pname.lower() == player_name.lower():
                    playerStats = player
                    break
            if not playerStats:
                print('issue finding player based on the id')
                return {}

        relevant_stats = {
                    "position": playerStats['position'],
                    "minutespg": playerStats['minutesPg'],
                    "fg%": playerStats['fieldPercent'],
                    "3%": playerStats['threePercent'],
                    "ft%": playerStats['ftPercent'],
                    "efg%": playerStats['effectFgPercent'],
                    "2attempts": playerStats['twoAttempts'],
                    "3attempts": playerStats['threeAttempts'],
                    "points": playerStats['points'],
                    "rebounds": playerStats['totalRb'],
                    "assists": playerStats['assists'],
                    "steals": playerStats['steals'],
                    "blocks": playerStats['blocks'],
                    "turnovers": playerStats['turnovers'],
                    "games": playerStats['games'],
        }
        
        return relevant_stats


    def get_team_stats(self, players, season=2025):

        if len(players) != 5:
            return "Enter 5 players"

        params = {
            "page": 1,
            "pageSize": 1000,
            "season": season
        }

        headers = {"accept": "application/json"}

        teamStats = {}

        for player in players:
            player_stats = self.get_player_stats(player)
            if player_stats:
                teamStats[player] = player_stats
            else:
                return "Problem with one of the players stats"

        return teamStats
            

    def evaluate_team(self, players):

        teamStats = self.get_team_stats(players)

        if not isinstance(teamStats, dict) or not teamStats:
            return "Error: could not get full team stats."

        team_fingerprint = {}

        for player_name, stats in teamStats.items():
            player_fingerprint = self.fingerprint(stats)
            team_fingerprint[player_name] = player_fingerprint

        synergy = self.check_synergy(team_fingerprint)

        return synergy

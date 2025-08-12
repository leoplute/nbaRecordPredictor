import requests
import json
import math
import itertools

BASE_URL = "https://api.server.nbaapi.com/api/playertotals"
ADVANCED_URL = "https://api.server.nbaapi.com/api/playeradvancedstats"

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
    
    def calculate_scoring_ability(self, player_stats):
        ts_score = self.normalize(player_stats['ts%'], 0.45, 0.70)
        usage_score = self.normalize(player_stats['usage%'], 0.12, 0.38)
        ppg = player_stats['points'] / player_stats['games']
        points_score = self.normalize(ppg, 5, 35)
        efg_score = self.normalize(player_stats['efg%'], 0.42, 0.68)
        fta_per_fga = player_stats['ftAttempts'] / max(player_stats['2attempts'] + player_stats['3attempts'], 1)
        ft_rate_score = self.normalize(fta_per_fga, 0.1, 0.6)

        overall_scoring_ability = (
            (ts_score * 0.35) +  # True shooting most important
            (usage_score * 0.25) +  # Context for volume
            (points_score * 0.20) +  # Raw production still matters
            (efg_score * 0.12) +  # Alternative efficiency measure
            (ft_rate_score * 0.08) # Getting to the line is valuable
        )
        return overall_scoring_ability
    
    def calculate_playmaking(self, player_stats):
        apg = player_stats['assists'] / player_stats['games']
        assists_score = self.normalize(apg, 1, 11)
        ast_to_ratio = player_stats['assists'] / max(player_stats['turnovers'], 1)
        ratio_score = self.normalize(ast_to_ratio, 0.8, 4.5)
        turnover_score = self.normalize(1 - player_stats['turnover%'], 1 - 0.20, 1 - 0.08)
        usage_score = self.normalize(abs(0.22 - player_stats['usage%']), 0, 0.15)

        overall_playmaking = (
            (assists_score * 0.35) +  # Raw assist production
            (ratio_score * 0.4) +  # Efficiency is important
            (turnover_score * 0.15) +  # Ball security
            (usage_score * 0.10)   # Context adjustment
        )

        return overall_playmaking
    
    def get_reduced_position_rebounding_factor(self, position):
        """Much smaller position adjustments that preserve volume distinctions"""
        position_factors = {
            "C": 1.0,     # Centers: baseline expectation
            "PF": 1.05,   # Power forwards: slight bonus for rebounding
            "SF": 1.15,   # Small forwards: moderate bonus
            "SG": 1.25,   # Shooting guards: good bonus but not extreme
            "PG": 1.35,   # Point guards: highest bonus but still reasonable
        }
        return position_factors.get(position, 1.15)  # Default for unknown positions
    

    def calculate_rebounding(self, player_stats):
        # Raw per-game rebounding - this captures volume dominance
        rpg = player_stats['rebounds'] / player_stats['games']
        raw_rebounding_score = self.normalize(rpg, 2, 16)  # Elite rebounders: 12+, role players: 4-8
        
        # Total rebound percentage - this captures efficiency and opportunity
        total_reb_score = self.normalize(player_stats['rebound%'], 0.04, 0.28)
        
        # Separate offensive and defensive components for nuanced analysis
        off_reb_score = self.normalize(player_stats['offensiveRbPercent'], 0.01, 0.15)
        def_reb_score = self.normalize(player_stats['defensiveRbPercent'], 0.06, 0.35)
        
        # Reduced position factor that acknowledges differences without overwhelming data
        position_factor = self.get_reduced_position_rebounding_factor(player_stats['position'])
        
        # Weight raw production heavily while incorporating efficiency measures
        base_rebounding_ability = (
            (raw_rebounding_score * 0.45) +    # Volume production is crucial
            (total_reb_score * 0.25) +         # Efficiency matters but less than volume
            (def_reb_score * 0.20) +           # Defensive rebounding fundamental to team defense
            (off_reb_score * 0.10)             # Offensive rebounding provides bonus value
        )
        
        # Apply modest position adjustment that preserves volume distinctions
        overall_rebounding_ability = base_rebounding_ability * position_factor
        
        return overall_rebounding_ability
    

    def get_position_defense_factor(self, position):
        position_weights = {
            'PG': [0.7, 0.3],  # Point guards: emphasize steals heavily
            'SG': [0.6, 0.4],  # Shooting guards: still favor steals but blocks matter
            'SF': [0.5, 0.5],  # Small forwards: balanced contribution expected
            'PF': [0.4, 0.6],  # Power forwards: blocks more important than steals
            'C': [0.3, 0.7],   # Centers: rim protection is primary defensive role
        }
        return position_weights.get(position, [0.5, 0.5])
    

    def calculate_defensive_ability(self, player_stats):
        steal_pct_score = self.normalize(player_stats['steal%'], 0.5, 4)
        block_pct_score = self.normalize(player_stats['block%'], 0.2, 8)
        def_bpm_score = self.normalize(player_stats['defensivePlusMinus'], -3, 5)
        def_reb_score = self.normalize(player_stats['defensiveRbPercent'], 0.05, 0.3)
        fouls_per_game = player_stats['fouls'] / player_stats['games']
        foul_score = self.normalize(6 - fouls_per_game, 0, 5)

        steal_weight, block_weight = self.get_position_defense_factor(player_stats['position'])
    
        # Calculate position-adjusted steal and block contributions
        position_adjusted_steal_block = (steal_pct_score * steal_weight) + (block_pct_score * block_weight)

        overall_defensive_ability = (
            (def_bpm_score * 0.35) +   # Overall impact most important
            (position_adjusted_steal_block * 0.35) +   # Position specific defense score
            (def_reb_score * 0.2) +   # Defensive rebounding score
            (foul_score * 0.1)     # Discipline factor
        )

        return overall_defensive_ability



    def fingerprint(self, player_stats):

        player_fingerprint = {}

        # Generate scoring ability score
        overall_scoring_ability = self.calculate_scoring_ability(player_stats)
        player_fingerprint['scoring_ability'] = overall_scoring_ability

        # Generate playmaking score
        overall_playmaking_ability = self.calculate_playmaking(player_stats)
        player_fingerprint['playmaking'] = overall_playmaking_ability

        # Generate rebounding ability
        overall_rebounding_ability = self.calculate_rebounding(player_stats)
        player_fingerprint['rebounding'] = overall_rebounding_ability

        # Generate defenive ability
        overall_defensive_ability = self.calculate_defensive_ability(player_stats)
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

        #return synergy
        return team_fingerprint

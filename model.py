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
    
    def percentile_normalize(self, value, percentiles):
        """
        Normalize based on percentile ranges rather than absolute min/max.
        This creates more realistic distributions.
        
        Args:
            value: The stat value to normalize
            percentiles: Dict with keys like 'p10', 'p50', 'p90' representing
                        the 10th, 50th, and 90th percentiles for this stat
        """
        if value <= percentiles['p10']:
            return 0.0
        elif value >= percentiles['p90']:
            return 1.0
        elif value <= percentiles['p50']:
            # Linear interpolation between 10th percentile (0.0) and 50th percentile (0.5)
            return 0.5 * (value - percentiles['p10']) / (percentiles['p50'] - percentiles['p10'])
        else:
            # Linear interpolation between 50th percentile (0.5) and 90th percentile (1.0)
            return 0.5 + 0.5 * (value - percentiles['p50']) / (percentiles['p90'] - percentiles['p50'])
    
    def calculate_scoring_ability(self, player_stats):
        # Points per game with realistic ranges
        ppg = player_stats['points'] / player_stats['games']
        ppg_percentiles = {
            'p10': 4.0,   # Bench players
            'p50': 11.5,  # Role players
            'p90': 25.0   # Elite scorers
        }
        
        # True shooting percentage ranges
        ts_percentiles = {
            'p10': 0.48,  # Poor efficiency
            'p50': 0.57,  # League average
            'p90': 0.67   # Elite efficiency
        }
        
        # Usage rate ranges
        usage_percentiles = {
            'p10': 0.12,  # Low usage
            'p50': 0.20,  # Average usage
            'p90': 0.32   # High usage stars
        }
        
        # Calculate component scores
        volume_score = self.percentile_normalize(ppg, ppg_percentiles)
        efficiency_score = self.percentile_normalize(player_stats['ts%'], ts_percentiles)
        usage_score = self.percentile_normalize(player_stats['usage%'], usage_percentiles)
        
        # Weight efficiency most heavily for scoring
        overall_scoring = (
            (efficiency_score * 0.45) +  # Efficiency is king
            (volume_score * 0.35) +      # Volume production matters
            (usage_score * 0.20)         # Context for role
        )
        
        return overall_scoring
    
    def calculate_playmaking(self, player_stats):
        # Assists per game
        apg = player_stats['assists'] / player_stats['games']
        apg_percentiles = {
            'p10': 1.2,   # Non-playmakers
            'p50': 3.1,   # Average
            'p90': 8.5    # Elite playmakers
        }
        
        # Assist-to-turnover ratio
        ast_to = player_stats['assists'] / max(player_stats['turnovers'], 1)
        ast_to_percentiles = {
            'p10': 0.9,   # Poor ball handlers
            'p50': 1.8,   # Average
            'p90': 3.5    # Excellent decision makers
        }
        
        # Turnover percentage (lower is better, so we invert it)
        to_pct_inverted = 1 - player_stats['turnover%']
        to_pct_percentiles = {
            'p10': 1 - 0.18,  # High turnover players
            'p50': 1 - 0.13,  # Average
            'p90': 1 - 0.08   # Great ball security
        }
        
        volume_score = self.percentile_normalize(apg, apg_percentiles)
        ratio_score = self.percentile_normalize(ast_to, ast_to_percentiles)
        security_score = self.percentile_normalize(to_pct_inverted, to_pct_percentiles)
        
        # Balance volume and efficiency
        overall_playmaking = (
            (volume_score * 0.4) +     # Raw assist production
            (ratio_score * 0.4) +      # Decision-making quality
            (security_score * 0.2)     # Ball security
        )
        
        return overall_playmaking
    

    def calculate_rebounding(self, player_stats):
        # Get raw rebounding rate
        rpg = player_stats['rebounds'] / player_stats['games']
        
        # Updated NBA percentiles - raised the elite threshold to better reflect actual distribution
        rpg_percentiles = {
            'p10': 2.2,   # Role players, guards - slightly lower to catch more low rebounders
            'p50': 4.8,   # Average NBA player - lowered to be more realistic
            'p90': 12.8   # Elite rebounders - raised significantly to properly capture Gobert/Sabonis tier
        }
        
        # Updated percentiles for total rebound percentage to better match reality
        trb_percentiles = {
            'p10': 0.05,  # Low-volume players
            'p50': 0.11,  # League average - slightly lower
            'p90': 0.28   # Elite rebounders - raised to capture truly elite rates
        }
        
        # Calculate base scores using percentile normalization
        volume_score = self.percentile_normalize(rpg, rpg_percentiles)
        efficiency_score = self.percentile_normalize(player_stats['rebound%'], trb_percentiles)
        
        # Much more conservative position adjustments to prevent inflation
        position_multipliers = {
            'C': 1.0,     # Centers - baseline expectation
            'PF': 1.01,   # Power forwards - minimal bonus
            'SF': 1.03,   # Small forwards - very small bonus  
            'SG': 1.06,   # Shooting guards - modest bonus
            'PG': 1.10,   # Point guards - reasonable but not excessive bonus
        }
        
        position_factor = position_multipliers.get(player_stats['position'], 1.02)
        
        # Increase volume weighting even more since raw rebounds matter most for team success
        base_score = (volume_score * 0.80) + (efficiency_score * 0.20)
        
        # Apply position adjustment more conservatively
        final_score = min(1.0, base_score * position_factor)
        
        return final_score
    

    def calculate_defensive_ability(self, player_stats):
        # Expanded defensive box plus-minus percentiles to capture elite defenders better
        dbpm_percentiles = {
            'p10': -3.0,  # Poor defenders - expanded range downward
            'p50': 0.0,   # Average - true neutral
            'p90': 4.0    # Elite defenders - expanded upward to capture Gobert-tier impact
        }
        
        # Steal percentage - slightly adjusted based on current league trends
        stl_pct_percentiles = {
            'p10': 0.5,   # Low steal rate
            'p50': 1.3,   # Average - slightly lower
            'p90': 3.0    # High steal rate - raised slightly
        }
        
        # Block percentage - significantly expanded to better capture rim protectors
        blk_pct_percentiles = {
            'p10': 0.3,   # Low block rate
            'p50': 1.0,   # Average - lowered  
            'p90': 6.5    # Elite rim protectors - raised to better capture Gobert's impact
        }
        
        # Position-specific weights for steals vs blocks
        position_weights = {
            'PG': {'steal': 0.8, 'block': 0.2},  # Guards rely heavily on steals
            'SG': {'steal': 0.75, 'block': 0.25}, 
            'SF': {'steal': 0.6, 'block': 0.4},   # Wings more balanced
            'PF': {'steal': 0.35, 'block': 0.65}, # Bigs favor blocks
            'C': {'steal': 0.25, 'block': 0.75}   # Centers heavily weighted toward rim protection
        }
        
        weights = position_weights.get(player_stats['position'], {'steal': 0.5, 'block': 0.5})
        
        # Calculate component scores
        dbpm_score = self.percentile_normalize(player_stats['defensivePlusMinus'], dbpm_percentiles)
        steal_score = self.percentile_normalize(player_stats['steal%'], stl_pct_percentiles)
        block_score = self.percentile_normalize(player_stats['block%'], blk_pct_percentiles)
        
        # Position-weighted steal/block contribution
        steal_block_score = (steal_score * weights['steal']) + (block_score * weights['block'])
        
        # Slightly increased weighting on defensive plus-minus since it's the best overall measure
        overall_defense = (
            (dbpm_score * 0.60) +        # Overall impact most important - increased weight
            (steal_block_score * 0.40)   # Position-specific contributions - decreased weight
        )
        
        return overall_defense



    def fingerprint(self, player_stats):
        fingerprint = {
            'scoring_ability': self.calculate_scoring_ability(player_stats),
            'playmaking': self.calculate_playmaking(player_stats),
            'rebounding': self.calculate_rebounding(player_stats),
            'defense': self.calculate_defensive_ability(player_stats)
        }
        return fingerprint

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
        return json.dumps(team_fingerprint, indent=4)

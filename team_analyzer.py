

class teamAnalyzer:
    '''
    def __init__(self):
        pass'''

    def categorize_players(self, team_fingerprints):

        team_totals = {
                'scoring_ability': 0,
                'playmaking': 0,
                'rebounding': 0,
                'defense': 0,
            }
        
        scoring = {
            'elite': [],
            'good': [],
            'average': [],
            'bad': []
        }
        playmaking = {
            'elite': [],
            'good': [],
            'average': [],
            'bad': []
        }
        rebounding = {
            'elite': [],
            'good': [],
            'average': [],
            'bad': []
        }
        defense = {
            'elite': [],
            'good': [],
            'average': [],
            'bad': []
        }

        # Add up everyones stats to get collective strengths + weaknesses, as well as get lists
        # of everyone who is elite, good, and bad at scoring, playmaking, rebounding, and defense.
        for player_name, fingerprint in team_fingerprints.items():
            for ability, score in fingerprint.items():

                if ability == "usage%":
                    continue

                team_totals[ability] += score

                if ability == 'scoring_ability':
                    if score >= 0.75:
                        scoring['elite'].append(player_name)
                    if score < 0.75 and score > 0.5:
                        scoring['good'].append(player_name)
                    if score <= 0.5 and score > 0.3:
                        scoring['average'].append(player_name)
                    if score <= 0.3:
                        scoring['bad'].append(player_name)

                if ability == 'playmaking':
                    if score >= 0.7:
                        playmaking['elite'].append(player_name)
                    if score < 0.7 and score > 0.45:
                        playmaking['good'].append(player_name)
                    if score <= 0.45 and score > 0.25:
                        playmaking['average'].append(player_name)
                    if score <= 0.25:
                        playmaking['bad'].append(player_name)

                if ability == 'rebounding':
                    if score >= 0.7:
                        rebounding['elite'].append(player_name)
                    if score < 0.7 and score > 0.45:
                        rebounding['good'].append(player_name)
                    if score <= 0.45 and score > 0.2:
                        rebounding['average'].append(player_name)
                    if score <= 0.2:
                        rebounding['bad'].append(player_name)

                if ability == 'defense':
                    if score >= 0.75:
                        defense['elite'].append(player_name)
                    if score < 0.75 and score > 0.5:
                        defense['good'].append(player_name)
                    if score <= 0.5 and score > 0.3:
                        defense['average'].append(player_name)
                    if score <= 0.3:
                        defense['bad'].append(player_name)

        return scoring, playmaking, rebounding, defense, team_totals
    

    def usage_analysis(self, team_fingerprints):
        high_usage_players = []
        average_usage_players = []
        low_usage_players = []

        for player_name, fingerprint in team_fingerprints.items():
            if fingerprint['usage%'] >= 25:
                high_usage_players.append(player_name)
            elif fingerprint['usage%'] <= 14:
                low_usage_players.append(player_name)
            else:
                average_usage_players.append(player_name)

        usage_analysis = {
            'high': high_usage_players,
            'average': average_usage_players,
            'low': low_usage_players
        }

        return usage_analysis


    def get_player_combos(self, player_categories):

        scoring = player_categories['scoring']
        playmaking = player_categories['playmaking']
        rebounding = player_categories['rebounding']
        defense = player_categories['defense']

        good_combos = []

        # Helper function to make sure two players on the 
        def not_same_player(list1, list2):
            return len(set(list1 + list2)) > max(len(list1), len(list2))
        
        # Rest of function is testing for a bunch of potential good combos on court and putting them
        # in a list to return
        
        # Elite scorer + elite playmaker
        if len(scoring['elite']) == 1 and len(playmaking['elite']) == 1:
            if not_same_player(scoring['elite'], playmaking['elite']):
                good_combos.append({
                    'type': 'elite_scorer_playmaker',
                    'scorer': scoring['elite'],
                    'playmaker': playmaking['elite']
                })

        # Elite scorer + good scorer
        if len(scoring['elite']) == 1 and len(scoring['good']) == 1:
            good_combos.append({
                'type': 'great_scoring',
                'eliteScorer': scoring['elite'],
                'goodScorer': scoring['good']
            }) 

        # Elite scorer + 2 good scorers
        if len(scoring['elite']) == 1 and len(scoring['good']) == 2:
            good_combos.append({
                'type': 'great_scoring_trio',
                'eliteScorer': scoring['elite'],
                'goodScorers': scoring['good']
            }) 

        # Elite scorer + elite playmaker + elite rebounder + elite defender
        if len(scoring['elite']) == 1 and len(playmaking['elite']) == 1 and not_same_player(scoring['elite'], playmaking['elite']):
            if len(rebounding['elite']) == 1 and len(defense['elite']) == 1 and not_same_player(rebounding['elite'], defense['elite']):
                if not_same_player(scoring['elite'], rebounding['elite']) and not_same_player(playmaking['elite'], defense['elite']):
                    if not_same_player(scoring['elite'], defense['elite']) and not_same_player(playmaking['elite'], rebounding['elite']):
                        good_combos.append({
                            'type': 'four_headed_monster',
                            'scorer': scoring['elite'],
                            'playmaker': playmaking['elite'],
                            'rebounder': rebounding['elite'],
                            'defender': defense['elite']
                        }) 

        # Elite rebounder + elite defender
        if len(rebounding['elite']) == 1 and len(defense['elite']) == 1:
            if not_same_player(rebounding['elite'], defense['elite']):
                good_combos.append({
                    'type': 'defender_rebounder',
                    'defender': defense['elite'],
                    'rebounder': rebounding['elite']
                })

        # 2 elite playmakers
        if len(playmaking['elite']) == 2:
            good_combos.append({
                'type': 'dual_playmakers',
                'playmakers': playmaking['elite']
            })

        # Elite scorer, elite playmaker, + elite rebounder
        if len(playmaking['elite']) == 1 and len(scoring['elite']) == 1 and len(rebounding['elite']) == 1:
            if not_same_player(playmaking['elite'], rebounding['elite']) and not_same_player(playmaking['elite'], scoring['elite']):
                if not_same_player(rebounding['elite'], scoring['elite']):
                    good_combos.append({
                        'type': 'fundamental_trio',
                        'scorer': scoring['elite'],
                        'playmaker': playmaking['elite'],
                        'rebounder': rebounding['elite']
                    })

        # 2 good scorers + good playmaker
        if len(playmaking['good']) == 1 and len(scoring['good']) == 2:
            if not_same_player(scoring['good'], playmaking['good']):
                good_combos.append({
                    'type': 'upcoming_trio',
                    'playmaker': playmaking['good'],
                    'scorers': scoring['good']
                })

        return good_combos
    

    def check_redundancy(self, team_fingerprints):
        # Classify players into roles first
        player_roles = {}
        redundant_pairs = []
        
        for player_name, fp in team_fingerprints.items():
            # Determine primary role based on basketball archetypes
            if fp['scoring_ability'] >= 0.75 and fp['usage%'] >= 0.28:
                role = "superstar"
            elif fp['scoring_ability'] >= 0.7 and fp['usage%'] >= 0.22:
                role = "primary_scorer"
            elif fp['scoring_ability'] >= 0.6 and fp['usage%'] <= 0.18:
                role = "efficient_scorer"  # High efficiency, lower usage
            elif fp['playmaking'] >= 0.65 and fp['usage%'] >= 0.20:
                role = "floor_general"
            elif fp['playmaking'] >= 0.5 and fp['scoring_ability'] >= 0.6:
                role = "combo_guard"  # Can score and create
            elif fp['defense'] >= 0.75 and fp['rebounding'] >= 0.65:
                role = "rim_protector"
            elif fp['defense'] >= 0.7 and fp['rebounding'] <= 0.4:
                role = "perimeter_defender"  # Good defense but not a rebounder
            elif fp['rebounding'] >= 0.7 and fp['defense'] >= 0.5:
                role = "glass_cleaner"  # Rebounding specialist
            elif fp['scoring_ability'] >= 0.5 and fp['rebounding'] >= 0.6 and fp['defense'] >= 0.5:
                role = "stretch_big"  # Versatile big man
            elif fp['scoring_ability'] <= 0.4 and fp['defense'] >= 0.6:
                role = "defensive_specialist"
            elif fp['scoring_ability'] <= 0.4 and fp['playmaking'] <= 0.4 and fp['usage%'] <= 0.15:
                role = "energy_player"  # Hustle guy, limited offensive role
            elif fp['scoring_ability'] >= 0.45 and max(fp['playmaking'], fp['rebounding'], fp['defense']) <= 0.5:
                role = "microwave_scorer"  # Can get hot but limited elsewhere
            elif fp['usage%'] >= 0.25 and fp['scoring_ability'] <= 0.6:
                role = "high_volume_inefficient"  # Takes lots of shots, not great at it
            elif all(0.4 <= fp[skill] <= 0.65 for skill in ['scoring_ability', 'playmaking', 'rebounding', 'defense']):
                role = "well_rounded_role_player"
            elif max(fp['scoring_ability'], fp['playmaking'], fp['rebounding'], fp['defense']) < 0.45:
                role = "bench_warmer"
            else:
                role = "versatile"  # Doesn't fit clear archetype
                
            player_roles[player_name] = role
        
        # Check for too many players in same role
        role_counts = {}
        for player, role in player_roles.items():
            if role not in role_counts:
                role_counts[role] = []
            role_counts[role].append(player)
        
        # Flag redundancies - certain roles shouldn't be duplicated
        problematic_duplicates = [
            "superstar", "floor_general", "rim_protector", 
            "high_volume_inefficient", "bench_warmer"
        ]
        
        concerning_duplicates = [
            "primary_scorer", "perimeter_defender", "glass_cleaner"
        ]
        
        for role, players in role_counts.items():
            if len(players) > 1:
                if role in problematic_duplicates:
                    redundant_pairs.append((players, role, "major redundancy - only need one"))
                elif role in concerning_duplicates and len(players) > 2:
                    redundant_pairs.append((players, role, "too many in same role"))
                elif len(players) >= 3:  # Any role with 3+ players is probably redundant
                    redundant_pairs.append((players, role, "oversaturation"))
        
        return redundant_pairs, player_roles
    
    def check_critical_gaps(self, elite_scorers, good_scorers, elite_playmakers, good_playmakers, elite_rebounders, 
                good_rebounders, elite_defenders, good_defenders):
        
        gaps_statement = "\n\nLets check if the team has any major gaps: "

        found_gap = False

        if not elite_scorers and not good_scorers:
            gaps_statement += f"\n - The team is severely lacking a competent scoring option, possibly even a couple."
            found_gap = True

        if not elite_scorers and good_scorers and len(good_scorers) < 3:
            gaps_statement += f"\n - The team is lacking enough scoring production to compete in todays NBA."
            found_gap = True

        if not elite_playmakers and good_playmakers and len(good_playmakers) < 2:
            gaps_statement += f"\n - The team is lacking playmaking. Ball movement is likely to be stagnant with little shot creation for others."
            found_gap = True

        if not elite_rebounders and good_rebounders and len(good_rebounders) < 2:
            gaps_statement += f"\n - The team needs more of a presence on the boards."
            found_gap = True

        if not elite_rebounders and not good_rebounders:
            gaps_statement += f"\n - The team is in need of a solid rebounder or two. This team will get killed on the boards"
            found_gap = True

        if not elite_defenders and not good_defenders:
            gaps_statement += f'\n - This team is in desperate need of a lockdown defender. There is no one to slow down opposing stars from putting up career nights against this lineup.'
            found_gap = True

        if not elite_defenders and not elite_rebounders:
            gaps_statement += f'\n - This team will struggle to slow down high octane offenses, with the absense of an elite rebounder and defender, this team will need to score 150 a night to compete.'
            found_gap = True

        if found_gap == False:
            gaps_statement += f'\n - No major gaps found.'
        else:
            gaps_statement += f'\n\nWhat area could the team sacrifice to fill some of those gaps?: '
            sacrifice_found = False

            if len(elite_playmakers) >= 2 and good_playmakers:
                gaps_statement += f'\n - The team has plenty of playmaking on the roster, maybe get rid of some playmakers.'
                sacrifice_found = True

            if len(good_playmakers) >= 3:
                gaps_statement += f'\n - The team has some pretty good playmakers, sacrificing playmaking for other abilities of need would be a good option here.'
                sacrifice_found = True

            if len(elite_scorers) >= 2 and len(good_scorers) >= 2:
                gaps_statement += f'\n - This team has enough high octane scorers, sacrifice some scoring for a more well rounded roster.'
                sacrifice_found = True
        
            if len(good_scorers) >= 4:
                gaps_statement += f'\n - This team has lots of goods scorers, one will likely step up to elite, meaning lessening some scoring for stats elsewhere will benefit the whole team.'
                sacrifice_found = True

            if len(elite_rebounders) >= 2 and len(good_rebounders) >= 2:
                gaps_statement += f'\n - The tea has lots of players that are active on the boards, maybe let go of some rebounding to help out the rest of the roster.'
                sacrifice_found = True

            if sacrifice_found == False:
                gaps_statement += f"\n - Team isn't competent enough in any area to sacrifice one for another" 

        return gaps_statement
    

    def check_aggregate_gaps(self, team_fingerprints):
        gaps_statement = "\n\nAggregate Team Gap Analysis:"
        found_gap = False

        # Calculate team totals
        totals = {
            'scoring': sum(fp['scoring_ability'] for fp in team_fingerprints.values()),
            'playmaking': sum(fp['playmaking'] for fp in team_fingerprints.values()),
            'defense': sum(fp['defense'] for fp in team_fingerprints.values()),
            'rebounding': sum(fp['rebounding'] for fp in team_fingerprints.values())
        }

        # Set thresholds (out of 5.0 total possible)
        thresholds = {
            'scoring': 2.8,     # Need decent offensive firepower
            'playmaking': 2.0,  # Need some ball movement
            'defense': 2.5,     # Defense wins championships
            'rebounding': 2.2   # Control the boards
        }

        for skill, total in totals.items():
            if total < thresholds[skill]:
                found_gap = True
                severity = "CRITICAL" if total < thresholds[skill] * 0.8 else "WARNING"
                gaps_statement += (
                    f"\n - {severity}: Team {skill} total ({total:.1f}) "
                    f"below competitive threshold ({thresholds[skill]:.1f})"
                )

        if not found_gap:
            gaps_statement += "\n - No major gaps found."

        return gaps_statement
    

    def predict_record(self, elite_scorers, good_scorers, bad_scorers, 
                        elite_defenders, good_defenders, bad_defenders,
                        elite_playmakers, elite_rebounders, team_fingerprints, redundancies):
    
        # Feature engineering
        features = {}
        
        # Star power features
        features['elite_count'] = len(set(elite_scorers + elite_playmakers + elite_defenders + elite_rebounders))
        features['scoring_depth'] = len(elite_scorers) + len(good_scorers) * 0.6
        features['defensive_strength'] = len(elite_defenders) + len(good_defenders) * 0.5
        
        # Balance features  
        features['major_weaknesses'] = len(bad_scorers) + len(bad_defenders)
        features['redundancy_penalty'] = len(redundancies) * 2
        
        # Chemistry features
        high_usage_count = sum(1 for fp in team_fingerprints.values() if fp['usage%'] > 0.25)
        features['usage_balance'] = abs(high_usage_count - 2)  # Optimal is 2 stars
        
        # Weights learned from historical data (you'd tune these)
        weights = {
            'elite_count': 8.0,
            'scoring_depth': 4.0, 
            'defensive_strength': 5.0,
            'major_weaknesses': -6.0,
            'redundancy_penalty': -2.0,
            'usage_balance': -3.0
        }
        
        # Calculate predicted wins
        predicted_wins = 35  # Base level
        for feature, value in features.items():
            predicted_wins += value * weights[feature]
        
        wins = max(15, min(67, round(predicted_wins)))
        return wins, 82 - wins

            
    def get_players_string(self, players):
        if len(players) > 1:
            result = ", ".join(players[:-1]) + ", and " + players[-1]
        else:
            result = players[0] if players else ""
        return result

    def analyze_team(self, team_fingerprints):

        scoring, playmaking, rebounding, defense, team_totals = self.categorize_players(team_fingerprints)

        player_categories = {
            'scoring': scoring,
            'playmaking': playmaking,
            'rebounding': rebounding,
            'defense': defense
        }

        usage_analysis = self.usage_analysis(team_fingerprints)

        good_combos = self.get_player_combos(player_categories)

        return {
            'player_categories': player_categories,
            'usage_analysis': usage_analysis,
            'good_combos': good_combos,
            '''
            'redundancies': redundancies,
            'player_roles': player_roles,
            'gaps': gaps,
            'aggregate_gaps': aggregate_gaps,
            'predicted_record': {'wins': wins, 'losses': losses},'''
            'team_fingerprints': team_fingerprints
        }
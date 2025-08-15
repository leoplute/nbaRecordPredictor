import requests
import json
import math
import itertools

BASE_URL = "https://api.server.nbaapi.com/api/playertotals"
ADVANCED_URL = "https://api.server.nbaapi.com/api/playeradvancedstats"

class FantasyModel:

    def get_elite_good_average_bad_statement(self, elite_scorers, good_scorers, average_scorers, bad_scorers, 
    elite_playmakers, good_playmakers, average_playmakers, bad_playmakers, elite_rebounders, good_rebounders, 
    average_rebounders, bad_rebounders, elite_defenders, good_defenders, average_defenders, bad_defenders):
                
        # Critical role analysis (these are must-haves)
        # Is there an elite, good, or bad scorer? if so, how many and 
        
        synergy_statement = "\n - "
        if elite_scorers:
            synergy_statement += f"{len(elite_scorers)} elite scorer(s) ({self.get_players_string(elite_scorers)}), "
        if good_scorers:
            synergy_statement += f"{len(good_scorers)} good scorer(s) ({self.get_players_string(good_scorers)}), "
        if average_scorers:
            synergy_statement += f"{len(average_scorers)} average scorer(s) ({self.get_players_string(average_scorers)}), "
        if bad_scorers:
            synergy_statement += f"{len(bad_scorers)} bad scorer(s) ({self.get_players_string(bad_scorers)})."

        synergy_statement += "\n - "
        if elite_playmakers:
            synergy_statement += f"{len(elite_playmakers)} elite playmaker(s) ({self.get_players_string(elite_playmakers)}), "
        if good_playmakers:
            synergy_statement += f"{len(good_playmakers)} good playmaker(s) ({self.get_players_string(good_playmakers)}), "
        if average_playmakers:
            synergy_statement += f"{len(average_playmakers)} average playmaker(s) ({self.get_players_string(average_playmakers)}), "
        if bad_playmakers:
            synergy_statement += f"{len(bad_playmakers)} bad playmaker(s) ({self.get_players_string(bad_playmakers)})."

        synergy_statement += "\n - "
        if elite_rebounders:
            synergy_statement += f"{len(elite_rebounders)} elite rebounder(s) ({self.get_players_string(elite_rebounders)}), "
        if good_rebounders:
            synergy_statement += f"{len(good_rebounders)} good rebounder(s) ({self.get_players_string(good_rebounders)}), "
        if average_rebounders:
            synergy_statement += f"{len(average_rebounders)} average rebounder(s) ({self.get_players_string(average_rebounders)}), "
        if bad_rebounders:
            synergy_statement += f"{len(bad_rebounders)} bad rebounder(s) ({self.get_players_string(bad_rebounders)})."

        synergy_statement += "\n - "
        if elite_defenders:
            synergy_statement += f"{len(elite_defenders)} elite defender(s) ({self.get_players_string(elite_defenders)}), "
        if good_defenders:
            synergy_statement += f"{len(good_defenders)} good defender(s) ({self.get_players_string(good_defenders)}), "
        if average_defenders:
            synergy_statement += f"{len(average_defenders)} average defender(s) ({self.get_players_string(average_defenders)}), "
        if bad_defenders:
            synergy_statement += f"{len(bad_defenders)} bad defender(s) ({self.get_players_string(bad_defenders)})."

        return synergy_statement

    def get_usage_statement(self, team_fingerprints):
        synergy_statement = "\n\nNow lets go over the usage rates of the players on the team:"
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

        # If there is no high usage players:
        if len(high_usage_players) == 0:
            synergy_statement += "\n - This squad has no proven stars who can take on a significant role"
            if len(low_usage_players) == 5:
                synergy_statement += f"\n - No player on this squad had a significant role for a team last year ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 1 and len(low_usage_players) == 4:
                synergy_statement += f"\n - You have 1 player who has proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), but 4 who did not ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 2  and len(low_usage_players) == 3:
                synergy_statement += f"\n - You have 2 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), but 3 who did not ({self.get_players_string(low_usage_players)})"
            if len(average_usage_players) == 3 and len(low_usage_players) == 2:
                synergy_statement += f"\n - You have 3 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), maybe one could breakout as a start with the opportunity, outside of them, 2 players with little usage ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 4  and len(low_usage_players) == 1:
                synergy_statement += f"\n - You have 4 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), this is a great chance for one or two to breakout and become a high usage star this year. You have one player with little usage ({self.get_players_string(low_usage_players)})"
            if len(average_usage_players) == 5:
                synergy_statement += f"\n - You have 5 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}). This is likely too much usage for one lineup, especially if one were to become a higher usage player."

        # 1 high usage players
        if len(high_usage_players) == 1:
            synergy_statement += f"\n - This lineup has one true star who was taking on a big offensive load last year, and that is {high_usage_players[0]}."
            if len(low_usage_players) == 4:
                synergy_statement += f"\n - Outside of the star, you have 4 players who didnt have much of a role last year ({self.get_players_string(low_usage_players)})."
                synergy_statement += "\n - If the low usage players could all make a big jump collectively this year, the team could compete, but until then its likely losses ahead."
            if len(low_usage_players) == 3:
                synergy_statement += f"\n - Outside of the star, the team has 3 low usage players ({self.get_players_string(low_usage_players)}) and 1 player who had average role last year ({self.get_players_string(average_usage_players)})."
                synergy_statement += f"\n - If the {average_usage_players[0]} continued to improve, and another low usage player jumped as well, this could be a solid team."
            if len(low_usage_players) == 2:
                synergy_statement += f"\n - Outside of the star, the team has 2 players with average roles last year ({self.get_players_string(average_usage_players)}), and 2 players with low usage last year ({self.get_players_string(low_usage_players)})."
                synergy_statement += "\n - Assuming they all develop and get better in their roles, this team can expect to compete in the coming years."
            if len(low_usage_players) == 1:    
                synergy_statement += f"\n - Outside of the star, the team has 3 players with average roles ({self.get_players_string(average_usage_players)}) and 1 low usage player ({self.get_players_string(low_usage_players)})."
                synergy_statement += "\n - Assuming they grow together as a team one of the average players jumps into star status, this team is on track to be a contender."

        # 2 high usage players
        if len(high_usage_players) == 2:
            synergy_statement += f"\n - This is a star driven lineup, 2 high usage players, {high_usage_players[0]} and {high_usage_players[1]}."
            if len(low_usage_players) == 3:
                synergy_statement += f"\n - After the 2 stars, you do not have another player proven to be able to step into a third star role. ({self.get_players_string(low_usage_players)})"
            if len(average_usage_players) == 2 and len(low_usage_players) == 1:
                synergy_statement += f"\n - After the 2 stars, you have 2 others players who have proven to be able to have roles on their team ({self.get_players_string(average_usage_players)}), and 1 player with low usage, maybe specialists ({self.get_players_string(low_usage_players)})."
            if len(low_usage_players) == 2 and len(average_usage_players) == 1:
                synergy_statement += f"\n - After the 2 stars, you have 1 other player who has proven to be able to have a role on his team ({self.get_players_string(average_usage_players)}), and 2 players with low usage, maybe specialistst ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 3:
                synergy_statement += f"\n - After the 2 stars, you have 3 other players who have proven to have roles on their teams ({self.get_players_string(average_usage_players)}), but this may cause for too many people wanting the ball."

        # 3 high usage player
        if len(high_usage_players) == 3:
            synergy_statement += f"\n - This team is led by a trio of stars, all used to having the ball in their hand ({self.get_players_string(high_usage_players)})."
            synergy_statement += "\n - With the right coaching and supporting cast, this squad could do some damage, but they all need to have the championship as goal number 1."
            if len(average_usage_players) == 2:
                synergy_statement += f"\n - Outside of the 3 stars, you have 2 other players who had an average role last year ({self.get_players_string(average_usage_players)})."
                synergy_statement += "\n - If one or two of them could take on a smaller role and accept less shots, this team could be good."
            if len(average_usage_players) == 1:
                synergy_statement += f"\n - Outside of the 3 stars, you have 1 role player ({self.get_players_string(average_usage_players)}) and 1 player who didn't have much of a role last year ({self.get_players_string(low_usage_players)}). If everyone can keep their roles, this team should be primed to make a run."
            if len(low_usage_players) == 2:
                synergy_statement += f"\n - Outside of the 3 stars, you have 2 players who did not have a big role last year ({self.get_players_string(low_usage_players)})."
                synergy_statement += "\n - If they can continue to play their role around the 3 stars, this lineup could win a lot of games"

        # 4 high usage players
        if len(high_usage_players) == 4:
            synergy_statement += f"\n - You have 4 high usage players, all on the same team ({self.get_players_string(high_usage_players)}). This is likely too much unless 2 of them are able and willing to take on a smaller role." 
            if len(average_usage_players) == 1:
                synergy_statement += f"\n - Besides the 4 stars, you have 1 role player ({self.get_players_string(average_usage_players)}), another player used to getting some shots"
                synergy_statement += "\n - With this many people wanting the ball, this is likely to not workout."
            if len(low_usage_players) == 1:
                synergy_statement += f"\n - Besides the 4 stars, you have 1 player who did not have a significant role last year ({self.get_players_string(low_usage_players)})."
                synergy_statement += "\n - This means that if 2 guys can take on a smaller role, this lineup has a great opportunity to compete"

        # 5 high usage players
        if len(high_usage_players) == 5:
            synergy_statement += f"\n - You have 5 high usage players, all on the same team ({self.get_players_string(high_usage_players)}). This is more likely an All-Star lineup rather than one that could truly compete for a championship"
            synergy_statement += "\n - Between egos and salaries, this team is not likely to stay together long enough to build the chemistry to win at the highest level."

        return synergy_statement

    def get_player_combos(self, elite_scorers, elite_playmakers, elite_rebounders, elite_defenders):
        synergy_statement = "\n\nHere is a breakdown of potentially strong player combinations: "
        if len(elite_scorers) == 1 and len(elite_playmakers) == 1:
            synergy_statement += f'\n - Elite scorer ({elite_scorers[0]}) + playmaker ({elite_playmakers[0]}) combo should create excellent offensive flow'

        if len(elite_scorers) == 2 and len(elite_playmakers) == 1:
            synergy_statement += f'\n - Elite scorer duo ({self.get_players_string(elite_scorers)}) + playmaker ({elite_playmakers[0]}) means an offense that can score from any spot on the court'

        if len(elite_scorers) == 1 and len(elite_playmakers) == 2:
            synergy_statement += f'\n - Elite scorer ({elite_scorers[0]}) + playmakers ({self.get_players_string(elite_playmakers)}) means a star that will be getting set up from lots of players on the court'

        if len(elite_defenders) == 2:
            synergy_statement += f'\n - 2 Elite defenders ({self.get_players_string(elite_defenders)}) will cause for matchup nightmares'

        if len(elite_defenders) == 3:
            synergy_statement += f'\n - 3 Elite defenders ({self.get_players_string(elite_defenders)}) will mean every star in the league will have a bad matchup somewhere on the team'

        if len(elite_rebounders) == 1 and len(elite_defenders) == 1:
            synergy_statement += f'\n - Elite rebounder ({elite_rebounders[0]}) and defender ({elite_defenders[0]}) means the chance of second chance points for the other team goes down'

        if len(elite_defenders) == 2 and len(elite_rebounders) == 1:
            synergy_statement += f'\n - Elite defender duo ({self.get_players_string(elite_defenders)}) + elite rebounder ({elite_rebounders[0]}) means lockdown defense with a strong rebounder to stop second chance points'

        if len(elite_rebounders) == 2:
            synergy_statement += f'\n - 2 Elite rebounders ({self.get_players_string(elite_rebounders)}) will dominate the boards'
        
        if len(elite_scorers) == 3:
            synergy_statement += f'\n - 3 Elite scorers ({self.get_players_string(elite_scorers)}) will give the team a scoring option at all times.'

        if len(elite_playmakers) == 2:
            synergy_statement += f"\n - 2 Elite playmakers ({self.get_players_string(elite_playmakers)}) will be able to set up any teammate"
        
        return synergy_statement

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

    def check_synergy(self, team_fingerprints):
        # Take in 5 'fingerprints'

        synergy_statement = "Thank you for inputting you team."

        team_abilities_totals = {
            'scoring_ability': 0,
            'playmaking': 0,
            'rebounding': 0,
            'defense': 0,
        }

        # Based on the players fingerprints, put them in these lists if they meet the thresholds
        # to use when evaluating where team is lacking + needing
        elite_scorers = []
        elite_playmakers = []
        elite_rebounders = []
        elite_defenders =[]
        good_scorers = []
        good_playmakers =[]
        good_rebounders = []
        good_defenders = []
        average_scorers = []
        average_playmakers =[]
        average_rebounders = []
        average_defenders = []
        bad_scorers = []
        bad_playmakers =[]
        bad_rebounders =[]
        bad_defenders = []

        # Add up everyones stats to get collective strengths + weaknesses, as well as get lists
        # of everyone who is elite, good, and bad at scoring, playmaking, rebounding, and defense.
        for player_name, fingerprint in team_fingerprints.items():
            for ability, score in fingerprint.items():

                if ability == "usage%":
                    break

                team_abilities_totals[ability] += score

                if ability == 'scoring_ability':
                    if score >= 0.75:
                        elite_scorers.append(player_name)
                    if score < 0.75 and score > 0.5:
                        good_scorers.append(player_name)
                    if score <= 0.5 and score > 0.3:
                        average_scorers.append(player_name)
                    if score <= 0.3:
                        bad_scorers.append(player_name)

                if ability == 'playmaking':
                    if score >= 0.7:
                        elite_playmakers.append(player_name)
                    if score < 0.7 and score > 0.45:
                        good_playmakers.append(player_name)
                    if score <= 0.45 and score > 0.25:
                        average_playmakers.append(player_name)
                    if score <= 0.25:
                        bad_playmakers.append(player_name)

                if ability == 'rebounding':
                    if score >= 0.7:
                        elite_rebounders.append(player_name)
                    if score < 0.7 and score > 0.45:
                        good_rebounders.append(player_name)
                    if score <= 0.45 and score > 0.2:
                        average_rebounders.append(player_name)
                    if score <= 0.2:
                        bad_rebounders.append(player_name)

                if ability == 'defense':
                    if score >= 0.75:
                        elite_defenders.append(player_name)
                    if score < 0.75 and score > 0.5:
                        good_defenders.append(player_name)
                    if score <= 0.5 and score > 0.3:
                        average_defenders.append(player_name)
                    if score <= 0.3:
                        bad_defenders.append(player_name)

        synergy_statement += '\nHere is a breakdown of your team: '
        
        # Critical role analysis (these are must-haves)
        # Is there an elite, good, or bad scorer? if so, how many and who
        elite_good_bad_statement = self.get_elite_good_average_bad_statement(elite_scorers=elite_scorers, good_scorers=good_scorers, 
                                    bad_scorers=bad_scorers, elite_playmakers=elite_playmakers, good_playmakers=good_playmakers,
                                    bad_playmakers=bad_playmakers, elite_rebounders=elite_rebounders, good_rebounders=good_rebounders,
                                    bad_rebounders=bad_rebounders, elite_defenders=elite_defenders, good_defenders=good_defenders, bad_defenders=bad_defenders,
                                    average_scorers=average_scorers, average_playmakers=average_playmakers, average_rebounders=average_rebounders, average_defenders=average_defenders)
        synergy_statement += str(elite_good_bad_statement)


        # Evaluate the team usage breakdown.
        # - Too many people wanting the ball? too little?, etc...
        usage_string = self.get_usage_statement(team_fingerprints=team_fingerprints)
        synergy_statement += str(usage_string)


        # Check for complementary pairings
        # MAKE SURE IT IS NOT THE SAME PLAYER
        player_combos_string = self.get_player_combos(elite_scorers=elite_scorers, elite_defenders=elite_defenders, elite_rebounders=elite_rebounders, elite_playmakers=elite_playmakers)
        synergy_statement += str(player_combos_string)


        # Check for redundant players that'll play the same role on the court
        redundancies, player_roles = self.check_redundancy(team_fingerprints)
    
        if redundancies:
            synergy_statement += "\n\nTeam Role Analysis:"
            
            # First, show what roles each player fills
            synergy_statement += "\nHere's how your players break down by role:"
            role_groups = {}
            for player, role in player_roles.items():
                if role not in role_groups:
                    role_groups[role] = []
                role_groups[role].append(player)
            
            for role, players in role_groups.items():
                role_display = role.replace('_', ' ').title()
                if len(players) == 1:
                    synergy_statement += f"\n - {role_display}: {players[0]}"
                else:
                    synergy_statement += f"\n - {role_display}: {self.get_players_string(players)}"
            
            # Then show redundancy concerns
            synergy_statement += "\n\nRedundancy Concerns:"
            for redundancy in redundancies:
                players_list, role, issue_type = redundancy
                role_display = role.replace('_', ' ').title()
                
                if issue_type == "major redundancy - only need one":
                    synergy_statement += f"\n - MAJOR ISSUE: You have multiple {role_display}s ({self.get_players_string(players_list)}) - teams typically only need one player in this role"
                elif issue_type == "too many in same role":
                    synergy_statement += f"\n - CONCERN: You have {len(players_list)} {role_display}s ({self.get_players_string(players_list)}) - this could create role confusion"
                elif issue_type == "oversaturation":
                    synergy_statement += f"\n - WARNING: You have {len(players_list)} players as {role_display}s ({self.get_players_string(players_list)}) - consider more diversity"
            
            synergy_statement += "\n\nRecommendation: Consider replacing one of the redundant players with someone who fills a different role to improve team balance."
        
        else:
            synergy_statement += "\n\nTeam Role Analysis:"
            synergy_statement += "\nYour team has good role diversity with minimal redundancy."
            
            # Still show the roles for context
            synergy_statement += "\nHere's how your players break down by role:"
            for player, role in player_roles.items():
                role_display = role.replace('_', ' ').title()
                synergy_statement += f"\n - {player}: {role_display}"       

        # Check for critical gaps in the team
        critical_gaps = self.check_critical_gaps(elite_scorers=elite_scorers, good_scorers=good_scorers, 
            elite_playmakers=elite_playmakers, good_playmakers=good_playmakers, elite_rebounders=elite_rebounders, 
            good_rebounders=good_rebounders, elite_defenders=elite_defenders, good_defenders=good_defenders)
        
        synergy_statement += critical_gaps
        
        # Check for aggregate gaps
        aggregate_gaps = self.check_aggregate_gaps(team_fingerprints)
        synergy_statement += aggregate_gaps


        # Predict a record out of 82 games
        wins, losses = self.predict_record(elite_scorers=elite_scorers, good_scorers=good_scorers, bad_scorers=bad_scorers,
                                           elite_defenders=elite_defenders, good_defenders=good_defenders, bad_defenders=bad_defenders,
                                           team_fingerprints=team_fingerprints, elite_playmakers=elite_playmakers, 
                                           elite_rebounders=elite_rebounders, redundancies=redundancies)


        synergy_statement += f'\n\nAnd finally, a record prediction for this team is:'
        synergy_statement += f'\n - {wins} - {losses}, {wins} wins and {losses} losses.'

        return synergy_statement


    """
        Normalize based on percentile ranges rather than absolute min/max.
        This creates more realistic distributions.
        
        Args:
            value: The stat value to normalize
            percentiles: Dict with keys like 'p10', 'p50', 'p90' representing
                        the 10th, 50th, and 90th percentiles for this stat
    """
    def percentile_normalize(self, value, percentiles):
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
            'defense': self.calculate_defensive_ability(player_stats),
            'usage%': player_stats['usage%'],
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
        #return json.dumps(team_fingerprint, indent=4)

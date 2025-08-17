from team_analyzer import teamAnalyzer


class outputGenerator:

    def __init__(self):
        self.teamAnalyzer = teamAnalyzer()

    def get_players_string(self, players):
        if len(players) > 1:
            result = ", ".join(players[:-1]) + ", and " + players[-1]
        else:
            result = players[0] if players else ""
        return result

    def generate_categorized_statement(self, player_categories):
        categorized_statement = '\nLets check out each of your players by category:'

        scoring = player_categories['scoring']
        categorized_statement += "\n - "
        if scoring['elite']:
            categorized_statement += f"{len(scoring['elite'])} elite scorer(s) ({self.get_players_string(scoring['elite'])}), "
        if scoring['good']:
            categorized_statement += f"{len(scoring['good'])} good scorer(s) ({self.get_players_string(scoring['good'])}), "
        if scoring['average']:
            categorized_statement += f"{len(scoring['average'])} average scorer(s) ({self.get_players_string(scoring['average'])}), "
        if scoring['bad']:
            categorized_statement += f"{len(scoring['bad'])} bad scorer(s) ({self.get_players_string(scoring['bad'])})."

        playmaking = player_categories['playmaking']
        categorized_statement += "\n - "
        if playmaking['elite']:
            categorized_statement += f"{len(playmaking['elite'])} elite playmaker(s) ({self.get_players_string(playmaking['elite'])}), "
        if playmaking['good']:
            categorized_statement += f"{len(playmaking['good'])} good playmaker(s) ({self.get_players_string(playmaking['good'])}), "
        if playmaking['average']:
            categorized_statement += f"{len(playmaking['average'])} average playmaker(s) ({self.get_players_string(playmaking['average'])}), "
        if playmaking['bad']:
            categorized_statement += f"{len(playmaking['bad'])} bad playmaker(s) ({self.get_players_string(playmaking['bad'])})."

        rebounding = player_categories['rebounding']
        categorized_statement += "\n - "
        if rebounding['elite']:
            categorized_statement += f"{len(rebounding['elite'])} elite rebounder(s) ({self.get_players_string(rebounding['elite'])}), "
        if rebounding['good']:
            categorized_statement += f"{len(rebounding['good'])} good rebounder(s) ({self.get_players_string(rebounding['good'])}), "
        if rebounding['average']:
            categorized_statement += f"{len(rebounding['average'])} average rebounder(s) ({self.get_players_string(rebounding['average'])}), "
        if rebounding['bad']:
            categorized_statement += f"{len(rebounding['bad'])} bad rebounder(s) ({self.get_players_string(rebounding['bad'])})."

        defense = player_categories['defense']
        categorized_statement += "\n - "
        if defense['elite']:
            categorized_statement += f"{len(defense['elite'])} elite defender(s) ({self.get_players_string(defense['elite'])}), "
        if defense['good']:
            categorized_statement += f"{len(defense['good'])} good defender(s) ({self.get_players_string(defense['good'])}), "
        if defense['average']:
            categorized_statement += f"{len(defense['average'])} average defender(s) ({self.get_players_string(defense['average'])}), "
        if defense['bad']:
            categorized_statement += f"{len(defense['bad'])} bad defender(s) ({self.get_players_string(defense['bad'])})."

        return categorized_statement
    

    def generate_usage_statement(self, usage_analysis):

        high_usage_players = usage_analysis['high']
        average_usage_players = usage_analysis['average']
        low_usage_players = usage_analysis['low']

        usage_statement = '\n\nLets go over the usage analysis on the team: '
        # If there is no high usage players:
        if len(high_usage_players) == 0:
            usage_statement += "\n - This squad has no proven stars who can take on a significant role"
            if len(low_usage_players) == 5:
                usage_statement += f"\n - No player on this squad had a significant role for a team last year ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 1 and len(low_usage_players) == 4:
                usage_statement += f"\n - You have 1 player who has proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), but 4 who did not ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 2  and len(low_usage_players) == 3:
                usage_statement += f"\n - You have 2 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), but 3 who did not ({self.get_players_string(low_usage_players)})"
            if len(average_usage_players) == 3 and len(low_usage_players) == 2:
                usage_statement += f"\n - You have 3 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), maybe one could breakout as a start with the opportunity, outside of them, 2 players with little usage ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 4  and len(low_usage_players) == 1:
                usage_statement += f"\n - You have 4 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}), this is a great chance for one or two to breakout and become a high usage star this year. You have one player with little usage ({self.get_players_string(low_usage_players)})"
            if len(average_usage_players) == 5:
                usage_statement += f"\n - You have 5 players who have proven to have an average role for a team last year ({self.get_players_string(average_usage_players)}). This is likely too much usage for one lineup, especially if one were to become a higher usage player."

        # 1 high usage players
        if len(high_usage_players) == 1:
            usage_statement += f"\n - This lineup has one true star who was taking on a big offensive load last year, and that is {high_usage_players[0]}."
            if len(low_usage_players) == 4:
                usage_statement += f"\n - Outside of the star, you have 4 players who didnt have much of a role last year ({self.get_players_string(low_usage_players)})."
                usage_statement += "\n - If the low usage players could all make a big jump collectively this year, the team could compete, but until then its likely losses ahead."
            if len(low_usage_players) == 3:
                usage_statement += f"\n - Outside of the star, the team has 3 low usage players ({self.get_players_string(low_usage_players)}) and 1 player who had average role last year ({self.get_players_string(average_usage_players)})."
                usage_statement += f"\n - If the {average_usage_players[0]} continued to improve, and another low usage player jumped as well, this could be a solid team."
            if len(low_usage_players) == 2:
                usage_statement += f"\n - Outside of the star, the team has 2 players with average roles last year ({self.get_players_string(average_usage_players)}), and 2 players with low usage last year ({self.get_players_string(low_usage_players)})."
                usage_statement += "\n - Assuming they all develop and get better in their roles, this team can expect to compete in the coming years."
            if len(low_usage_players) == 1:    
                usage_statement += f"\n - Outside of the star, the team has 3 players with average roles ({self.get_players_string(average_usage_players)}) and 1 low usage player ({self.get_players_string(low_usage_players)})."
                usage_statement += "\n - Assuming they grow together as a team one of the average players jumps into star status, this team is on track to be a contender."

        # 2 high usage players
        if len(high_usage_players) == 2:
            usage_statement += f"\n - This is a star driven lineup, 2 high usage players, {high_usage_players[0]} and {high_usage_players[1]}."
            if len(low_usage_players) == 3:
                usage_statement += f"\n - After the 2 stars, you do not have another player proven to be able to step into a third star role. ({self.get_players_string(low_usage_players)})"
            if len(average_usage_players) == 2 and len(low_usage_players) == 1:
                usage_statement += f"\n - After the 2 stars, you have 2 others players who have proven to be able to have roles on their team ({self.get_players_string(average_usage_players)}), and 1 player with low usage, maybe specialists ({self.get_players_string(low_usage_players)})."
            if len(low_usage_players) == 2 and len(average_usage_players) == 1:
                usage_statement += f"\n - After the 2 stars, you have 1 other player who has proven to be able to have a role on his team ({self.get_players_string(average_usage_players)}), and 2 players with low usage, maybe specialistst ({self.get_players_string(low_usage_players)})."
            if len(average_usage_players) == 3:
                usage_statement += f"\n - After the 2 stars, you have 3 other players who have proven to have roles on their teams ({self.get_players_string(average_usage_players)}), but this may cause for too many people wanting the ball."

        # 3 high usage player
        if len(high_usage_players) == 3:
            usage_statement += f"\n - This team is led by a trio of stars, all used to having the ball in their hand ({self.get_players_string(high_usage_players)})."
            usage_statement += "\n - With the right coaching and supporting cast, this squad could do some damage, but they all need to have the championship as goal number 1."
            if len(average_usage_players) == 2:
                usage_statement += f"\n - Outside of the 3 stars, you have 2 other players who had an average role last year ({self.get_players_string(average_usage_players)})."
                usage_statement += "\n - If one or two of them could take on a smaller role and accept less shots, this team could be good."
            if len(average_usage_players) == 1:
                usage_statement += f"\n - Outside of the 3 stars, you have 1 role player ({self.get_players_string(average_usage_players)}) and 1 player who didn't have much of a role last year ({self.get_players_string(low_usage_players)}). If everyone can keep their roles, this team should be primed to make a run."
            if len(low_usage_players) == 2:
                usage_statement += f"\n - Outside of the 3 stars, you have 2 players who did not have a big role last year ({self.get_players_string(low_usage_players)})."
                usage_statement += "\n - If they can continue to play their role around the 3 stars, this lineup could win a lot of games"

        # 4 high usage players
        if len(high_usage_players) == 4:
            usage_statement += f"\n - You have 4 high usage players, all on the same team ({self.get_players_string(high_usage_players)}). This is likely too much unless 2 of them are able and willing to take on a smaller role." 
            if len(average_usage_players) == 1:
                usage_statement += f"\n - Besides the 4 stars, you have 1 role player ({self.get_players_string(average_usage_players)}), another player used to getting some shots"
                usage_statement += "\n - With this many people wanting the ball, this is likely to not workout."
            if len(low_usage_players) == 1:
                usage_statement += f"\n - Besides the 4 stars, you have 1 player who did not have a significant role last year ({self.get_players_string(low_usage_players)})."
                usage_statement += "\n - This means that if 2 guys can take on a smaller role, this lineup has a great opportunity to compete"

        # 5 high usage players
        if len(high_usage_players) == 5:
            usage_statement += f"\n - You have 5 high usage players, all on the same team ({self.get_players_string(high_usage_players)}). This is more likely an All-Star lineup rather than one that could truly compete for a championship"
            usage_statement += "\n - Between egos and salaries, this team is not likely to stay together long enough to build the chemistry to win at the highest level."

        return usage_statement
    

    def generate_combo_statement(self, good_combos):

        combo_statement = '\n\nHere are any potential good player combinations:'
        for combo in good_combos:
            type = combo['type']

            # Elite scorer + elite playmaker
            if type == 'elite_scorer_playmaker':
                combo_statement += f"\n - Scorer: {combo['scorer'][0]} and playmaker: {combo['playmaker'][0]} will make for a lethal duo on the offensive end."

            # Elite scorer + good scorer
            if type == 'great_scoring':
                combo_statement += f"\n - Elite scorer: {combo['eliteScorer'][0]} and good scorer: {combo['goodScorer'][0]} will give the team enough solid scoring options to be effective."

            # Elite scorer + 2 good scorers
            if type == 'great_scoring_trio':
                combo_statement += f"\n - Elite scorer: {combo['eliteScorer'][0]} and good scorers: {self.get_players_string(combo['goodScorers'])} will provide lots of offensive options."

            # Elite scorer + elite playmaker + elite rebounder + elite defender
            if type == 'four_headed_monster':
                combo_statement += f"\n - Elite scorer: {combo['scorer'][0]}, elite playmaker: {combo['playmaker'][0]}, elite rebounder: {combo['rebounder'][0]}, and elite defender: {combo['defender'][0]} are 4 players you will want on the court in all the biggest moments. Together they give you elite capabilities for every ability."

            # Elite defender + elite rebounder
            if type == 'defender_rebounder':
                combo_statement += f"\n - Elite rebounder: {combo['rebounder'][0]} and elite defender: {combo['defender'][0]} will help limit the other teams second chance opportunities."

            # 2 Elite playmakers
            if type == 'dual_playmaker':
                combo_statement += f"\n - Elite playmakers: {self.get_players_string(combo['playmakers'])} will help keep the offense moving and incorporate everyone."

            # Elite scorer + elite playmaker + elite rebounder
            if type == 'fundamental_trio':
                combo_statement += f"\n - Elite scorer: {combo['scorer'][0]}, elite playmaker: {combo['playmaker'][0]}, and elite rebounder: {combo['rebounder'][0]} cover your most fundamental needs."

            # 2 good scorers + elite playmaker
            if type == 'upcoming_trio':
                combo_statement += f"\n - Good scorers: {self.get_players_string(combo['scorers'])} and elite playmaker {combo['playmaker'][0]} will generate your offense lots of points."

        return combo_statement


    def generate_redundancy_statement(self, redundant_pairs, player_roles):

        redundancy_statement = '\n\nLets look for any redundant player pairs and what roles your lineup has:'
        redundancy_statement += '\nRoles first:'

        for player, role in player_roles.items():
            redundancy_statement += f"\n - {player}'s role: {role}"

        redundancy_statement += f'\n\nNow redudant pairs: '
        for players, role, message in redundant_pairs:
            redundancy_statement += f'\n - Players: {self.get_players_string(players)} both fill the role {role}.'

        return redundancy_statement
    

    def generate_critical_gaps_statement(self, gaps, abundances):
            
        # Is there any gaps
        if gaps:
            gaps_statement = '\n\nWhat critical gaps does your team have: '
            gaps_statement += f'\n - '
            for gap in gaps:
                gaps_statement += f'Gap: {gap}, '

            # If there is gaps, what could fill them?
            if abundances:
                gaps_statement += f'\n\nWhat parts of the team could you sacrifice to fill those gaps?: '
                gaps_statement += f'\n - '
                for ability in abundances:
                    gaps_statement += f'{ability}, '

        else:
            gaps_statement = '\n\nNo critical gaps found in the lineup.'

        return gaps_statement
    
    
    def generate_aggregate_gaps_statement(self, aggregate_gaps):

        if aggregate_gaps:
            gaps_statement = "\n\nHere is where your teams totals don't quite meet a good teams needs: "

            for skill in aggregate_gaps:
                gaps_statement += f"\n - The team is lacking in {skill}"

        else:
            gaps_statement = '\n\nTeam meets the needed totals for all skills'

        return gaps_statement
    
    
    def generate_record_statement(self, wins, losses):
        record_statement = '\n\nBased on your players stats, usage rates, and tendencies, a predicted record for this squad is:'
        record_statement += f'\n - {wins} wins and {losses} losses, {wins} - {losses}'
        return record_statement
    

    def generate_final_output(self, team_analysis):

        final_output = 'Thank you for inputting your team, here is an analysis of the lineup:'

        # Get the categorization statement, __ elite scoeres, __ good , __ bad , etc... 
        categorized_statement = self.generate_categorized_statement(team_analysis['player_categories'])
        final_output += categorized_statement

        # Get the usage statement
        usage_statement = self.generate_usage_statement(team_analysis['usage_analysis'])
        final_output += usage_statement

        # Get the good combination statement
        combo_statement = self.generate_combo_statement(team_analysis['good_combos'])
        final_output += combo_statement

        # Get the statement for any redundancy amongst players
        redundancy_statement = self.generate_redundancy_statement(team_analysis['redundant_pairs'], team_analysis['player_roles'])
        final_output += redundancy_statement

        # Get the statement on any critical gaps + abundances
        critical_gaps_statement = self.generate_critical_gaps_statement(team_analysis['gaps'], team_analysis['abundances'])
        final_output += critical_gaps_statement

        # Get the statement on any aggregate gaps
        aggregate_gaps_statement = self.generate_aggregate_gaps_statement(team_analysis['aggregate_gaps'])
        final_output += aggregate_gaps_statement

        # Get the predicted record statement
        predicted_record_statement = self.generate_record_statement(team_analysis['wins'], team_analysis['losses'])
        final_output += predicted_record_statement
        
        return final_output
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

    def generate_categorized_statement(self, scoring, playmaking, rebounding, defense):
        categorized_statement = '\nLets check out each of your players by category:'

        categorized_statement += "\n - "
        if scoring['elite']:
            categorized_statement += f"{len(scoring['elite'])} elite scorer(s) ({self.get_players_string(scoring['elite'])}), "
        if scoring['good']:
            categorized_statement += f"{len(scoring['good'])} good scorer(s) ({self.get_players_string(scoring['good'])}), "
        if scoring['average']:
            categorized_statement += f"{len(scoring['average'])} average scorer(s) ({self.get_players_string(scoring['average'])}), "
        if scoring['bad']:
            categorized_statement += f"{len(scoring['bad'])} bad scorer(s) ({self.get_players_string(scoring['bad'])})."

        categorized_statement += "\n - "
        if playmaking['elite']:
            categorized_statement += f"{len(playmaking['elite'])} elite playmaker(s) ({self.get_players_string(playmaking['elite'])}), "
        if playmaking['good']:
            categorized_statement += f"{len(playmaking['good'])} good playmaker(s) ({self.get_players_string(playmaking['good'])}), "
        if playmaking['average']:
            categorized_statement += f"{len(playmaking['average'])} average playmaker(s) ({self.get_players_string(playmaking['average'])}), "
        if playmaking['bad']:
            categorized_statement += f"{len(playmaking['bad'])} bad playmaker(s) ({self.get_players_string(playmaking['bad'])})."

        categorized_statement += "\n - "
        if rebounding['elite']:
            categorized_statement += f"{len(rebounding['elite'])} elite rebounder(s) ({self.get_players_string(rebounding['elite'])}), "
        if rebounding['good']:
            categorized_statement += f"{len(rebounding['good'])} good rebounder(s) ({self.get_players_string(rebounding['good'])}), "
        if rebounding['average']:
            categorized_statement += f"{len(rebounding['average'])} average rebounder(s) ({self.get_players_string(rebounding['average'])}), "
        if rebounding['bad']:
            categorized_statement += f"{len(rebounding['bad'])} bad rebounder(s) ({self.get_players_string(rebounding['bad'])})."

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
    

    def generate_final_output(self, team_fingerprints):

        final_output = ''

        scoring, playmaking, rebounding, defense, team_totals = self.teamAnalyzer.seperate_players(team_fingerprints)
        categorized_statement = self.generate_categorized_statement(scoring, playmaking, rebounding, defense)
        final_output += categorized_statement

        return final_output
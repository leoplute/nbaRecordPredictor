from grab_player_data import grabPlayerData
from stats_calculator import statsCalculator
from team_analyzer import teamAnalyzer
from output_generator import outputGenerator
import json

class FantasyModel:

    def __init__(self):
        self.grabPlayerData = grabPlayerData()
        self.statsCalculator = statsCalculator()
        self.teamAnalyzer = teamAnalyzer()
        self.outputGenerator = outputGenerator()


    def evaluate_team(self, players):

        teamStats = self.grabPlayerData.get_team_stats(players)

        if not isinstance(teamStats, dict) or not teamStats:
            return "Error: could not get full team stats."

        team_fingerprint = {}

        for player_name, stats in teamStats.items():
            player_fingerprint = self.statsCalculator.fingerprint(stats)
            team_fingerprint[player_name] = player_fingerprint

        analysis = self.teamAnalyzer.analyze_team(team_fingerprint)

        output = self.outputGenerator.generate_final_output(analysis)

        return output

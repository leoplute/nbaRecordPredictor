Leo Plute
8/17/25

NBA Lineup Analyzer
 - A basketball lineup analysis tool that evaluates lineups using real nba player statistics and advanced statistis

 Overview
  - The NBA Lineup Analyzer is a desktop application that takes in 5 players and provides a detailed analysis including player catergorization, usage rates, team chemistry, potential weaknesses, and predicing a record. Built with Python and PySide6, it features a clean HUI and real-time data fetching from NBA API.
   - API found at: https://github.com/nprasad2077/nbaStats/blob/main/README.md

Features:
 - Player Analysis: Categorizes players into elite/good/average/bad tiers across 4 key skills: scoring, playmaking, rebounding, and defense.
 - Team Chemistry Analysis: Using usage rates, player role redundancy checks, and optimal player combinations, the program can predict what the team chemistry would be like amongst the lineup.
 - Gap Analysis: The program looks for gaps in the team by looking for skill deficiencies among the lineup, areas of abundance for potential trades, and looks at the aggregate team totals to benchmark against the 2024-25 NBA Champion Oklahoma City Thunder's starting 5.
 - Predictive Modeling: Win-loss record prediction based on critical analysis
 - User friendly interface: 
  - Clean desktop GUI with position-labeled input fields
  - Enter/tab key navigation between inputs
  - Real-time loading animations
  - Comprehensive text analysis output

Installs needed:
 - pip install PySide6
 - pip install requests
 - pip install unidecode

Architecture:
 - This application follows the model-view-controller (MVC) pattern:
  - main.py, application entry point
  - view.py: Pyside6 GUI interface creation with user inputs fields and output display
  - controller.py: Event handling as well as UI state management
  - model.py: Logic coordinator

Data processing pipeline:
 - grab_player_data.py: NBA API integration with smart player ID resolution
 - stats_calculator.py: Advanced metrics calculations using percentile normalization
 - team_analyzer.py: Uses player 'fingerprints' to establish team chemistry, role analysis, and predictive modeling
 - ouput_generator.py: Natural language analysis report generation

Usage:
 1. Input players in the labeled position input boxes
 2. Using tab or enter you can move between inputs fields
 3. After 5 players are inputted, use the submit button or click enter in the last field to analyze the lineup
 4. Wait for a moment and review the analysis including:
  - Player skill categorization
  - Usage rate analysis
  - Good player combinations
  - Role redundancies
  - Critical gaps + strengths
  - Predicted record

Player name format:
 - Use players full names ( 'T.J. McConnell', 'Stephen Curry' )
 - Special characters are automatically handled
 - Periods in names like 'T.J. McConnell' are automatically processed


Developement Notes:
Current limitations:
 - Relies on free NBA API with limited number of team statistics
 - Only uses data from the 2024-2025 season
 - Basic error handling for network issues

Planned improvements:
 - Enhanced error handling
 - Historical season comparison
 - Advance UI
 - Potentially even more analysis
  
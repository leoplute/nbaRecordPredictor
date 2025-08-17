import pytest
import requests

def find_player_id(player_name, season=2025):
    """Find player ID by searching all players in the season"""
    BASE_URL = "https://api.server.nbaapi.com/api/playertotals"
    headers = {"accept": "application/json"}
    
    page = 1
    while page <= 20:  # Safety limit
        params = {
            "page": page,
            "pageSize": 1000,
            "season": season,
        }
        
        response = requests.get(BASE_URL, params=params, headers=headers)
        if response.status_code != 200:
            break
            
        data = response.json()
        players = data.get("data", [])
        
        if not players:
            break
            
        for player in players:
            if player.get('playerName', '').lower() == player_name.lower():
                return player.get('playerId')
                
        page += 1
    
    return None

def test_find_specific_player():
    """Test to find a specific player's ID - CHANGE THE NAME HERE"""
    
    # *** CHANGE THIS PLAYER NAME TO WHOEVER YOU WANT TO TEST ***
    player_name = "Jalen Williams"
    
    player_id = find_player_id(player_name)
    
    print(f"\nPlayer: {player_name}")
    print(f"Player ID: {player_id}")
    
    assert player_id is not None, f"Could not find player ID for {player_name}"


if __name__ == "__main__":
    test_find_specific_player()
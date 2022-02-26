from typing import Sequence
import game_rules
import player as player_module



def test_player_list():
    game_data = game_rules.GameData()
    player = player_module.Player()
    player1 = player_module.Player()
    assert game_data.player_list() is not None
    assert game_data.next_player() is None

    player.name = "player0"
    game_data.append_player(player)
    assert game_data.next_player() is player

    player1.name = "player1"
    game_data.append_player(player1)
    assert game_data.next_player() is player1

    assert game_data.next_player() is player




def test_update_keys():
    game_data = game_rules.GameData()
    sequence = [1]

    game_data.update_keys(sequence)
    assert game_data.keys is sequence




def test_players_count():
    game_data = game_rules.GameData()
    player = player_module.Player("player0")
    player1 = player_module.Player("player1")

    assert game_data.players_count() == 0

    game_data.append_player(player)
    assert game_data.players_count() == 1

    game_data.append_player(player1)
    assert game_data.players_count() == 2
    


def test_visit_assign_character():
    game_data = game_rules.GameRules()
    player = player_module.Player("player0")

    assert player.character is None
    game_data.visit_assign_character(player)
    assert player.character is not None
    
    

def test_visit_initialize_player():
    game_data = game_rules.GameRules()
    player = player_module.Player("player0")

    assert player.life == 0
    player.character = player_module.Elie()
    game_data.visit_initialize_player(player)
    assert player.life != 0
    
    

def test_is_first_death():
    game_data = game_rules.GameData()

    assert game_data.is_first_death() == False
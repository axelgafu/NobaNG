from tkinter import Place
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
    player.character = player_module.Elie(player)
    game_data.visit_initialize_player(player)
    assert player.life != 0
    
    

def test_is_first_death():
    game_data = game_rules.GameData()

    assert game_data.is_first_death() == False
    


def test_new_game_data():
    game_data = game_rules.GameData()

    assert game_rules.GameData() is game_rules.GameData()
    


def test_new_game_rules():
    assert game_rules.GameRules() is game_rules.GameRules()
    


def test_visit_throw_dice_ghost():
    rules = game_rules.GameRules()
    player = player_module.Player()
    data = game_rules.GameData()

    player.status = player_module.Player.S_GHOST
    data.append_player(player)
    assert rules.visit_throw_dice(data, True) != None
    


def test_visit_lock_dice_bomb():
    rules = game_rules.GameRules()
    player = player_module.Player()
    data = game_rules.GameData()

    player.dice_value = ["bomb","","bomb","","bomb",""]
    assert rules.visit_lock_dice(data) == False
    


def test_visit_2xlife():
    rules = game_rules.GameRules()
    player = player_module.Player()

    player.max_life = 9
    player.life = 1
    player.dice_value = ["2xlife","","2xlife","","2xlife",""]
    assert rules.visit_life(player) == False
    assert player.life == 7
    


def test_visit_life():
    rules = game_rules.GameRules()
    player = player_module.Player()

    player.max_life = 9
    player.life = 1
    player.dice_value = ["life","","life","","life",""]
    assert rules.visit_life(player) == False
    assert player.life == 4



def test_visit_Doc_stats_rules():
    player = player_module.Player()

    player.life = 0
    player.character = player_module.Doc(player)
    player.character.visit_character_stats_rules("1")
    player.character.visit_character_stats_rules("2")
    assert player.life == 4



def test_visit_Elie_counter_rules():
    rules = game_rules.GameRules()
    player = player_module.Player()
    player_target = player_module.Player()
    game_data = game_rules.GameData()

    game_data.append_player(player)
    game_data.append_player(player_target)

    player.life = 2
    player.character = player_module.Elie(player)
    
    player_target.life = 2
    player_target.character = player_module.Jose(player_target)

    dice:list[game_rules.Die] = game_data.shuffle_dice()
    dice[0].value = "1"
    dice[1].value = "2"
    dice[2].value = "life"
    
    dice[0].assign(player_target)
    dice[1].assign(player_target)
    dice[2].assign(player)

    assert rules.visit_character_counter_rules(game_data) == False
    dice[0].execute()
    dice[1].execute()
    dice[2].execute()

    assert player_target.life == 2
    assert player.life == 1
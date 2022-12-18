# Automatically generated by Pynguin.
import state as module_0
import player as module_1
import game_rules as module_2


def test_case_0():
    float_0 = -1389.4
    perform_activity_0 = module_0.PerformActivity()
    assert perform_activity_0.state_id == 'ST_ACTIVITY'
    var_0 = perform_activity_0.transitionate(float_0)
    assert var_0.state_id == 'ST_TURN'
    assert var_0.re_rol == 3
    assert var_0.sub_state == 1
    assert module_0.PlayGame.STATE_THROWING_DICE == 1
    assert module_0.PlayGame.STATE_PLAYER_DECIDING == 2
    assert module_0.PlayGame.STATE_ENDING_TURN == 3


def test_case_1():
    lobby_0 = module_0.Lobby()
    assert lobby_0.state_id == 'ST_LOBBY'
    list_0 = [lobby_0]
    quit_0 = module_0.Quit()
    assert quit_0.state_id == 'ST_QUIT'
    var_0 = quit_0.update(list_0)
    assert var_0 is None


def test_case_2():
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'


def test_case_3():
    quit_0 = module_0.Quit()
    assert quit_0.state_id == 'ST_QUIT'


def test_case_4():
    play_game_0 = module_0.PlayGame()
    assert play_game_0.state_id == 'ST_TURN'
    assert play_game_0.re_rol == 3
    assert play_game_0.sub_state == 1
    assert module_0.PlayGame.STATE_THROWING_DICE == 1
    assert module_0.PlayGame.STATE_PLAYER_DECIDING == 2
    assert module_0.PlayGame.STATE_ENDING_TURN == 3
    var_0 = play_game_0.handle_answer_rerol()
    game_data_0 = None
    lobby_0 = module_0.Lobby()
    assert lobby_0.state_id == 'ST_LOBBY'
    var_1 = lobby_0.update(game_data_0)
    player_0 = module_1.Player()
    perform_activity_0 = module_0.PerformActivity()
    assert perform_activity_0.state_id == 'ST_ACTIVITY'
    var_2 = perform_activity_0.transitionate(player_0)
    assert len(var_0) == 2
    assert var_1 is None
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.max_life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.dice_value == ['', '', '', '', '', '']
    assert player_0.character is None
    assert player_0.role is None
    assert player_0.attack_vector == {'clockwise': [], 'backwards': []}
    assert var_2.state_id == 'ST_TURN'
    assert var_2.re_rol == 3
    assert var_2.sub_state == 1
    assert module_1.Player.S_DEAD == 'dead'
    assert module_1.Player.S_ALIVE == 'alive'
    assert module_1.Player.S_GHOST == 'ghost'
    quit_0 = module_0.Quit()
    assert quit_0.state_id == 'ST_QUIT'
    var_3 = quit_0.update(lobby_0)
    assert var_3 is None


def test_case_5():
    play_game_0 = module_0.PlayGame()
    assert play_game_0.state_id == 'ST_TURN'
    assert play_game_0.re_rol == 3
    assert play_game_0.sub_state == 1
    assert module_0.PlayGame.STATE_THROWING_DICE == 1
    assert module_0.PlayGame.STATE_PLAYER_DECIDING == 2
    assert module_0.PlayGame.STATE_ENDING_TURN == 3
    var_0 = play_game_0.set_player_choices()


def test_case_6():
    play_game_0 = module_0.PlayGame()
    assert play_game_0.state_id == 'ST_TURN'
    assert play_game_0.re_rol == 3
    assert play_game_0.sub_state == 1
    assert module_0.PlayGame.STATE_THROWING_DICE == 1
    assert module_0.PlayGame.STATE_PLAYER_DECIDING == 2
    assert module_0.PlayGame.STATE_ENDING_TURN == 3
    var_0 = play_game_0.handle_answer_rerol()
    lobby_0 = module_0.Lobby()
    assert lobby_0.state_id == 'ST_LOBBY'
    player_0 = module_1.Player()
    perform_activity_0 = module_0.PerformActivity()
    assert perform_activity_0.state_id == 'ST_ACTIVITY'
    var_1 = perform_activity_0.transitionate(player_0)
    assert len(var_0) == 2
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.max_life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.dice_value == ['', '', '', '', '', '']
    assert player_0.character is None
    assert player_0.role is None
    assert player_0.attack_vector == {'clockwise': [], 'backwards': []}
    assert var_1.state_id == 'ST_TURN'
    assert var_1.re_rol == 3
    assert var_1.sub_state == 1
    assert module_1.Player.S_DEAD == 'dead'
    assert module_1.Player.S_ALIVE == 'alive'
    assert module_1.Player.S_GHOST == 'ghost'
    quit_0 = module_0.Quit()
    assert quit_0.state_id == 'ST_QUIT'
    quit_1 = module_0.Quit()
    assert quit_1.state_id == 'ST_QUIT'
    quit_2 = module_0.Quit()
    assert quit_2.state_id == 'ST_QUIT'


def test_case_7():
    set_0 = set()
    game_rules_0 = module_2.GameRules()
    play_game_0 = module_0.PlayGame()
    assert play_game_0.state_id == 'ST_TURN'
    assert play_game_0.re_rol == 3
    assert play_game_0.sub_state == 1
    assert module_0.PlayGame.STATE_THROWING_DICE == 1
    assert module_0.PlayGame.STATE_PLAYER_DECIDING == 2
    assert module_0.PlayGame.STATE_ENDING_TURN == 3
    state_0 = None
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'
    state_1 = display_0.next_state(state_0)
    assert state_1.state_id == 'ST_GENERAL'
    display_1 = module_0.Display()
    assert display_1.state_id == 'ST_GENERAL'
    state_2 = display_1.next_state(state_1)
    assert state_2.state_id == 'ST_GENERAL'
    list_0 = [set_0, set_0]
    quit_0 = module_0.Quit()
    assert quit_0.state_id == 'ST_QUIT'
    var_0 = quit_0.update(list_0)
    assert game_rules_0 is not None
    assert var_0 is None
    display_2 = module_0.Display()
    assert display_2.state_id == 'ST_GENERAL'
    str_0 = display_2.get_message()
    assert str_0 == ''


def test_case_8():
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'
    str_0 = display_0.get_message()
    assert str_0 == ''

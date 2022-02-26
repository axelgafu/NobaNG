# Automatically generated by Pynguin.
import state as module_0
import player as module_1


def test_case_0():
    play_game_0 = module_0.PlayGame()
    assert play_game_0.state_id == 'ST_TURN'
    assert play_game_0.re_rol == 3


def test_case_1():
    game_start_0 = module_0.GameStart()
    assert game_start_0.state_id == 'ST_GAME_START'


def test_case_2():
    float_0 = -708.555345
    game_over_0 = module_0.GameOver()
    assert game_over_0.state_id == 'ST_GAME_OVER'
    var_0 = game_over_0.update(float_0)


def test_case_3():
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'


def test_case_4():
    str_0 = 'tq[/qy\t\n'
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'
    state_0 = display_0.message(str_0)
    assert state_0.state_id == 'ST_GENERAL'


def test_case_5():
    quit_0 = module_0.Quit()
    assert quit_0.state_id == 'ST_QUIT'
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'
    str_0 = display_0.get_message()
    assert str_0 == ''
    perform_activity_0 = module_0.PerformActivity()
    assert perform_activity_0.state_id == 'ST_ACTIVITY'
    state_0 = module_0.State()
    assert state_0.state_id == 'ST_GENERAL'
    state_1 = display_0.next_state(state_0)
    assert state_1.state_id == 'ST_GENERAL'
    var_0 = perform_activity_0.transitionate(quit_0)
    assert var_0.state_id == 'ST_TURN'
    assert var_0.re_rol == 3
    str_1 = 'd|E~\nO-nh*D*a exv%A'
    var_1 = quit_0.update(str_1)
    assert var_1 is None
    quit_1 = module_0.Quit()
    assert quit_1.state_id == 'ST_QUIT'
    display_1 = module_0.Display()
    assert display_1.state_id == 'ST_GENERAL'
    var_2 = quit_1.update(display_1)
    assert var_2 is None
    display_2 = module_0.Display()
    assert display_2.state_id == 'ST_GENERAL'
    var_3 = display_2.update(quit_1)
    assert var_3 is None


def test_case_6():
    str_0 = 'o9j'
    player_0 = module_1.Player(str_0)
    lobby_0 = module_0.Lobby()
    assert lobby_0.state_id == 'ST_LOBBY'
    display_0 = module_0.Display()
    assert display_0.state_id == 'ST_GENERAL'
    bytes_0 = b'J\x12\x0b4\xcc'
    state_0 = display_0.using(bytes_0)
    assert state_0.state_id == 'ST_GENERAL'
    perform_activity_0 = module_0.PerformActivity()
    assert perform_activity_0.state_id == 'ST_ACTIVITY'
    bool_0 = None
    var_0 = state_0.set_transitionable(bool_0)

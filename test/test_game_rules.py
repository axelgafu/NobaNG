# Automatically generated by Pynguin.
import player as module_0
import game_rules as module_1


def test_case_0():
    player_0 = module_0.Player()
    bool_0 = True
    game_rules_0 = module_1.GameRules()
    bool_1 = game_rules_0.visit_throw_dice(player_0, bool_0)
    assert bool_1 is False
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'


def test_case_1():
    game_rules_0 = module_1.GameRules()


def test_case_2():
    player_0 = module_0.Player()
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.visit_assign_character(player_0)


def test_case_3():
    player_0 = module_0.Player()
    str_0 = '2uK.Ru&#'
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.visit_initialize_player(player_0)
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.dice_value == ['', '', '', '', '', '']
    assert player_0.dice_re_roll == [3, 3, 3, 3, 3, 3]
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert var_0 is None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'
    var_1 = game_rules_0.throw_alive(player_0, str_0)
    assert var_1 is None


def test_case_4():
    player_0 = module_0.Player()
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.throw_ghost(player_0)
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert var_0 is None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'
    bool_0 = game_rules_0.visit_life(player_0)
    assert bool_0 is False
    bool_1 = False
    bool_2 = game_rules_0.visit_throw_dice(player_0, bool_1)
    assert bool_2 is False


def test_case_5():
    player_0 = module_0.Player()
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.throw_ghost(player_0)
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.dice_re_roll != [3, 3, 3, 3, 3, 3]
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert var_0 is None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'
    bool_0 = game_rules_0.visit_life(player_0)
    assert bool_0 is False
    var_1 = game_rules_0.visit_assign_character(player_0)
    assert var_1 is None
    var_2 = game_rules_0.visit_initialize_player(player_0)
    assert player_0.life == 8
    assert player_0.dice_count == 5
    assert var_2 is None


def test_case_6():
    player_0 = module_0.Player()
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.throw_ghost(player_0)
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.dice_value != ['', '', '', '', '', '']
    assert player_0.dice_re_roll >= [0, 3, 3, 3, 3, 3]
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert var_0 is None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'
    bool_0 = game_rules_0.visit_life(player_0)
    assert bool_0 is False
    bool_1 = game_rules_0.visit_throw_dice(player_0, bool_0)
    assert bool_1 is False


def test_case_7():
    player_0 = module_0.Player()
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.throw_ghost(player_0)
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert var_0 is None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'


def test_case_8():
    player_0 = module_0.Player()
    game_rules_0 = module_1.GameRules()
    var_0 = game_rules_0.throw_ghost(player_0)
    assert player_0.name == ''
    assert player_0.life == 0
    assert player_0.arrows == 0
    assert player_0.dice_count == 6
    assert player_0.status == 'alive'
    assert player_0.dice_value != ['', '', '', '', '', '']
    assert player_0.dice_re_roll != [3, 3, 3, 3, 3, 3]
    assert player_0.character is None
    assert player_0.role is None
    assert game_rules_0 is not None
    assert var_0 is None
    assert module_0.Player.S_DEAD == 'dead'
    assert module_0.Player.S_ALIVE == 'alive'
    assert module_0.Player.S_GHOST == 'ghost'
    var_1 = game_rules_0.visit_assign_character(player_0)
    assert var_1 is None
    bool_0 = False
    bool_1 = game_rules_0.visit_throw_dice(player_0, bool_0)
    assert bool_1 is False
    assert player_0.dice_re_roll > [0, 0, 0, 0, 0, 0]
    var_2 = game_rules_0.visit_assign_character(player_0)
    assert var_2 is None
    game_rules_1 = module_1.GameRules()
    assert game_rules_1 is not None
    bool_2 = game_rules_1.visit_life(player_0)
    assert bool_2 is False
    var_3 = game_rules_1.visit_initialize_player(player_0)
    assert player_0.life == 8
    assert player_0.dice_count == 5
    assert var_3 is None

# Automatically generated by Pynguin.
import game_rules as module_0
import player as module_1


def test_case_0():
    try:
        game_data_0 = module_0.GameData()
    except BaseException:
        pass


def test_case_1():
    try:
        game_data_0 = module_0.GameData()
    except BaseException:
        pass


def test_case_2():
    try:
        player_0 = module_1.Player()
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        var_0 = game_rules_0.visit_assign_character(player_0)
        assert player_0.name == ''
        assert player_0.life == 0
        assert player_0.max_life == 0
        assert player_0.arrows == 0
        assert player_0.dice_count == 6
        assert player_0.status == 'alive'
        assert player_0.dice_value == ['', '', '', '', '', '']
        assert player_0.role is None
        assert player_0.attack_vector == {'clockwise': [], 'backwards': []}
        assert var_0 is None
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_data_0 = module_0.GameData()
    except BaseException:
        pass


def test_case_3():
    try:
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        player_0 = module_1.Player()
        game_rules_1 = module_0.GameRules()
        assert game_rules_1 is not None
        bool_0 = game_rules_1.visit_life(player_0)
        assert bool_0 is False
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_data_0 = module_0.GameData()
    except BaseException:
        pass


def test_case_4():
    try:
        player_0 = module_1.Player()
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        var_0 = game_rules_0.visit_initialize_player(player_0)
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
        assert var_0 is None
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_data_0 = module_0.GameData()
    except BaseException:
        pass


def test_case_5():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        var_1 = die_brave_0.execute()
        assert var_1 is None
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_0 = game_rules_0.visit_life(player_0)
        assert bool_0 is False
        var_2 = game_rules_0.visit_initialize_player(player_0)
        assert var_2 is None
        list_0 = die_brave_0.get_dice()
        assert list_0 == ['2x1', '2x2', 'bomb', 'arrow', 'shoot', 'bullet']
        bool_1 = game_rules_0.visit_status(player_0, game_data_0)
    except BaseException:
        pass


def test_case_6():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        list_0 = game_rules_0.throw_ghost(game_data_0)
    except BaseException:
        pass


def test_case_7():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = die_0.get_selected_targets()
    except BaseException:
        pass


def test_case_8():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        list_0 = die_brave_0.get_dice()
        assert list_0 == ['2x1', '2x2', 'bomb', 'arrow', 'shoot', 'bullet']
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        list_1 = game_data_0.shuffle_dice()
    except BaseException:
        pass


def test_case_9():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        list_0 = game_rules_0.throw_alive(game_data_0, player_0)
    except BaseException:
        pass


def test_case_10():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        die_regular_0 = module_0.DieRegular(game_data_0)
        assert die_regular_0.value == ''
        list_0 = die_regular_0.get_dice()
        assert list_0 == ['1', '2', 'shoot', 'arrow', 'bomb', 'life']
        die_1 = module_0.Die(game_data_0)
        assert die_1.value == ''
        game_data_1 = module_0.GameData()
    except BaseException:
        pass


def test_case_11():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        str_0 = '0[\tHH'
        list_0 = die_brave_0.get_dice()
        assert list_0 == ['2x1', '2x2', 'bomb', 'arrow', 'shoot', 'bullet']
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        var_1 = die_0.lock(str_0)
        assert var_1 is None
        die_1 = module_0.Die(game_data_0)
        assert die_1.value == ''
        die_coward_0 = module_0.DieCoward(game_data_0)
        assert die_coward_0.value == ''
        list_1 = die_coward_0.get_dice()
        assert list_1 == ['1', 'no_arrow', 'bomb', 'arrow', '2xlife', 'life']
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_0 = game_rules_0.visit_life(player_0)
        assert bool_0 is False
        var_2 = game_rules_0.visit_initialize_player(player_0)
        assert var_2 is None
        game_data_1 = module_0.GameData()
    except BaseException:
        pass


def test_case_12():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        list_0 = die_0.get_available_targets(game_data_0)
    except BaseException:
        pass


def test_case_13():
    try:
        game_data_0 = None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        var_0 = die_0.shuffle()
    except BaseException:
        pass


def test_case_14():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        var_1 = die_brave_0.execute()
        assert var_1 is None
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_0 = game_rules_0.visit_life(player_0)
        assert bool_0 is False
        var_2 = game_rules_0.visit_initialize_player(player_0)
        assert var_2 is None
        list_0 = die_0.get_dice()
        assert list_0 == []
        bool_1 = game_rules_0.visit_status(player_0, game_data_0)
    except BaseException:
        pass


def test_case_15():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        bool_0 = die_0.is_skippable()
        assert bool_0 is False
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_1 = game_rules_0.visit_life(player_0)
        assert bool_1 is False
        var_1 = game_rules_0.visit_initialize_player(player_0)
        assert var_1 is None
        game_data_1 = module_0.GameData()
    except BaseException:
        pass


def test_case_16():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        die_1 = module_0.Die(game_data_0)
        assert die_1.value == ''
        var_1 = die_0.visit_character_stats_rules()
    except BaseException:
        pass


def test_case_17():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        var_1 = die_brave_0.execute()
        assert var_1 is None
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_0 = game_rules_0.visit_life(player_0)
        assert bool_0 is False
        list_0 = die_brave_0.get_dice()
        assert list_0 == ['2x1', '2x2', 'bomb', 'arrow', 'shoot', 'bullet']
        var_2 = game_rules_0.visit_initialize_player(player_0)
        assert var_2 is None
        bool_1 = game_rules_0.visit_lock_dice(game_data_0)
    except BaseException:
        pass


def test_case_18():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_0 = game_rules_0.visit_life(player_0)
        assert bool_0 is False
        list_0 = die_brave_0.get_dice()
        assert list_0 == ['2x1', '2x2', 'bomb', 'arrow', 'shoot', 'bullet']
        var_1 = game_rules_0.visit_initialize_player(player_0)
        assert var_1 is None
        bool_1 = game_rules_0.visit_life(player_0)
        assert bool_1 is False
        bool_2 = game_rules_0.visit_character_counter_rules(game_data_0)
    except BaseException:
        pass


def test_case_19():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        game_rules_0 = module_0.GameRules()
        assert game_rules_0 is not None
        bool_0 = game_rules_0.visit_life(player_0)
        assert bool_0 is False
        list_0 = die_brave_0.get_dice()
        assert list_0 == ['2x1', '2x2', 'bomb', 'arrow', 'shoot', 'bullet']
        die_1 = module_0.Die(game_data_0)
        assert die_1.value == ''
        die_1.assign(player_0)
        var_1 = game_rules_0.visit_initialize_player(player_0)
        assert var_1 is None
        bool_1 = game_rules_0.visit_life(player_0)
        assert bool_1 is False
        bool_2 = game_rules_0.visit_status(player_0, game_data_0)
    except BaseException:
        pass


def test_case_20():
    try:
        game_data_0 = None
        die_brave_0 = module_0.DieBrave(game_data_0)
        assert die_brave_0.value == ''
        var_0 = die_brave_0.execute()
        assert var_0 is None
        die_0 = module_0.Die(game_data_0)
        assert die_0.value == ''
        player_0 = module_1.Player()
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
        assert module_1.Player.S_DEAD == 'dead'
        assert module_1.Player.S_ALIVE == 'alive'
        assert module_1.Player.S_GHOST == 'ghost'
        var_1 = die_0.execute()
    except BaseException:
        pass

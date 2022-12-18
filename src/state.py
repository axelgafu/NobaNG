import sys
from typing import Sequence
import pygame

# from ui import UI
from player import Player
from game_rules import GameRules, GameData


#
# Class: State
# ==============================================================================
class State:
    """Game engine is based on state machine theory. Generic state."""

    def __init__(self):
        self.state_id = "ST_GENERAL"
        self._states_pool = {}
        self._transition_cooldown = 200
        self._transition_time = 0
        self._transitions_enabled = False

    def get_state(self, state_class_name) -> "State":
        """Returns a `State`:class: object with current game state ready to
        execute next action.
        """
        if state_class_name not in self._states_pool.keys():
            current_module = sys.modules[__name__]
            klass = getattr(current_module, state_class_name)
            self._states_pool[state_class_name] = klass()

        return self._states_pool[state_class_name]

    def traverseState(self, game_data: GameData):
        """Performs current state actions, update players stats and
        transitions to next state.
        """
        if game_data.keys is not None and self._transitions_enabled:
            self.set_transitionable(False)
            self.update(game_data)
            transition = self.transitionate(game_data)
            if transition == None:  # Implicitly return same state.
                # print(f"{self.__class__.__name__} -> {self.__class__.__name__}")
                return self
            else:
                # print(f"{self.__class__.__name__}:{self} -> {transition.__class__.__name__}:{transition}")
                return transition

        # print(f"(Default) {self.__class__.__name__} -> {self.__class__.__name__}")
        return self

    def transitionate(self, game_data: GameData):
        """Abstraction function to be rewritten by sub-classes to provide
        desired behavior depending on game state.
        """
        pass

    def update(self, game_data: GameData):
        """Abstraction function to be rewritten by sub-classes to provide
        desired behavior depending on game state.
        """
        pass

    def set_transitionable(self, enabled: bool):
        """Use this function to control the speed of the game states transitions.
        When transitionable is set to false, the game's screens transitions will
        stop until transitionable is set to true.
        """
        self._transitions_enabled = enabled


#
# Class: Quit
# ==============================================================================
class Quit(State):
    """This state is reached from Lobby state when the player wants to end the
    game.
    """

    def __init__(self):
        super().__init__()
        self.state_id = "ST_QUIT"
        self._updated = False

    def update(self, game_data):
        """Gracefully closes connections stablished during the game and releases
        claimed resources before closing the game.
        """
        if not self._updated:
            self._updated = True


#
# Class: Lobby
# ==============================================================================
class Lobby(State):
    """Reached at the very begining of the game start and it is used to register
    players in the game.
    """

    def __init__(self):
        super().__init__()
        self.state_id = "ST_LOBBY"

    def update(self, game_data: GameData):
        """Lobby just waits for the players to be registered.
        Future implementations will add options to create new play rooms and
        options to allow users to register in those game rooms.
        .. todo:: Implement cooperative mode.
        """
        pass

    def transitionate(self, game_data):
        """Lobby transitions are the following:
            =============== ==============
               Transition     New State
            =============== ==============
               K_ESCAPE      :class:`Quit`
              Players < 1    :class:`Display`
               K_RIGHT       :class:`GameStart`
            =============== ==============

        :param game_data:
            Holds the game state data.

        .. note::
            Players should be added manually.
        """
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state("Quit")

        if game_data.players_count() < 1:
            message, handler = self.handle_answer_add_user(game_data)
            return self.get_state("Display").message(message).using(handler)

        elif game_data.keys[pygame.K_RIGHT]:
            return self.get_state("GameStart")

    def handle_answer_add_user(self, game_data: GameData):
        """High-order function, returns a message that should be shown to the
        player and the function that should be used to handle player's response
        to the displayed question.
        usage example:

        .. code-block:: python
            :emphasize-lines: 1,3,4

            message, handler = self.handle_answer_add_user(game_data)
            return (self.get_state('Display')
                .message(self,message)
                .using(handler))

        """
        message = (
            f"Press Enter to add a default user: Player{game_data.players_count()+1}"
        )

        def handle(display_state: Display, game_data: GameData) -> State:
            """Use this function to register a new player in the local machine by
            using enter key and assigning a default player name.
            """
            if game_data.keys[pygame.K_RETURN]:
                player = Player()
                player.name = f"Player{game_data.players_count()+1}"
                game_data.append_player(player)

            return self

        return message, handle


#
# Class: GameStart
# ==============================================================================
class GameStart(State):
    """This state is reached after players are registered and the players group
    is ready to start the game. During this state, roles and characters are
    randomly assigned.
    """

    def __init__(self):
        super().__init__()
        self.state_id = "ST_GAME_START"
        self._updated = False
        self._game_rules = GameRules()

    def update(self, game_data: GameData):
        """Uses the game data infrastructure to assign characters and roles to
        players.
        """

        if not self._updated:
            for playr in game_data.player_list():
                self._game_rules.visit_assign_character(playr)
                self._game_rules.visit_initialize_player(playr)
            self._updated = True

    def transitionate(self, game_data):
        """Moves the game to a different state depending on the state transitions.

        :param game_data:
            Holds the game state data.

        GameStart transitions are the following:
            =============== ==============
               Transition     New State
            =============== ==============
               K_RETURN      :class:`PlayGame`
               K_ESCAPE      :class:`Lobby`
            =============== ==============

        """
        self._updated = False
        if game_data.keys[pygame.K_RETURN]:
            return self.get_state("PlayGame")

        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state("Lobby")
        self._updated = True


#
# Class: PlayGame
# ==============================================================================
class PlayGame(State):
    """This state is reached after roles and characters have been assigned. During
    this state, players throw the dice until their turns end and current player
    gets ready to execute actions.
    """

    _STATE_GEN = 0
    STATE_THROWING_DICE = _STATE_GEN + 1
    STATE_PLAYER_DECIDING = _STATE_GEN + 2
    STATE_ENDING_TURN = _STATE_GEN + 3

    def __init__(self):
        super().__init__()
        self.state_id = "ST_TURN"
        self.re_rol = 3
        self._game_rules = GameRules()
        self.sub_state = self.STATE_THROWING_DICE

    def update(self, game_data: GameData):
        """Applies dice rules as required after each dice throw."""
        # Wait for player choices from UI
        self.apply_rules(self._game_rules, game_data)

    def set_player_choices(self):
        pass

    def transitionate(self, game_data: GameData):
        """Moves the game to a different state depending on the state transitions.

        :param game_data:
            Holds the game state data (:class:`GameData`).

        PlayGame transitions are the following:
            ========================== ==============
               Transition                 New State
            ========================== ==============
               Player is dead           :class:`GameOver`
               K_ESCAPE                 :class:`GameStart`
               Dice re-roll ends        :class:`PerformActivity`
               Dice re-roll available   :class:`Display`
            ========================== ==============

        .. note::
            Display class will ask the player to choose between end turn or
            throw the dice again.

        """
        if game_data.current_player().status == Player.S_DEAD:
            return self.get_state("GameOver")

        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state("GameStart")

        if self.sub_state == PlayGame.STATE_THROWING_DICE:
            if self.re_rol <= 0:
                self.sub_state = PlayGame.STATE_PLAYER_DECIDING
                print("State -> PlayGame.STATE_PLAYER_DECIDING")
                return self  # Continue in this state.
            else:
                message, handler = self.handle_answer_rerol()
                return (
                    self.get_state("Display")
                    # type: ignore # mypy, polymorphic function (see state.Display).
                    .next_state(self)
                    .message(message)
                    .using(handler)
                )

        elif self.sub_state == PlayGame.STATE_PLAYER_DECIDING:
            # User is deciding actions, see User Interface code.
            return self

        elif self.sub_state == PlayGame.STATE_ENDING_TURN:
            # End of current player's turn
            self.re_rol = 3
            self._game_rules.visit_finish_turn(game_data)
            self.sub_state = PlayGame.STATE_THROWING_DICE
            print("State -> PlayGame.STATE_THROWING_DICE")
            return self.get_state("PerformActivity")

    def handle_answer_rerol(self):
        """High-order function, returns a message that should be shown to the
        player and the function that should be used to handle player's response
        to the displayed question.
        usage example:

        .. code-block:: python
            :emphasize-lines: 1,4,5

            message, handler = self.handle_answer_rerol()
            return (self.get_state('Display')
                .next_state(self)
                .message(message)
                .using(handler))

        """
        message = "Press up arrow to finish turn"

        def handle(display_state: Display, game_data: GameData) -> State:
            """Display class will ask the player to choose between end turn or
            throw the dice again.

            Potential transitions are the following:
            ========================== ==============
               Transition                 New State
            ========================== ==============
               K_UP & player is alive   :class:`PerformActivity`
               K_UP & player is dead    :class:`GameStart`
               K_RETURN                 :class:`Display`
            ========================== ==============

            .. note::
                Transition when K_RETURN is pressed is actually to the same
                Display instance itself.

            """
            if game_data.keys[pygame.K_UP]:
                self.re_rol = 3
                self._game_rules.visit_finish_turn(game_data)
                if game_data.current_player().status == Player.S_ALIVE:
                    # return self.get_state("PerformActivity")
                    self.sub_state = PlayGame.STATE_PLAYER_DECIDING
                    return self
                else:
                    return self.get_state("GameOver")

            elif game_data.keys[pygame.K_RETURN]:
                return self

            # return display_state
            return self.get_state("PlayGame")

        return message, handle

    def apply_rules(self, game_rules: GameRules, game_data: GameData):
        """This method uses the infrastructure of :class:`GameRules` class to
        apply the game rules to the players in the game.
        """

        if self.re_rol <= 0:
            return  # No more re-roles.

        player = game_data.current_player()
        if player.status == Player.S_ALIVE:
            end_player_turn = False

            dice = game_rules.visit_throw_dice(game_data, brave=False)
            # TODO add here logic to assign dice

            # TODO
            # end_player_turn = (
            #     game_rules.visit_life(player)
            #     or game_rules.visit_shoot(game_data)
            #     or game_rules.visit_bombs(game_data)
            #     or game_rules.visit_arrows(game_data)
            #     or
            #     # game_rules.visit_status(player, game_data) or
            #     game_rules.visit_character_stats_rules(player)
            # )

            # end_player_turn = game_rules.visit_status(player, game_data) or end_player_turn
            if end_player_turn:
                self.re_rol = 0
            else:
                self.re_rol -= 1


#
# Class: PerformActivity
# ==============================================================================
class PerformActivity(State):
    """This state is reached when player has thrown the dice and has made the
    decision about what actions should be performed. It is important to remark
    that there are actions available for other players that have been given by
    the specific role or character each player is assigned to. So, players may
    decide to activate those actions and this is the state where that occur.
    """

    def __init__(self):
        super().__init__()
        self.state_id = "ST_ACTIVITY"
        self._transitions_enabled = True
        self._game_rules = GameRules()

    def update(self, game_data: GameData):
        """This method will enable character specific and role specific actions
        and will execute the actions that any given player has decided to use.
        Only the first player that claims the action will be allowed.
        """
        self._game_rules.visit_character_counter_rules(game_data)
        self._game_rules.visit_apply_dice_actions(game_data)
        pass

    def transitionate(self, game_data):
        """Moves the game to a different state depending on the state transitions.

        :param game_data:
            Holds the game state data (:class:`GameData`).

        PerformActivity transitions are the following:
            ========================== ==============
               Transition                 New State
            ========================== ==============
               Always                  :class:`PlayGame`
            ========================== ==============

        Note that transition to PlayGame state is automatic.
        """
        #
        # Automatic return on activity complete.
        #
        return self.get_state("PlayGame")


#
# Class: GameOver
# ==============================================================================
class GameOver(State):
    """This state is reached when player has died in the game."""

    def __init__(self):
        super().__init__()
        self.state_id = "ST_GAME_OVER"
        self._updated = False

    def update(self, game_data):
        """There are no updates for game data from this state."""
        pass

    def transitionate(self, game_data):
        """Moves the game to a different state depending on the state transitions.

        :param game_data:
            Holds the game state data (:class:`GameData`).

        PerformActivity transitions are the following:
            ========================== ==============
               Transition                 New State
            ========================== ==============
               K_ESCAPE                  :class:`Lobby`
            ========================== ==============

        Players going back to the Looby state from GameOver state should wait
        for the next game round.
        """
        if game_data.keys[pygame.K_ESCAPE]:
            return self.get_state("Lobby")


#
# Class: Display
# ==============================================================================
class Display(State):
    """This state is reached from any state that requests showing a message.

    .. image:: image/diagram/display-state_sequence/display-state_sequence.png

    usage example:

    .. code-block:: python
        :emphasize-lines: 1,3,4

        message, handler = self.handle_answer_rerol()
        return (self.get_state('Display')
            .message(message)
            .using(handler))

    """

    def __init__(self):
        super().__init__()
        self._activity_performed = False
        self._message = ""
        self._next_state = None
        self._display_time = 0
        self._display_duration = 2000

    def update(self, game_data):
        """Does nothing still"""
        pass

    def message(self, message: str) -> "State":
        """Sets the message that should be shown to the player.
        :return: this state. Use it to chain setup calls.
        :rtype: State
        """
        self._message = message
        return self

    def next_state(self, next_state: State) -> "State":
        self._next_state = next_state
        return self

    def get_message(self) -> str:
        """
        :return: message to be displayed
        :rtype: str
        """
        return self._message

    def using(self, function) -> State:
        """Use this method to define the **callback** function to be used
        during this display execution.

        :return: this state. Use it to chain setup calls.
        :rtype: State
        """
        self._handler = function
        return self

    def transitionate(self, game_data: GameData):
        """Uses the **callback** function defined in the `uses` function to
        perform the transitionate step.

        :param game_data: Game information.
        :type game_date: GameData
        """
        if self._handler is not None:
            next_state = self._handler(self, game_data)
            if next_state is not self:
                # Clean-up current state handler to avoid
                # unwanted side effects.
                self._handler = None

            return next_state

        return self

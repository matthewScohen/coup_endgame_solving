import itertools
from card_enum import CARD


class CoupMatchupEnvironment:
    def __init__(self, player1_cards, player2_cards):
        """
        :param player1_cards: The cards player1 starts the game with
        :param player2_cards: The cards player2 starts the game with
        """
        self.player1_cards = player1_cards
        self.player2_cards = player2_cards

        self.transitions = None
        self.states = None
        self._player_1_winning_region = None
        self._player_2_winning_region = None

    def _get_states(self):
        """
        Game states are of the form (player1_state, player2_state, turn, counter_state) player1_state and player2_state
        are player_states (see _get_player_states). turn = {1,2} and indicates which player takes an action from the
        state. counter_state is a boolean value that indicates if the player takes an action or counter action

        :return: A list of all possible states
        """
        player1_states = self._get_player_states(self.player1_cards)
        player2_states = self._get_player_states(self.player2_cards)
        possible_turn_values = (1, 2)
        possible_counter_state_values = (0, 1)

        possible_states = itertools.product(player1_states, player2_states, possible_turn_values,
                                            possible_counter_state_values)
        # remove states where both players have 2 dead cards
        possible_states = [state for state in possible_states if
                           state[0][0] != "dead" or state[0][1] != "dead" or state[1][0] != "dead"
                           or state[0][1] != "dead"]
        # TODO can we remove states where 1 player is dead and the other has more than 9(?) coins?
        return list(possible_states)

    @staticmethod
    def _get_player_states(self, player_cards):
        """
        player_states are of the form (card, card, coin_count) where card is either the value of the
        alive card or "dead" and coin_count is the number of coins the player has.

        :param player_cards: A tuple of the player's cards
        :return: A list of all possible player states
        """
        card0_states = (player_cards[0], "dead")
        card1_states = (player_cards[1], "dead")
        # players can have at most 12 coins since they must coup if they have 10+ and can take at most 3 at a time
        coin_states = [n for n in range(13)]
        player_states = itertools.product(card0_states, card1_states, coin_states)
        return list(player_states)

    def get_start_game_state(self):
        """
        :return: The state that represents the start of a new game (both players have their cards alive and 2 coins)
        """
        player1_state = (self.player1_cards[0], self.player1_cards[1], 2)
        player2_state = (self.player2_cards[0], self.player2_cards[1], 2)
        start_game_state = (player1_state, player2_state, 1, 0)
        return start_game_state

    def _get_actions(self, state, player):
        """
        Returns a list of all actions 'player' can take from 'state'. Actions will be different if the state is a
        counter-action state or regular state and also depend on the player since players can have different cards

        :param state: The state from which player is taking actions
        :param player: An integer representing the player whose actions should be returned
        :return: A list of all possible actions for player
        """
        pass

    def _get_transition(self):
        """
        :return: A transition dictionary where the value of trans[state][action] is the resulting state for taking
        'action' from 'state'.
        """
        return None

    def _solve_winning_region(self, player):
        """
        Calculates and returns the winning region of player using the two player attractor algorithm

        :param player: An integer representing the player who's winning region should be returned
        :return: A list of states that are winning for player
        """
        return list()

    def solve(self):
        self.states = self._get_states()
        self.transitions = self._get_transition()

        self._player_1_winning_region = self._solve_winning_region(player=1)
        self._player_2_winning_region = self._solve_winning_region(player=2)

    def get_win_region(self, player):
        """
        :param player: An integer representing the player who's winning region should be returned
        :return: The stored list of winning states for player
        """
        if player == 1:
            assert self._player_1_winning_region is not None, f"Player 1 winning region not defined for {self}"
            return self._player_1_winning_region
        elif player == 2:
            assert self._player_2_winning_region is not None, f"Player 2 winning region not defined for {self}"
            return self._player_2_winning_region
        else:
            raise Exception(f"Player {player} not defined in {self}")

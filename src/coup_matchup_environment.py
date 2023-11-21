import itertools
import constants


class CoupMatchupEnvironment:
    def __init__(self, player1_cards, player2_cards):
        """
        :param player1_cards: The cards player1 starts the game with
        :param player2_cards: The cards player2 starts the game with
        """
        self.player1_cards = player1_cards
        self.player2_cards = player2_cards

        # self.transitions[state][action] = new_state
        self.transitions = None
        self.states = None
        self.actions = None
        self._player_1_winning_region = None
        self._player_2_winning_region = None

    def _get_states(self):
        """
        Game states are of the form (player1_state, player2_state, turn, counter_state) player1_state and player2_state
        are player_states (see _get_player_states). turn = {1,2} and indicates which player takes an action from the
        state. counter_state is a boolean value that indicates if the player takes an action or counter action

        :return: A list of all possible states
        """
        # TODO we need to change state to account for the fact that what happens when you take a counter action depends
        # TODO on the previous action. We don't want to make the game reliant on previous states so we should probably
        # TODO encode the ability to take a counter action in the state. SO instead of (player1_state, player2_state, turn, counter_state)
        # TODO it should be something like (player1_state, player2_state, turn, assassinate_counter_state, foregin_aid_couter_state, steal_counter_state)
        # TODO so the action that can be countered is indicated in the state
        # TODO alternatly we could just encode this in the action, eg if you assassinate just have the transition function
        # TODO check if the other player has a contessa. This is probably equivalent but I think its better to do the counter
        # TODO state option since that will more closely model the game even if they are equal techincally.
        # TODO JUST PUTTING THIS HERE SO I DON'T FORGET
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
        return list(possible_states)

    @staticmethod
    def _get_player_states(player_cards):
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

    def _get_actions(self):
        """
        :return: A tuple of all possible actions (including counter-actions)
        """
        actions = list(constants.actions)
        actions.extend(constants.counter_actions)
        return tuple(actions)

    def _get_enabled_actions(self, state):
        """
        Returns a list of all actions/counter-actions that can be taken from 'state'.

        :param state: The state from which player is taking actions
        :return: A list of all possible actions that can be taken from 'state'
        """
        player = state[0] if state[2] == 1 else state[1]
        player_coins = player[2]
        enabled_acts = list()

        # state is action state
        if state[3] == 0:
            enabled_acts.append(constants.INCOME)
            enabled_acts.append(constants.FOREIGN_AID)
            if player_coins >= 7:
                enabled_acts.append(constants.COUP)
            if constants.DUKE in player:
                enabled_acts.append(constants.TAX)
            if constants.ASSASSIN in player and player_coins >= 3:
                enabled_acts.append(constants.ASSASSINATE)
            if constants.CAPTAIN in player:
                enabled_acts.append(constants.STEAL)
        # state is counter-action state
        elif state[3] == 1:
            if constants.DUKE in player:
                enabled_acts.append(constants.BLOCK_FOREIGN_AID)
            if constants.CAPTAIN in player or constants.AMBASSADOR in player:
                enabled_acts.append(constants.BLOCK_STEAL)
            if constants.CONTESSA in player:
                enabled_acts.append(constants.BLOCK_ASSASSINATE)
        else:
            raise NotImplementedError(f"Error value of {state[3]} not allowed for counter-action indicator")

        return enabled_acts

    def _get_transitions(self):
        """
        :return: A transition dictionary where transitions[state][action] = new_state
        """
        transitions = dict(
            zip(self.states, [dict(zip(self.actions, [None for _ in self.actions])) for _ in self.states]))
        for state in transitions:
            for action in state:
                if action in self._get_enabled_actions(state):
                    transitions[state][action] = self._transition(state, action)
                else:
                    transitions[state][action] = constants.ACTION_DISABLED
        return transitions

    @staticmethod
    def _transition(state, action):
        """
        :param state: An initial state the action is being taken from
        :param action: The action being taken from state
        :return: The resulting state from taking action from the input state
        """
        # TODO implement game transition logic here
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
        self.actions = self._get_actions()
        self.transitions = self._get_transitions()

        self._player_1_winning_region = self._solve_winning_region(player=1)
        self._player_2_winning_region = self._solve_winning_region(player=2)

    def get_win_region(self, player):
        """
        :param player: An integer representing the player who's winning region should be returned
        :return: The stored list of winning states for player
        """
        if player == 1:
            assert self._player_1_winning_region is not None, f"Player {player} winning region not defined for {self} "\
                                                              f"call {self}.solve()"
            return self._player_1_winning_region
        elif player == 2:
            assert self._player_2_winning_region is not None, f"Player {player} winning region not defined for {self} "\
                                                              f"call {self}.solve()"
            return self._player_2_winning_region
        else:
            raise Exception(f"Player {player} not defined in {self}")
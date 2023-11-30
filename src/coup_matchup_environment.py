import copy
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
        self._states = None
        self._goal_states_1 = None
        self._goal_states_2 = None
        self.actions = None
        self._player_1_winning_region = None
        self._player_2_winning_region = None
        self._policy_1 = None
        self._policy_2 = None

    def _get_states(self):
        """
        Game states are of the form
        (player1_state, player2_state, turn, assassinate_counter_state, foregin_aid_couter_state, steal_counter_state, coup_counter_state)
        player1_state and player2_state are player_states (see _get_player_states). turn = {1,2} and indicates which
        player takes an action from the state. The counter_state fields are boolean values that indicate which (if any)
        counter action can be taken from that state. The coup counter state indicates it is a state following the other
        player's coup action (from this state the only actions are to choose which card to kill)

        :return: A list of all possible states
        """
        if self._states is None:
            player1_states = self._get_player_states(self.player1_cards)
            player2_states = self._get_player_states(self.player2_cards)
            possible_turn_values = (1, 2)
            possible_assassinate_counter_state_values = (0, 1)
            possible_foreign_aid_counter_state_values = (0, 1)
            possible_steal_counter_state_values = (0, 1)
            possible_coup_counter_state_values = (0, 1)

            possible_states = itertools.product(player1_states, player2_states, possible_turn_values,
                                                possible_assassinate_counter_state_values,
                                                possible_foreign_aid_counter_state_values,
                                                possible_steal_counter_state_values, possible_coup_counter_state_values)
            # remove states where both players have 2 dead cards
            possible_states = [state for state in possible_states if
                               state[0][0] != "dead" or state[0][1] != "dead" or state[1][0] != "dead"
                               or state[1][1] != "dead"]
            self._states = list(possible_states)
        return self._states

    def _get_actions(self):
        """
        :return: A tuple of all possible actions (including counter-actions)
        """
        if self.actions is None:
            actions = list(constants.actions)
            actions.extend(constants.counter_actions)
            return tuple(actions)
        else:
            return self.actions

    def _get_transitions(self):
        """
        :return: A transition dictionary where transitions[state][action] = new_state
        """
        transitions = dict(
            zip(self._states, [dict(zip(self.actions, [None for _ in self.actions])) for _ in self._states]))
        for state in transitions:
            for action in transitions[state]:
                if action in self.get_enabled_actions(state):
                    transitions[state][action] = self.transition(state, action)
                else:
                    transitions[state][action] = constants.ACTION_DISABLED
        return transitions

    def _solve_winning_region(self, player, verbose=False):
        """
        Calculates and returns the winning region of player using the two player attractor algorithm
        :param player: An integer representing the player who's winning region should be returned
        :return: A list of states that are winning for player
        """

        policy = dict(zip(self._states, [None for _ in self._states]))
        attractor_sets = list()
        # initial winning set = player final states
        previous_attractor = self.get_goal_states(player)
        new_attractor = set()
        # keep track of each attractor level in attractor_sets to construct the winning policy later
        attractor_sets.append(previous_attractor)

        i = 1
        while True:
            if verbose:
                print(f"Computing attractor level {i} for player {player}")
            new_attractor = copy.deepcopy(previous_attractor)
            for state in self._states:
                if state not in previous_attractor:
                    turn = state[2]
                    if turn == player:
                        # if state is player's state add to attractor if ANY action leads to a winning state
                        for action in self.transitions[state]:
                            if self.transitions[state][action] in previous_attractor:
                                new_attractor.add(state)
                                policy[state] = action
                    else:
                        # if it is the other players turn add the state if ALL actions lead to a winning state
                        all_actions_safe = True
                        for action in self.transitions[state]:
                            if self.transitions[state][action] != constants.ACTION_DISABLED \
                                    and self.transitions[state][action] not in previous_attractor:
                                all_actions_safe = False
                        if all_actions_safe:
                            new_attractor.add(state)
            attractor_sets.append(new_attractor)
            i += 1
            if new_attractor == previous_attractor:
                break
            else:
                previous_attractor = copy.deepcopy(new_attractor)

        # TODO calculate policy here based on attractor_sets
        # policy[state] = actions that result in state at lower attractor_set level
        return previous_attractor, policy

    def get_start_game_state(self):
        """
        :return: The state that represents the start of a new game (both players have their cards alive and 2 coins)
        """
        player1_state = (self.player1_cards[0], self.player1_cards[1], 2)
        player2_state = (self.player2_cards[0], self.player2_cards[1], 2)
        start_game_state = (player1_state, player2_state, 1, 0, 0, 0, 0)
        return start_game_state

    def get_goal_states(self, player):
        """
        :param player: The player whose goal states are returned
        :return: A set of goal states for player (states where both of the other player's cards are dead)
        """
        if player == 1 and self._goal_states_1 is not None:
            return self._goal_states_1
        if player == 2 and self._goal_states_2 is not None:
            return self._goal_states_2
        else:
            goal_states = set()
            for state in self._states:
                opponent_state = state[1] if player == 1 else state[0]
                if opponent_state[0] == constants.DEAD and opponent_state[1] == constants.DEAD:
                    goal_states.add(state)
            if player == 1:
                self._goal_states_1 = goal_states
            elif player == 2:
                self._goal_states_2 = goal_states
            else:
                raise IndexError
            return goal_states

    def solve(self, verbose=False):
        self._states = self._get_states()
        self.actions = self._get_actions()
        self.transitions = self._get_transitions()

        self._player_1_winning_region, self._policy_1 = self._solve_winning_region(player=1, verbose=verbose)
        self._player_2_winning_region, self._policy_2 = self._solve_winning_region(player=2, verbose=verbose)

    def get_win_region(self, player):
        """
        :param player: An integer representing the player whose winning region should be returned
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

    def get_policy(self, player):
        """
        :param player: An integer representing the player whose policy should be returned
        :return: A policy dict for player of the form policy[state] = action
        """
        policy = self._policy_1 if player == 1 else self._policy_2
        return policy

    @staticmethod
    def transition(state, action):
        """
        :param state: An initial state the action is being taken from
        :param action: The action being taken from state
        :return: The resulting state from taking action from the input state
        """
        # unpack state
        player1_state, player2_state, turn, assassinate_counter_state, foreign_aid_counter_state, \
        steal_counter_state, coup_counter_state = state

        new_player1_state = player1_state
        new_player2_state = player2_state
        new_turn = turn
        new_assassinate_counter_state = assassinate_counter_state
        new_foreign_aid_counter_state = foreign_aid_counter_state
        new_steal_counter_state = steal_counter_state
        new_coup_counter_state = coup_counter_state

        # state is action state
        if assassinate_counter_state == 0 and foreign_aid_counter_state == 0 and steal_counter_state == 0 and coup_counter_state == 0:
            new_turn = 1 if turn == 2 else 2
            if action == constants.INCOME:
                if turn == 1:
                    new_player1_state = (player1_state[0], player1_state[1], player1_state[2] + 1)
                elif turn == 2:
                    new_player2_state = (player2_state[0], player2_state[1], player2_state[2] + 1)
            elif action == constants.FOREIGN_AID:
                new_foreign_aid_counter_state = 1
            elif action == constants.COUP:
                new_coup_counter_state = 1
                if turn == 1:
                    new_player1_state = (player1_state[0], player1_state[1], player1_state[2] - 7)
                elif turn == 2:
                    new_player2_state = (player2_state[0], player2_state[1], player2_state[2] - 7)
            elif action == constants.TAX:
                if turn == 1:
                    new_player1_state = (player1_state[0], player1_state[1], player1_state[2] + 3)
                elif turn == 2:
                    new_player2_state = (player2_state[0], player2_state[1], player2_state[2] + 3)
            elif action == constants.ASSASSINATE:
                new_assassinate_counter_state = 1
            elif action == constants.STEAL:
                new_steal_counter_state = 1

        # state is a counter_state
        elif assassinate_counter_state == 1:
            new_assassinate_counter_state = 0
            if action == constants.BLOCK_ASSASSINATE:
                # nothing changes if you block the assassination
                pass
            elif action == constants.KILL_CARD_1:
                if turn == 1:
                    new_player1_state = (constants.DEAD, player1_state[1], player1_state[2])
                elif turn == 2:
                    new_player2_state = (constants.DEAD, player2_state[1], player2_state[2])
            elif action == constants.KILL_CARD_2:
                if turn == 1:
                    new_player1_state = (player1_state[0], constants.DEAD, player1_state[2])
                elif turn == 2:
                    new_player2_state = (player2_state[0], constants.DEAD, player2_state[2])
        elif new_foreign_aid_counter_state == 1:
            new_foreign_aid_counter_state = 0
            if action == constants.BLOCK_FOREIGN_AID:
                # if foreign aid is block nothing happens
                pass
            else:
                # the player whose turn it is NOT gets +2 coins since the turn indicates the player who is blocking
                if turn == 1:
                    new_player2_state = (player2_state[0], player2_state[1], player2_state[2] + 2)
                elif turn == 2:
                    new_player1_state = (player1_state[0], player1_state[1], player1_state[2] + 2)
        elif steal_counter_state == 1:
            new_steal_counter_state = 0
            if action == constants.BLOCK_STEAL:
                pass
            else:
                if turn == 1:
                    # you can only steal 1 or 0 coins if the player has fewer than 2 coins
                    coins_stolen = 2 if player1_state[2] >= 2 else player1_state[2]
                    new_player1_state = (player1_state[0], player1_state[1], player1_state[2] - coins_stolen)
                    new_player2_state = (player2_state[0], player2_state[1], player2_state[2] + coins_stolen)
                elif turn == 2:
                    coins_stolen = 2 if player2_state[2] >= 2 else player2_state[2]
                    new_player1_state = (player1_state[0], player1_state[1], player1_state[2] + coins_stolen)
                    new_player2_state = (player2_state[0], player2_state[1], player2_state[2] - coins_stolen)
        elif coup_counter_state == 1:
            new_coup_counter_state = 0
            if action == constants.KILL_CARD_1:
                if turn == 1:
                    new_player1_state = (constants.DEAD, player1_state[1], player1_state[2])
                elif turn == 2:
                    new_player2_state = (constants.DEAD, player2_state[1], player2_state[2])
            elif action == constants.KILL_CARD_2:
                if turn == 1:
                    new_player1_state = (player1_state[0], constants.DEAD, player1_state[2])
                elif turn == 2:
                    new_player2_state = (player2_state[0], constants.DEAD, player2_state[2])

        new_state = (new_player1_state, new_player2_state, new_turn, new_assassinate_counter_state,
                     new_foreign_aid_counter_state, new_steal_counter_state, new_coup_counter_state)
        return new_state

    @staticmethod
    def get_enabled_actions(state):
        """
        Returns a list of all actions/counter-actions that can be taken from 'state'.

        :param state: The state from which player is taking actions
        :return: A list of all possible actions that can be taken from 'state'
        """
        player = state[0] if state[2] == 1 else state[1]
        player_coins = player[2]
        enabled_acts = list()
        # ACTION STATE
        if state[3] == 0 and state[4] == 0 and state[5] == 0 and state[6] == 0:
            if player_coins >= 10:
                enabled_acts.append(constants.COUP)
                return enabled_acts
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
        # COUNTER ACTION STATES
        # counter-assassinate state
        elif state[3] == 1:
            if player[0] != constants.DEAD:
                enabled_acts.append(constants.KILL_CARD_1)
            if player[1] != constants.DEAD:
                enabled_acts.append(constants.KILL_CARD_2)
            if constants.CONTESSA in player:
                enabled_acts.append(constants.BLOCK_ASSASSINATE)
        # counter-foreign-aid state
        elif state[4] == 1 and constants.DUKE in player:
            enabled_acts.append(constants.BLOCK_FOREIGN_AID)
        # counter-steal state
        elif state[5] == 1 and (constants.CAPTAIN in player or constants.AMBASSADOR in player):
            enabled_acts.append(constants.BLOCK_STEAL)
        # counter-coup state
        elif state[6] == 1:
            if player[0] != constants.DEAD:
                enabled_acts.append(constants.KILL_CARD_1)
            if player[1] != constants.DEAD:
                enabled_acts.append(constants.KILL_CARD_2)
        # state is counter-state and you cannot counter the action
        else:
            enabled_acts.append(constants.NO_ACTION)

        return enabled_acts

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
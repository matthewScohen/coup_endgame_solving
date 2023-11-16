class CoupMatchupEnvironment:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self._player_1_winning_region = None
        self._player_2_winning_region = None

    def get_states(self):
        """
        :return: A list of all possible states
        """
        pass

    def get_actions(self, state, player):
        """
        Returns a list of all actions 'player' can take from 'state'. Actions will change if the state is a
        counter-action state or regular state and also depend on the player since players can have different cards

        :param state: The state from which player is taking actions
        :param player: An integer representing the player who's actions should be returned
        :return: A list of all possible actions for player
        """
        pass

    def get_transition(self):
        """
        :return: A transition dictionary where the value of trans[state][action] is the resulting state for taking
        'action' from 'state'.
        """
        pass

    def _solve_winning_region(self, player):
        """
        Calculates and returns the winning region of player
        :param player: An integer representing the player who's winning region should be returned
        :return: A list of states that are winning for player
        """
        return list()

    def solve(self):
        """
        Calculate the winning regions of both players and store them in the winning region class variables
        """
        self._player_1_winning_region = self._solve_winning_region(player=1)
        self._player_2_winning_region = self._solve_winning_region(player=2)

    def get_win_region(self, player):
        """
        Returns the stored list of winning states for player
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

class CoupMatchupEnvironment:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.player_1_winning_region = None
        self.player_2_winning_region = None

    def get_states(self):
        """
        :return: A list of all possible states
        """
        pass

    def get_actions(self):
        """
        :return: A list of all possible actions
        """
        pass

    def get_transition(self):
        """
        :return: A transition dictionary of the form trans[state][action][new_state]
        """
        pass

    def __solve_winning_region(self, player):
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
        self.player_1_winning_region = self.__solve_winning_region(player=1)
        self.player_2_winning_region = self.__solve_winning_region(player=2)

    def get_win_region(self, player):
        """
        Returns the stored list of winning states for player
        :param player: An integer representing the player who's winning region should be returned
        :return: The stored list of winning states for player
        """
        if player == 1:
            assert self.player_1_winning_region is not None, f"Player 1 winning region not defined for {self}"
            return self.player_1_winning_region
        elif player == 2:
            assert self.player_2_winning_region is not None, f"Player 2 winning region not defined for {self}"
            return self.player_2_winning_region
        else:
            raise Exception(f"Player {player} not defined in {self}")

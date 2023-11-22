import constants

from coup_matchup_environment import CoupMatchupEnvironment


def main():
    player1_cards = (constants.CAPTAIN, constants.CONTESSA)
    player2_cards = (constants.DUKE, constants.ASSASSIN)
    matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    # states = matchup._get_states()
    # matchup.solve()
    state = ((constants.CAPTAIN, constants.CONTESSA, 0), (constants.DUKE, constants.ASSASSIN, 12), 1, 1, 0, 0)
    # print(matchup._get_transitions()[state])
    print(matchup._get_enabled_actions(state))
    # print(f"Player {1 if initial_state in matchup.get_win_region(1) else 2} wins")


if __name__ == "__main__":
    main()

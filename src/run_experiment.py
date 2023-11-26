import constants

from coup_matchup_environment import CoupMatchupEnvironment


def main():
    player1_cards = (constants.CAPTAIN, constants.CONTESSA)
    player2_cards = (constants.DUKE, constants.ASSASSIN)
    matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    # states = matchup._get_states()
    matchup.solve()

    initial_state = matchup.get_start_game_state()
    #state = ((constants.CAPTAIN, constants.CONTESSA, 0), (constants.DEAD, constants.ASSASSIN, 8), 2, 0, 0, 0, 1)
    # print(matchup._get_transitions()[state])
    #print(matchup._get_enabled_actions(state))
    #print(matchup._transition(state, constants.KILL_CARD_2))
    #print(f"Player {1 if initial_state in matchup.get_win_region(1) else 2} wins")

    # Check which player's winning region contains the initial state
    if initial_state in matchup.get_win_region(1):
        winner = 1
    elif initial_state in matchup.get_win_region(2):
        winner = 2
    else:
        winner = None

    if winner:
        print(f"Player {winner} wins")
    else:
        print("No winner determined from the initial state, possible error")


if __name__ == "__main__":
    main()

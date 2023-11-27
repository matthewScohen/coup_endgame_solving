import constants

from coup_matchup_environment import CoupMatchupEnvironment


def main():
    player1_cards = (constants.DUKE, constants.ASSASSIN)
    player2_cards = (constants.CAPTAIN, constants.CONTESSA)
    matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    matchup.solve()
    initial_state = matchup.get_start_game_state()

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

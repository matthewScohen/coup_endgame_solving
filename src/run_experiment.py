from coup_matchup_environment import CoupMatchupEnvironment
def main():
    player1_cards = ("captain", "contessa")
    player2_cards = ("duke", "assassin")
    matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    print(len(matchup._get_states()))
    # matchup.solve()
    # print(f"Player {1 if initial_state in matchup.get_win_region(1) else 2} wins")

if __name__ == "__main__":
    main()
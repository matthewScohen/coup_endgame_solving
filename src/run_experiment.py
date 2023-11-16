from coup_matchup_environment import CoupMatchupEnvironment
from card_enum import CARD

def main():
    player1_cards = (CARD.CAPTAIN.value, CARD.CONTESSA.value)
    player2_cards = (CARD.DUKE.value, CARD.ASSASSIN.value)
    matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    print(matchup._get_states())
    # matchup.solve()
    # print(f"Player {1 if initial_state in matchup.get_win_region(1) else 2} wins")

if __name__ == "__main__":
    main()
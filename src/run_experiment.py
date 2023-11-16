from coup_matchup_environment import CoupMatchupEnvironment
def main():
    initial_state = ("state", "values", "here")
    matchup = CoupMatchupEnvironment(initial_state)
    matchup.solve()
    print(f"Player {1 if initial_state in matchup.get_win_region(1) else 2} wins")

if __name__ == "__main__":
    main()
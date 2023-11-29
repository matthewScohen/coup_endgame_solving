import itertools
import random
import csv

import constants
from coup_matchup_environment import CoupMatchupEnvironment


def run_matchup(player1_cards, player2_cards, verbose=False):
    matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    matchup.solve(verbose=verbose)
    initial_state = matchup.get_start_game_state()

    winner = None
    if initial_state in matchup.get_win_region(1):
        winner = 1
    elif initial_state in matchup.get_win_region(2):
        winner = 2

    assert winner is not None, f"Error with {matchup}, no winner found."
    return winner, matchup.get_policy(1), matchup.get_policy(2), matchup


def get_game_run(matchup: CoupMatchupEnvironment, policy_1: dict, policy_2: dict):
    """
    :param policy_1:
    :param policy_2:
    :param matchup:
    :return:
    """
    run = list()
    state = matchup.get_start_game_state()
    run.append(state)

    while state not in matchup.get_goal_states(1) and state not in matchup.get_goal_states(2):
        turn = state[2]
        action = policy_1[state] if turn == 1 else policy_2[state]
        # if action is None that means there is no action for player to win so a random action is selected
        if action is None:
            action = random.choice(CoupMatchupEnvironment.get_enabled_actions(state))
        new_state = CoupMatchupEnvironment.transition(state, action)
        run.extend([action, new_state])
        print(state, action)
        state = new_state
    return run


def run_experiment(path="results.txt", verbose=False):
    """
    Evaluate all possible matchups and write the results to the file specified by path
    """
    card_pairs = list(itertools.product(constants.CARDS, constants.CARDS))
    matchups = list(itertools.product(card_pairs, card_pairs))

    i = 0
    with open(path, "w") as file:
        for matchup in matchups:
            print(f"Solving matchup {i+1}/{len(matchups)}")
            winner, _, _, _ = run_matchup(matchup[0], matchup[1], verbose=verbose)
            file.write(f"{matchup[0]},{matchup[1]},{winner}\n")


def main():
    run_experiment(verbose=True)


if __name__ == "__main__":
    main()

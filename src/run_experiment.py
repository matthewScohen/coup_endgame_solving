import constants
import random
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


def run_experiment():
    """
    Run and record the result of all matchups
    """
    pass


def main():
    player1_cards = (constants.AMBASSADOR, constants.AMBASSADOR)
    player2_cards = (constants.ASSASSIN, constants.CONTESSA)
    # print(CoupMatchupEnvironment.get_enabled_actions((('ambassador', 'ambassador', 6), ('assassin', 'contessa', 4), 2, 0, 0, 0, 0)))

    # matchup = CoupMatchupEnvironment(player1_cards, player2_cards)
    # state = (('assassin', 'contessa', 8), ('ambassador', 'ambassador', 10), 1, 0, 0, 0, 0)
    # print(CoupMatchupEnvironment.get_enabled_actions(state))
    # print(CoupMatchupEnvironment.transition(state, constants.ASSASSINATE))
    # new_state = CoupMatchupEnvironment.transition(state, constants.ASSASSINATE)
    # print(CoupMatchupEnvironment.get_enabled_actions(new_state))

    # matchup.solve(verbose=True)
    # print(state in matchup.get_win_region(1))
    # print(state in matchup.get_win_region(2))
    # print(matchup.get_policy(1)[state])
    # print(matchup.get_policy(2)[state])
    # print(CoupMatchupEnvironment.get_enabled_actions(state))

    winner, policy_1, policy_2, matchup = run_matchup(player1_cards, player2_cards, verbose=True)
    print(winner)
    print(get_game_run(matchup, policy_1, policy_2))

if __name__ == "__main__":
    main()

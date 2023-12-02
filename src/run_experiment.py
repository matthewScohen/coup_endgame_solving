import itertools
import random
import threading
import concurrent.futures
import os

import constants
from coup_matchup_environment import CoupMatchupEnvironment


def run_matchup(player1_cards, player2_cards, verbose=False):
    matchup_env = CoupMatchupEnvironment(player1_cards, player2_cards)
    matchup_env.solve(verbose=verbose)
    initial_state = matchup_env.get_start_game_state()

    winner = None
    if initial_state in matchup_env.get_win_region(1):
        winner = 1
    elif initial_state in matchup_env.get_win_region(2):
        winner = 2

    assert winner is not None, f"Error with {matchup_env}, no winner found."
    return winner, matchup_env.get_policy(1), matchup_env.get_policy(2), matchup_env


def get_game_run(matchup: CoupMatchupEnvironment, policy_1: dict, policy_2: dict):
    """
    Returns a list in the form (state, action, state, action...) representing a run of game matchup with the
    given policies.
    :param policy_1: Policy for player 1
    :param policy_2: Policy for player 2
    :param matchup: CoupMatchupEnvironment environment of the game
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


def get_run_graph(matchup: CoupMatchupEnvironment, pi1: dict, pi2: dict):
    """
    Returns a graph in the form graph[state] = list(successor_states) that shows a game run where the player who wins
    takes their optimal action and the player who loses has all possible successor states listed
    """
    initial_state = matchup.get_start_game_state()
    graph = dict()
    _get_run_graph(initial_state, graph, matchup, pi1, pi2)
    return graph


def _get_run_graph(initial_state, graph: dict, matchup: CoupMatchupEnvironment, pi1: dict, pi2: dict):
    """
    Utility function -- see get_run_graph
    """
    state = initial_state
    graph[state] = list()
    if state in matchup.get_goal_states(1) or state in matchup.get_goal_states(2):
        return
    else:
        turn = state[2]
        action = pi1[state] if turn == 1 else pi2[state]
        # if action is None that means there is no action for player to win, so we look at all their possible actions
        if action is None:
            for action in CoupMatchupEnvironment.get_enabled_actions(state):
                new_state = CoupMatchupEnvironment.transition(state, action)
                graph[state].append(new_state)
                if new_state not in graph.keys():
                    _get_run_graph(new_state, graph, matchup, pi1, pi2)
        else:
            new_state = CoupMatchupEnvironment.transition(state, action)
            graph[state].append(new_state)
            _get_run_graph(new_state, graph, matchup, pi1, pi2)
    return


def get_next_states(matchup: CoupMatchupEnvironment, state, pi):
    """
    If there is a winning action for the player with strategy pi return the resulting state from taking that action
    otherwise returns a list of all states that can result from any enabled action.
    """
    if pi[state] is not None:
        return [matchup.transition(state, pi[state])]
    else:
        return [matchup.transition(state, action) for action in matchup.get_enabled_actions(state)]


def write_to_file(result, file, lock):
    """
    Write to a file in a thread safe way
    """
    lock.acquire()
    try:
        file.write(f"{result}\n")
    finally:
        lock.release()


def run_experiment(path="../data/results.txt", verbose=False, num_cores=1, overwrite=False):
    """
    Evaluate all possible matchups and write the results to the file specified by path
    :param path: Path of file to write results to
    :param verbose: Boolean value indicating whether to print matchup debug info
    :param num_cores: Number of cores to use for parallel processing
    :param overwrite: Whether to overwrite the file at path if it already exists
    """
    if os.path.isfile(path) and overwrite is False:
        raise Exception(
            f"File {path} already exists, if you wish to overwrite it call this function with overwrite=True")
    if num_cores < 1:
        raise Exception(f"Error, value of {num_cores} for num_cores not allowed")
    # Compute combinations of cards since (DUKE,CAPTAIN) is the same as (CAPTAIN,DUKE)
    card_pairs = list(itertools.combinations(constants.CARDS, 2))
    # Add duplicate pairs (CAPTAIN, CAPTAIN), (DUKE,DUKE), etc.
    card_pairs.extend([(card, card) for card in constants.CARDS])
    matchups = list(itertools.product(card_pairs, card_pairs))
    i = 0
    if num_cores == 1:
        with open(path, "w") as file:
            for matchup in matchups:
                winner, _, _, _ = run_matchup(matchup[0], matchup[1], verbose=verbose)
                file.write(f"{matchup[0]},{matchup[1]},{winner}\n")
                print(f"Solved {i + 1}/{len(matchups)} matchups")
                i += 1
    else:
        max_workers = os.cpu_count() if num_cores > os.cpu_count() else num_cores
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            with open(path, 'w') as file:
                lock = threading.Lock()
                future_results = [executor.submit(run_matchup, matchup[0], matchup[1], verbose=verbose)
                                  for matchup in matchups]

                i = 0
                for future in concurrent.futures.as_completed(future_results):
                    winner, _, _, matchup = future.result()
                    result = f"{matchup.player1_cards}, {matchup.player2_cards}, {winner}"
                    write_to_file(result, file, lock)
                    print(f"Solved {i + 1}/{len(matchups)} matchups")
                    i += 1


def main():
    run_experiment(verbose=False, num_cores=1)


if __name__ == "__main__":
    main()

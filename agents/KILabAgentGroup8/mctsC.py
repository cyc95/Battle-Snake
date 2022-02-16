import time
from agents.KILabAgentGroup8.simulator_environment import simulatorEnvironment
from agents.KILabAgentGroup8.uct_nodeC import UCTNode
from environment.Battlesnake.model.Snake import Snake
import copy

def mcts(
        simulation_time: float,
        env: simulatorEnvironment,
        you: Snake
) -> UCTNode:
    start_time = time.time()
    root_node = UCTNode(
        boardState=env.board,
        action=None,
        parent=None,
        you=you
    )
    while time.time() - start_time < simulation_time and not root_node.end:
        selected_node, next_action = root_node.select(env)
        if selected_node is None:
            continue
        leaf_node, winner = selected_node.expand(env, next_action)
        if leaf_node is None:
            continue
        #if winner is None:
         #   winner = leaf_node.simulate(env, (simulation_time-time.time()+start_time))
        leaf_node.backup(winner)
    return root_node

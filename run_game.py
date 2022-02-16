
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from environment.Battlesnake.modes.Modes import GameMode
from environment.battlesnake_environment import BattlesnakeEnvironment
from agents.KILabAgentGroup8.KILabAgentV import KILabAgentV
from agents.KILabAgentGroup8.KILabAgentNewMinMax import KILabAgentNewMinMax
from agents.KILabAgentGroup8.KILabAgentOldMinMax import KILabAgentOldMinMax
from agents.KILabAgentGroup8.KILabAgent import KILabAgent
from agents.KILabAgentGroup8.KILabAgentOldOnServer import KILabAgentOldOnServer
# from agents.KILabAgentGroup8.KILabAgentMCTS import KILabAgentMCTS
from agents.KILabAgentGroup8.SimulatorAgent import SimulatorAgent
from agents.KILabAgentGroup8.Test import Test
from agents.RandomAgent.RandomAgent import RandomAgent
import copy
import time



agents = [KILabAgent(), RandomAgent(),RandomAgent(),RandomAgent()]

# remote_agent = RemoteAgent(url='130.75.31.206:8000')
# agents.append(remote_agent)
if 1:
    env = BattlesnakeEnvironment(
        width=11,
        height=11,
        agents=agents,
        act_timeout=10,
        export_games=False,
        mode=GameMode.STANDARD,
        squad_assignments=[1, 1, 3, 3, 4, 4],
        ruleset_settings=RulesetSettings()
    )

    env.reset()
    env.render()
    snakes = env.board.snakes
    you = copy.deepcopy(snakes[0].snake_id)
    opp = copy.deepcopy(snakes[1].snake_id)
    i = [0, 0]
    while True:

        step_start_time = time.time()
        env.handle_input()

        env.step()
        env.render()
        if env.is_game_over():
            print(len(env.board.snakes))
            if len(env.board.snakes) == 0:
                get_length = env.board.dead_snakes[0].get_length() - env.board.dead_snakes[1].get_length()
                if get_length > 0:
                    if env.board.dead_snakes[0].snake_id == you:
                        i[0] += 1
                    else:
                        i[1] += 1
                if get_length < 0:
                    if env.board.dead_snakes[1].snake_id == you:
                        i[0] += 1
                    else:
                        i[1] += 1
            else:
                if env.board.snakes[0].snake_id == you:
                    i[0] += 1
                else:
                    i[1] += 1
            print(i)
            print(env.board.turn)
            env.reset()
            snakes = env.board.snakes
            you = copy.deepcopy(snakes[0].snake_id)
            opp = copy.deepcopy(snakes[1].snake_id)



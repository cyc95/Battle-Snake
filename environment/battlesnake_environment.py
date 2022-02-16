import multiprocessing

from environment.Battlesnake.agents.BaseAgent import BaseAgent
from typing import List, Optional
import pygame
import sys
import time
import traceback
from copy import deepcopy
from collections import Counter

from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.errors import AgentTimeoutError
from environment.Battlesnake.modes.Modes import GameMode
from environment.Battlesnake.modes.Royal import RoyalGame
from environment.Battlesnake.modes.Solo import SoloGame
from environment.Battlesnake.modes.Standard import StandardGame
from environment.Battlesnake.modes.Squad import SquadGame
from environment.Battlesnake.modes.AbstractGame import AbstractGame
from environment.Battlesnake.renderer.field_color import FieldColor
from environment.Battlesnake.renderer.game_renderer import GameRenderer
from environment.Battlesnake.helper.helper import Helper
from environment.Battlesnake.exporter.Exporter import Exporter

default_colors = FieldColor.SNAKE_COLORS


class BattlesnakeEnvironment:
    def __init__(
        self,
        width: int,
        height: int,
        agents: List[BaseAgent],
        act_timeout: float,
        start_paused:bool = False,
        speed_initial:int = 1,
        do_render:bool = True,
        mode:GameMode = GameMode.STANDARD,
        ruleset_settings: RulesetSettings = RulesetSettings(),
        squad_assignments: List[int] = None,
        export_games:bool = False,
        replay_name_prefix: str = None,
        replay_folder:str = "replays",
    ):
        self.width = width
        self.height = height
        self.num_snakes = len(agents)
        self.snake_ids = None
        self.agents: List[BaseAgent] = agents
        self.game: Optional[AbstractGame] = None
        self.board: Optional[BoardState] = None
        self.game_renderer = None
        self.act_timeout = act_timeout
        self.default_snake_colors = None
        self.do_render = do_render
        self.mode = mode
        self.ruleset_settings = ruleset_settings
        self.squad_assignments = squad_assignments
        if mode == GameMode.SQUAD:
            self.num_squads = len(set(squad_assignments))
            if self.num_snakes < 4:
                raise ValueError("In squad mode at least 4 players are required.")
            if (not squad_assignments or
               len(squad_assignments) != self.num_snakes or
               self.num_squads < 2 or
               any(count < 2 for count in Counter(squad_assignments).values())):
                raise ValueError("In squad mode at least 2 squads are required."
                                 " Every snake needs a squad and every squad two snakes.")

        self.speed = speed_initial
        self.paused = start_paused

        if self.paused:
            print("Press P to start game")

        self.export_games = export_games
        self.replay_name_prefix = replay_name_prefix
        self.replay_folder = replay_folder
        self.exporter = None
        self.ongoing_connections = []

    def __del__(self):
        # prevent unnecessary instances running in connected remote snakes
        if len(self.ongoing_connections) > 0:
            for idx, snake_id in enumerate(self.ongoing_connections):
                agent = self.agents[idx]
                snake = self.board.get_alive_or_dead_snake_by_id(snake_id)
                agent.end(self.game_info, self.board.turn, self.board, snake)

    def reset(self):

        self.snake_ids = [Helper.generate_snake_id() for _ in range(self.num_snakes)]

        self.default_snake_colors = default_colors.copy()

        make_filename = lambda s: "".join(x for x in s if x.isalnum())
        replay_name = "_".join(make_filename(sn.get_name()) for sn in self.agents) + "_"
        if self.replay_name_prefix:
            replay_name = self.replay_name_prefix + "_" + replay_name
        self.exporter = (
            Exporter(
                file_name=replay_name,
                output_folder=self.replay_folder,
                append_date=True,
            )
            if self.export_games
            else None
        )

        if self.mode == GameMode.STANDARD:
            game_class = StandardGame
        elif self.mode == GameMode.SOLO:
            game_class = SoloGame
        elif self.mode == GameMode.SQUAD:
            game_class = SquadGame
        elif self.mode == GameMode.ROYAL:
            game_class = RoyalGame
        else:
            raise ValueError('unknown mode:', self.mode)

        self.game = game_class(ruleset_settings=self.ruleset_settings)
        self.game_info = self.create_game_info(timeout=int(self.act_timeout * 1000), game=self.game)

        self.board = self.game.create_initial_board_state(
            width=self.width, height=self.height, snake_ids=self.snake_ids
        )

        self.update_snake_infos()
        if self.do_render:
            self.game_renderer = GameRenderer(self.width, self.height, self.num_snakes)

        if self.export_games:
            self.exporter.add_initial_state(self.game_info, self.board)

    def update_snake_infos(self):

        colors = self.default_snake_colors
        if self.mode == GameMode.SQUAD:
            squad_colors = {squad: None for squad in set(self.squad_assignments)}
            for squad in squad_colors:
                if squad_colors[squad] is None:
                    color = colors.pop(0)
                    colors.append(color)
                    squad_colors[squad] = color

        for idx, agent in enumerate(self.agents):
            snake_id = self.snake_ids[idx]
            snake = self.board.get_alive_or_dead_snake_by_id(snake_id)
            name = agent.get_name()
            color = agent.get_color()
            snake.snake_head = agent.get_head()
            snake.snake_tail = agent.get_tail()

            snake.snake_name = name

            if self.mode == GameMode.SQUAD:
                snake.squad = self.squad_assignments[idx]

            if snake.snake_color is None:
                if self.mode == GameMode.SQUAD:
                    snake.snake_color = squad_colors[snake.squad]
                else:
                    if color is None:
                        color = colors.pop(0)
                        colors.append(color)

                        snake.snake_color = color

    def handle_input(self):

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # print(event.key)
                self.user_key_pressed(event.key)

            elif event.type == pygame.QUIT:
                print("Game quit by user!")
                pygame.quit()
                sys.exit()

    def step(self):
        """
        :return: Gibt zurück, ob das Spiel beendet wurde
        """

        if self.paused:
            return

        if self.game.is_game_over(self.board):
            return True

        actions = {}
        board = self.board
        game_info = self.game_info
        turn = self.board.turn

        for idx, snake_id in enumerate(self.snake_ids):
            agent = self.agents[idx]
            snake = board.get_alive_or_dead_snake_by_id(snake_id)

            if turn == 0:
                BattlesnakeEnvironment.copy_and_call(
                    agent.start,
                    timeout=2,
                    snake_name=snake.snake_name,
                    game_info=game_info,
                    turn=turn,
                    board=board,
                    you=snake,
                )
                self.ongoing_connections.append(snake_id)

            if not snake.is_alive():
                continue

            agent_action = None
            # IDEA: use Process and set timeout
            agent_move_result, act_time = BattlesnakeEnvironment.copy_and_call(
                agent.move,
                timeout=self.act_timeout,
                snake_name=snake.snake_name,
                game_info=game_info,
                turn=turn,
                board=board,
                you=snake,
            )

            if agent_move_result is not None:
                agent_action = agent_move_result.direction

            actions[snake_id] = agent_action
            snake.latency = act_time

        self.game.create_next_board_state(board=self.board, moves=actions)

        if self.export_games:
            self.exporter.add_latest_game_step(self.board)

        is_game_over = self.game.is_game_over(self.board)
        for idx, snake_id in enumerate(self.snake_ids):
            agent = self.agents[idx]
            snake = board.get_alive_or_dead_snake_by_id(snake_id)

            call_end = False
            if not snake.is_alive() and snake.elimination_event.turn == turn:
                # check if snake dead in this turn
                call_end = True

            elif is_game_over:
                # notify alive snake that game has ended
                call_end = True

            if call_end:
                BattlesnakeEnvironment.copy_and_call(
                    agent.end,
                    timeout=2,
                    snake_name=snake.snake_name,
                    game_info=game_info,
                    turn=turn,
                    board=board,
                    you=snake,
                )
                if snake_id in self.ongoing_connections:
                    self.ongoing_connections.remove(snake_id)

        return is_game_over

    def render(self):
        self.game_renderer.display(self.board)

    def wait_after_step(self, action_time=0):

        if self.game.is_game_over(self.board):
            wait_time = 100
        else:

            if self.speed == 3:
                wait_time = 0
            elif self.speed == 2:
                wait_time = 100
            else:
                wait_time = 250

        final_wait_time = max(0, wait_time - action_time)
        if final_wait_time > 0:
            pygame.time.wait(final_wait_time)

    def wait_after_round(self):

        if self.speed == 3:
            wait_time = 500
        elif self.speed == 2:
            wait_time = 1000
        else:
            wait_time = 1500

        if wait_time > 0:
            pygame.time.wait(wait_time)

    def user_key_pressed(self, key):

        if key == pygame.K_r:
            print("user pressed reset")
            self.reset()

        elif key == pygame.K_1:
            print("set speed: 1")
            self.speed = 1

        elif key == pygame.K_2:
            print("set speed: 2")
            self.speed = 2

        elif key == pygame.K_3:
            print("set speed: 3")
            self.speed = 3

        elif key == pygame.K_p:
            print("toggle pause")
            self.paused = not self.paused

        else:
            for agent in self.agents:
                agent.user_key_pressed(key)

    def is_game_over(self):
        return self.game.is_game_over(self.board)

    def create_game_info(self, timeout, game: AbstractGame):
        game_id = Helper.generate_game_id()
        return GameInfo(game_id=game_id, ruleset_name=game.ruleset_name(), ruleset_version='v1.0.0', timeout=timeout, ruleset_settings=game.ruleset_settings)

    @staticmethod
    def copy_and_call(func, timeout=None, snake_name=None, **kwargs):
        kwargs = deepcopy(kwargs)

        try:

            # return BattlesnakeEnvironment.call_process(func=func, timeout=timeout, **kwargs)
            return BattlesnakeEnvironment.call_sync(
                func=func, timeout=timeout, **kwargs
            )

        except AgentTimeoutError:
            print("snake {}: timeout after {} seconds".format(snake_name, timeout))

        except Exception:
            traceback.print_exc()
            print(
                "snake {}: Exception raised in act method of agent".format(snake_name)
            )

        # result, act_time
        return None, None

    @staticmethod
    def call_sync(func, timeout=None, **kwargs):

        act_start_time = time.time()
        result = func(**kwargs)
        act_time = time.time() - act_start_time

        if timeout is not None:
            if act_time > timeout:
                raise AgentTimeoutError()

        return result, act_time

    @staticmethod
    def call_process(func, timeout=None, **kwargs):
        # TODO implement

        print("call_process with timeout {}".format(timeout))
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        return_dict["test"] = 1

        def call(d, **kwargs):
            print("hello world")
            print(id(kwargs["board"]))

            # print('got', kwargs)
            for i in range(4):
                print(i)
                time.sleep(1)

            d["call"] = 2
            print(d)

        p = multiprocessing.Process(target=call, args=(return_dict,), kwargs=kwargs)
        p.start()

        # Wait for X seconds or until process finishes
        p.join(timeout=timeout)

        if p.exitcode is None:
            # agent did not terminate in time
            p.terminate()
            # p.join()
            raise AgentTimeoutError()

        print("x")


import math
from typing import Tuple, List, Optional
from environment.Battlesnake.agents.BaseAgent import BaseAgent
import numpy as np
import random

from environment.Battlesnake.helper.DirectionUtil import DirectionUtil
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.MoveResult import MoveResult
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Direction import Direction
from environment.Battlesnake.model.grid_map import GridMap
from environment.Battlesnake.model.Occupant import Occupant
from environment.Battlesnake.util.kl_priority_queue import KLPriorityQueue
import copy
import time


class KILabAgentV(BaseAgent):

    def get_name(self):
        return 'Gruppe8'

    def get_head(self):
        return 'viper'

    def get_tail(self):
        return 'bolt'

    def start(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def move(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake) -> MoveResult:

        grid_map: GridMap[Occupant] = board.generate_grid_map()
        if you.health < 40:
            best_action = self.follow_food(you, board, grid_map)
        else:
            best_action = self.attack(you, board, grid_map)
            if best_action is None:
                best_action = self.follow_food(you, board, grid_map)
        if best_action is not None:
            return MoveResult(direction=best_action)
        best_actions = self.survive(you, board, grid_map)
        return MoveResult(direction=best_actions)

    def survive(slef, you: Snake,
                board: BoardState,
                grid_map: GridMap):
        
        queue = KLPriorityQueue()
        came_from = {}
        cost_so_far = {}

        # calc heuristic for start and search field
        # add start_field to queue
        current_field = you.get_head()
        search_field = current_field
        queue.put(0.0 , current_field)
        cost_so_far[current_field] = 0.0
        while not queue.empty():
            # get node from queue
            current_field = queue.get()
            # find all neighbors that are valid
            neighbors = [
                [current_field.x + 1, current_field.y],
                [current_field.x - 1, current_field.y],
                [current_field.x, current_field.y + 1],
                [current_field.x, current_field.y - 1]
            ]
            valid_neighbors = [Position(x=n[0], y=n[1]) for n in neighbors if grid_map.is_valid_at(n[0], n[1]) and not board.is_occupied_by_snake(Position(n[0],n[1]))]
            
            for neighbor in valid_neighbors:
                if neighbor not in cost_so_far:
                    cost_so_far[neighbor] = cost_so_far[current_field] - 1
                    #cost_so_far[current_field] -= 1
                    came_from[neighbor] = current_field
                    #count number of valid neighbors
                    neighbors = [
                    [current_field.x + 1, current_field.y],
                    [current_field.x - 1, current_field.y],
                    [current_field.x, current_field.y + 1],
                    [current_field.x, current_field.y - 1]
                    ]
                    number_of_valid_neighbors = len([Position(x=n[0], y=n[1]) for n in neighbors if grid_map.is_valid_at(n[0], n[1]) and not board.is_occupied_by_snake(Position(n[0],n[1]))])
            

                    if number_of_valid_neighbors > 0:
                        #queue.put(float(-number_of_valid_neighbors + cost_so_far[neighbor]), neighbor)
                        queue.put(float(-number_of_valid_neighbors), neighbor)
                        search_field = neighbor
        
        # Berechnung des Pfades
        
        current_field = Position(search_field.x, search_field.y)
        if current_field not in came_from:
            return None
        while not came_from[current_field].is_position_equal_to(you.get_head()):
            current_field = came_from[current_field]
        # while not came_from[current_field].is_position_equal_to(start_field):
        #     if current_field.x - came_from[current_field].x == 1:
        #         path.insert(0, [current_field, Direction.RIGHT])
        #     if current_field.x - came_from[current_field].x == -1:
        #         path.insert(0, [current_field, Direction.LEFT])
        #     if current_field.y - came_from[current_field].y == 1:
        #         path.insert(0, [current_field, Direction.UP])
        #     if current_field.y - came_from[current_field].y == -1:
        #         path.insert(0, [current_field, Direction.DOWN])
        #     current_field = came_from[current_field]
        # if current_field.x - came_from[current_field].x == 1:
        #     path.insert(0, [current_field, Direction.RIGHT])
        # if current_field.x - came_from[current_field].x == -1:
        #     path.insert(0, [current_field, Direction.LEFT])
        # if current_field.y - came_from[current_field].y == 1:
        #     path.insert(0, [current_field, Direction.UP])
        # if current_field.y - came_from[current_field].y == -1:
        #     path.insert(0, [current_field, Direction.DOWN])
        if current_field.x - came_from[current_field].x == 1:
            path = Direction.RIGHT
        if current_field.x - came_from[current_field].x == -1:
            path = Direction.LEFT
        if current_field.y - came_from[current_field].y == 1:
            path = Direction.UP
        if current_field.y - came_from[current_field].y == -1:
            path = Direction.DOWN
        return path

    def end(self, game_info: GameInfo, turn: int, board: BoardState, you: Snake):
        pass

    def follow_food(self, snake: Snake, board: BoardState, grid_map: GridMap):

        head = snake.get_head()
        lowcost = math.inf
        bestpath = None
        for food in board.food:
            distance, path = KILabAgentV.a_star_search(head, food, board, grid_map)
            if distance < lowcost:
                bestpath = path
                lowcost = distance
        return bestpath

    def attack(self, snake: Snake, board: BoardState, grid_map: GridMap):
        opp_snake = copy.deepcopy([n for n in board.get_alive_and_dead_snakes() if n.snake_id != snake.snake_id][0])
        if opp_snake.get_length() < 3:
            return None
        opp_snake_x = np.zeros(opp_snake.get_length())
        opp_snake_y = np.zeros(opp_snake.get_length())
        for idx, body in enumerate(opp_snake.body):
            opp_snake_x[idx-1] = body.x
            opp_snake_y[idx-1] = body.y
        opp_snake_x_Centroid = np.mean(opp_snake_x)
        opp_snake_y_Centroid = np.mean(opp_snake_y)
        opp_snake_x_var = np.var(opp_snake_x)
        opp_snake_y_var = np.var(opp_snake_y)
        policy = []
        bestpath = None
        if opp_snake_x_var <= opp_snake_y_var:
            policy.append('y')
            #y wichtig .fest
            if np.mean(opp_snake_y_Centroid + opp_snake.body[0].y) < int(board.height / 2):
                policy.append(0)
                # y = 0
                if np.mean(opp_snake_x_Centroid + opp_snake.body[0].x) < int(board.height / 2):
                    policy.append(board.height-1)
                    # x = board.height
                    search = self.find_position(grid_map, policy)

                  #  print('ziel')
                  #  print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
                else:
                    policy.append(0)
                    # x = 0
                    search = self.find_position(grid_map, policy)

                 #   print('ziel')
                 #   print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
            else:
                policy.append(board.height - 1)
                # y = board.height
                if np.mean(opp_snake_x_Centroid + opp_snake.body[0].x) < int(board.height / 2):
                    policy.append(board.height-1)
                    # x = board.height
                    search = self.find_position(grid_map, policy)

                  #  print('ziel')
                  #  print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
                else:
                    policy.append(0)
                    # x = 0
                    search = self.find_position(grid_map, policy)

                  #  print('ziel')
                  #  print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)

        else:
            policy.append('x')
            #x wichtig .fest
            if np.mean(opp_snake_x_Centroid + opp_snake.body[0].x) < int(board.height / 2):
                # x = 0
                policy.append(0)
                if np.mean(opp_snake_y_Centroid + opp_snake.body[0].y) < int(board.height / 2):
                    policy.append(board.height-1)
                    # y = board.height
                    search = self.find_position(grid_map, policy)

                #    print('ziel')
                #    print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
                else:
                    policy.append(0)
                    # y = 0

                    search = self.find_position(grid_map, policy)

                 #   print('ziel')
                 #   print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
            else:
                # x = board.height
                policy.append(board.height - 1)
                if np.mean(opp_snake_y_Centroid + opp_snake.body[0].y) < int(board.height / 2):
                    policy.append(board.height-1)
                    # y = board.height
                    search = self.find_position(grid_map, policy)

                #    print('ziel')
               #     print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
                else:
                    policy.append(0)
                    # y = 0
                    search = self.find_position(grid_map, policy)

               #     print('ziel')
               #     print(search)

                    if search is not None:
                        cost, bestpath = self.a_star_search(snake.body[0], search, board, grid_map)
        return bestpath

    def find_position(self, grid_map, policy):
        if policy[0] == 'x':
            bestposition = Position(x=policy[1], y=policy[2])
            while grid_map.grid_cache[bestposition.x][bestposition.y] == Occupant.Snake or grid_map.grid_cache[bestposition.x][int(bestposition.y - (bestposition.y - 5) / abs(bestposition.y - 5))] == Occupant.Snake:
                if policy[1] <= 5:
                    bestposition.x += 1
                    if bestposition.x > 10:
                        bestposition.x = 0
                        bestposition.y = int(bestposition.y - (bestposition.y - 5) / abs(bestposition.y - 5))
                else:
                    bestposition.x -= 1
                    if bestposition.x < 0:
                        bestposition.x = 0
                        bestposition.y = int(bestposition.y - (bestposition.y - 5) / abs(bestposition.y - 5))
                if bestposition.y == 5:
                    break
                if bestposition.x == 5:
                    break
            while grid_map.grid_cache[bestposition.x][bestposition.y] != Occupant.Snake:
                if policy[2] == 0:
                    if bestposition.y == 10:
                        return None
                    bestposition.y += 1
                else:
                    if bestposition.y == 0:
                        return None
                    bestposition.y -= 1
        if policy[0] == 'y':
            bestposition = Position(y=policy[1], x=policy[2])
            while grid_map.grid_cache[bestposition.x][bestposition.y] == Occupant.Snake or grid_map.grid_cache[int(bestposition.x - (bestposition.x - 5) / abs(bestposition.x - 5))][bestposition.y] == Occupant.Snake:
                if policy[1] <= 5:
                    bestposition.y += 1
                    if bestposition.y > 10:
                        bestposition.y = 0
                        bestposition.x = int(bestposition.x - (bestposition.x - 5) / abs(bestposition.x - 5))
                else:
                    bestposition.y -= 1
                    if bestposition.y < 0:
                        bestposition.y = 0
                        bestposition.x = int(bestposition.x - (bestposition.x - 5) / abs(bestposition.x - 5))
                if bestposition.x == 5:
                    break
                if bestposition.y == 5:
                    break
            while grid_map.grid_cache[bestposition.x][bestposition.y] != Occupant.Snake:
                if policy[2] == 0:
                    if bestposition.x == 10:
                        return None
                    bestposition.x += 1
                else:
                    if bestposition.x == 0:
                        return None
                    bestposition.x -= 1
        return bestposition

    @staticmethod
    def a_star_search(start_field: Position,
                      search_field: Position,
                      board: BoardState,
                      grid_map: GridMap) -> Tuple[int, List[Tuple[Position, Direction]]]:
        if start_field.x == search_field.x and start_field.y == search_field.y:
            return None,None
        queue = KLPriorityQueue()
        came_from = {}
        cost_so_far = {}
        Ziel = Position(x=search_field.x, y=search_field.y)
        # calc heuristic for start and search field
        # add start_field to queue
        queue.put((abs(start_field.x - search_field.x) + abs(start_field.y - search_field.y)), start_field)
        cost_so_far[start_field] = 0.0
        while not queue.empty():
            # get node from queue
            current_field = queue.get()
            # check if search_field was found
            # find all neighbors that are valid
            neighbors = [
                [current_field.x + 1, current_field.y],
                [current_field.x - 1, current_field.y],
                [current_field.x, current_field.y + 1],
                [current_field.x, current_field.y - 1]
            ]
            valid_neighbors = [Position(x=n[0], y=n[1]) for n in neighbors if grid_map.is_valid_at(n[0], n[1])]
            for neighbor in valid_neighbors:
                if neighbor not in cost_so_far and grid_map.get_value_at_position(neighbor) != Occupant.Snake:
                    cost_so_far[neighbor] = cost_so_far[current_field] + 1
                    came_from[neighbor] = current_field
                    queue.put(
                        (cost_so_far[neighbor] + abs(neighbor.x - search_field.x) + abs(neighbor.y - search_field.y)),
                        neighbor)
                # ob neighbor in queue
                # ja: check ob Kosten (F) geringer sind
                # nein: add neighbor to queue
        # Berechnung des Pfades
        if Ziel not in cost_so_far:
            cost = np.inf
        else:
            cost = cost_so_far[Ziel]
        # path: List[Tuple[Position, Direction]] = []
        current_field = Position(Ziel.x, Ziel.y)
        if current_field not in came_from:
            return np.inf, None
        while not came_from[current_field].is_position_equal_to(start_field):
            current_field = came_from[current_field]
        # while not came_from[current_field].is_position_equal_to(start_field):
        #     if current_field.x - came_from[current_field].x == 1:
        #         path.insert(0, [current_field, Direction.RIGHT])
        #     if current_field.x - came_from[current_field].x == -1:
        #         path.insert(0, [current_field, Direction.LEFT])
        #     if current_field.y - came_from[current_field].y == 1:
        #         path.insert(0, [current_field, Direction.UP])
        #     if current_field.y - came_from[current_field].y == -1:
        #         path.insert(0, [current_field, Direction.DOWN])
        #     current_field = came_from[current_field]
        # if current_field.x - came_from[current_field].x == 1:
        #     path.insert(0, [current_field, Direction.RIGHT])
        # if current_field.x - came_from[current_field].x == -1:
        #     path.insert(0, [current_field, Direction.LEFT])
        # if current_field.y - came_from[current_field].y == 1:
        #     path.insert(0, [current_field, Direction.UP])
        # if current_field.y - came_from[current_field].y == -1:
        #     path.insert(0, [current_field, Direction.DOWN])
        if current_field.x - came_from[current_field].x == 1:
            path = Direction.RIGHT
        if current_field.x - came_from[current_field].x == -1:
            path = Direction.LEFT
        if current_field.y - came_from[current_field].y == 1:
            path = Direction.UP
        if current_field.y - came_from[current_field].y == -1:
            path = Direction.DOWN
        return cost, path
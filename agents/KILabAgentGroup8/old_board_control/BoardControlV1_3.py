import numpy as np
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.util.kl_priority_queue import KLPriorityQueue
import copy


def BoardControl(board: BoardState, you: Snake):
    # It takes too long to calculate accurately, so here is an approximate calculation
    you_snake_id = you.snake_id
    length_you = 0
    length_opp = 0
    if len(board.snakes) == 1:
        if board.snakes[0].snake_id == you_snake_id:
            return 121
        else:
            return -121
    if len(board.snakes) == 0:
        for snake in board.dead_snakes:
            if snake.snake_id == you_snake_id:
                length_you = len(snake.body)
            else:
                length_opp = len(snake.body)
        if length_you > length_opp:
            return 121
        if length_you < length_opp:
            return -121
        return 0
    state = np.zeros(shape=(board.width, board.height), dtype='int32')
    Control_state = np.zeros(shape=(board.width, board.height), dtype='int32')
    Control_you = 0
    Control_opp = 0
    wall_you = {}
    wall_opp = {}
    wall_you_2 = {}
    wall_opp_2 = {}
    low_wall_you = np.inf
    low_wall_opp = np.inf
    you_end = True
    opp_end = True
    you_food = 0
    opp_food = 0
    queue = []
    queue_opp = []
    queue_neu = []
    queue_opp_neu = []

    for f in board.food:
        state[f.x][f.y] = 500
    for snake in board.snakes:
        if not snake.is_alive():
            continue
        for i in range(len(snake.body)):
            if snake.snake_id == you_snake_id:
                state[snake.body[-i-1].x][snake.body[-i-1].y] = i + 1
            else:
                state[snake.body[-i-1].x][snake.body[-i-1].y] = i + 1
            Control_state[snake.body[-i - 1].x][snake.body[-i - 1].y] = 200
        if snake.snake_id == you_snake_id:
            queue.append(snake.body[0])
            length_you = len(snake.body)
        else:
            queue_opp.append(snake.body[0])
            length_opp = len(snake.body)
    if length_you >= length_opp:
        for i in range(1, 121):
            if not queue and not queue_opp:
                break
            if not queue:
                if low_wall_you > Control_you + 1 - you_food and low_wall_you != np.inf:
                    you_end = False
            if not queue_opp:
                if low_wall_opp > Control_opp + 1 - opp_food and low_wall_opp != np.inf:
                    opp_end = False
            while queue:
                current_field = queue.pop()
                neighbors = [
                    [current_field.x + 1, current_field.y],
                    [current_field.x - 1, current_field.y],
                    [current_field.x, current_field.y + 1],
                    [current_field.x, current_field.y - 1]
                ]
                for neighbor in neighbors:
                    if (10 >= neighbor[0] >= 0) and (10 >= neighbor[1] >= 0):
                        if Control_state[neighbor[0]][neighbor[1]] == 0:
                            Control_state[neighbor[0]][neighbor[1]] = 1
                            if state[neighbor[0]][neighbor[1]] == 500:
                                you_food += 1
                            Control_you += 1
                            queue_neu.append(Position(x=neighbor[0], y=neighbor[1]))
                        if Control_state[neighbor[0]][neighbor[1]] == 200:
                            if state[neighbor[0]][neighbor[1]] not in wall_you:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_you[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                else:
                                    if state[neighbor[0]][neighbor[1]] < low_wall_you:
                                        low_wall_you = state[neighbor[0]][neighbor[1]]
                            else:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_you_2[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                else:
                                    if state[neighbor[0]][neighbor[1]] < low_wall_you:
                                        low_wall_you = state[neighbor[0]][neighbor[1]]
            while queue_opp:
                current_field = queue_opp.pop()
                neighbors = [
                    [current_field.x + 1, current_field.y],
                    [current_field.x - 1, current_field.y],
                    [current_field.x, current_field.y + 1],
                    [current_field.x, current_field.y - 1]
                ]
                for neighbor in neighbors:
                    if (10 >= neighbor[0] >= 0) and (10 >= neighbor[1] >= 0):
                        if Control_state[neighbor[0]][neighbor[1]] == 0:
                            Control_state[neighbor[0]][neighbor[1]] = -1
                            if state[neighbor[0]][neighbor[1]] == 500:
                                opp_food += 1
                            Control_opp += 1
                            queue_opp_neu.append(Position(x=neighbor[0], y=neighbor[1]))
                        if Control_state[neighbor[0]][neighbor[1]] == 200:
                            if state[neighbor[0]][neighbor[1]] not in wall_opp:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_opp[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                else:
                                    if state[neighbor[0]][neighbor[1]] < low_wall_opp:
                                        low_wall_opp = state[neighbor[0]][neighbor[1]]
                            else:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_opp_2[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                else:
                                    if state[neighbor[0]][neighbor[1]] < low_wall_opp:
                                        low_wall_opp = state[neighbor[0]][neighbor[1]]

            queue = copy.deepcopy(queue_neu)
            queue_neu = []
            queue_opp = copy.deepcopy(queue_opp_neu)
            queue_opp_neu = []
            if you_end:
                if i in wall_you:
                    Control_state[wall_you[i].x][wall_you[i].y] = 1
                    Control_you += 1
                    queue.append(wall_you[i])
                    if i in wall_you_2:
                        Control_state[wall_you_2[i].x][wall_you_2[i].y] = 1
                        Control_you += 1
                        queue.append(wall_you_2[i])
            if opp_end:
                if i in wall_opp:
                    if Control_state[wall_opp[i].x][wall_opp[i].y] != 1:
                        Control_state[wall_opp[i].x][wall_opp[i].y] = - 1
                        Control_opp += 1
                        queue_opp.append(wall_opp[i])
                    if i in wall_opp_2:
                        if Control_state[wall_opp_2[i].x][wall_opp_2[i].y] != 1:
                            Control_state[wall_opp_2[i].x][wall_opp_2[i].y] = - 1
                            Control_opp += 1
                            queue_opp.append(wall_opp_2[i])
    else:
        for i in range(1, 121):
            if not queue and not queue_opp:
                break
            if not queue:
                if low_wall_you > Control_you + 1 - you_food and low_wall_you != np.inf:
                    you_end = False
            if not queue_opp:
                if low_wall_opp > Control_opp + 1 - opp_food and low_wall_opp != np.inf:
                    opp_end = False
            while queue_opp:
                current_field = queue_opp.pop()
                neighbors = [
                    [current_field.x + 1, current_field.y],
                    [current_field.x - 1, current_field.y],
                    [current_field.x, current_field.y + 1],
                    [current_field.x, current_field.y - 1]
                ]
                for neighbor in neighbors:
                    if (10 >= neighbor[0] >= 0) and (10 >= neighbor[1] >= 0):
                        if Control_state[neighbor[0]][neighbor[1]] == 0:
                            Control_state[neighbor[0]][neighbor[1]] = -1
                            if state[neighbor[0]][neighbor[1]] == 500:
                                opp_food += 1
                            Control_opp += 1
                            queue_opp_neu.append(Position(x=neighbor[0], y=neighbor[1]))
                        if Control_state[neighbor[0]][neighbor[1]] == 200:
                            if state[neighbor[0]][neighbor[1]] not in wall_opp:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_opp[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                if state[neighbor[0]][neighbor[1]] < low_wall_opp:
                                    low_wall_opp = state[neighbor[0]][neighbor[1]]
                            else:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_opp_2[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                if state[neighbor[0]][neighbor[1]] < low_wall_opp:
                                    low_wall_opp = state[neighbor[0]][neighbor[1]]
            while queue:
                current_field = queue.pop()
                neighbors = [
                    [current_field.x + 1, current_field.y],
                    [current_field.x - 1, current_field.y],
                    [current_field.x, current_field.y + 1],
                    [current_field.x, current_field.y - 1]
                ]
                for neighbor in neighbors:
                    if (10 >= neighbor[0] >= 0) and (10 >= neighbor[1] >= 0):
                        if Control_state[neighbor[0]][neighbor[1]] == 0:
                            Control_state[neighbor[0]][neighbor[1]] = 1
                            if state[neighbor[0]][neighbor[1]] == 500:
                                you_food += 1
                            Control_you += 1
                            queue_neu.append(Position(x=neighbor[0], y=neighbor[1]))
                        if Control_state[neighbor[0]][neighbor[1]] == 200:
                            if state[neighbor[0]][neighbor[1]] not in wall_you:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_you[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                else:
                                    if state[neighbor[0]][neighbor[1]] < low_wall_you:
                                        low_wall_you = state[neighbor[0]][neighbor[1]]
                            else:
                                if state[neighbor[0]][neighbor[1]] <= i:
                                    wall_you_2[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                                else:
                                    if state[neighbor[0]][neighbor[1]] < low_wall_you:
                                        low_wall_you = state[neighbor[0]][neighbor[1]]
            queue = copy.deepcopy(queue_neu)
            queue_neu = []
            queue_opp = copy.deepcopy(queue_opp_neu)
            queue_opp_neu = []
            if opp_end:
                if i in wall_opp:
                    Control_state[wall_opp[i].x][wall_opp[i].y] = - 1
                    Control_opp += 1
                    queue_opp.append(wall_opp[i])
                    if i in wall_opp_2:
                        Control_state[wall_opp_2[i].x][wall_opp_2[i].y] = - 1
                        Control_opp += 1
                        queue_opp.append(wall_opp_2[i])
            if you_end:
                if i in wall_you:
                    if Control_state[wall_you[i].x][wall_you[i].y] != -1:
                        Control_state[wall_you[i].x][wall_you[i].y] = 1
                        Control_you += 1
                        queue.append(wall_you[i])
                    if i in wall_you_2:
                        if Control_state[wall_you_2[i].x][wall_you_2[i].y] != -1:
                            Control_state[wall_you_2[i].x][wall_you_2[i].y] = 1
                            Control_you += 1
                            queue.append(wall_you_2[i])

    result = Control_you - Control_opp
    if opp_end != you_end:
        if not you_end:
            result = -121
        else:
            result = 121
    return result


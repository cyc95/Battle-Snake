import numpy as np
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.util.kl_priority_queue import KLPriorityQueue
import copy

## Rewards:
# win: 121
# lost: -121
# tie: 0

def BoardControl(board: BoardState, you: Snake):
    # It takes too long to calculate accurately, so here is an approximate calculation
     
    you_snake_id = you.snake_id
    length_you = 0
    length_opp = 0

    # check if game is already won or lost
    if len(board.snakes) == 1:
        if board.snakes[0].snake_id == you_snake_id:
            return 121 # win reward
        else:
            return -121 # loss reward

    # head to head accident
    if len(board.snakes) == 0:
        for snake in board.dead_snakes:
            if snake.snake_id == you_snake_id:
                length_you = len(snake.body)
            else:
                length_opp = len(snake.body)
        if length_you > length_opp:
            return 121 # win
        if length_you < length_opp:
            return -121 # loss
        return 0 # tie

    # initialize empty states: state, snake, control
    state = np.zeros(shape=(board.width, board.height), dtype='int32')
    snake_state = np.zeros(shape=(board.width, board.height), dtype='int32')
    Control_state = np.zeros(shape=(board.width, board.height), dtype='int32')

    # NOTE initialize values (?)
    Control_you = 0
    Control_opp = 0
    wall_you = {}
    wall_opp = {}
    wall_you_2 = {}
    wall_opp_2 = {}
    low_wall_you = np.inf
    low_wall_opp = np.inf
    you_end = True # you alive default: True
    opp_end = True # opp alive
    you_food = 0 # number of food in our controlled area
    opp_food = 0 # number of food in their controlled area

    # NOTE init queues
    queue = []
    queue_opp = []
    queue_neu = []
    queue_opp_neu = []

    for f in board.food:
        state[f.x][f.y] = 500 # 500 means foo on state?

    # iterate over all snakes on board (dead or alive)
    for snake in board.snakes:

        # check if snake is already dead
        if not snake.is_alive():
            continue

        for i in range(len(snake.body)):


            if snake.snake_id == you_snake_id:
                # numbered position of snake: 1 Head, 12 Tail
                state[snake.body[-i - 1].x][snake.body[-i - 1].y] = i + 1 
                snake_state[snake.body[-i - 1].x][snake.body[-i - 1].y] = 1 # mark snake pos on snake state
            else:
                state[snake.body[-i - 1].x][snake.body[-i - 1].y] = i + 1
                snake_state[snake.body[-i - 1].x][snake.body[-i - 1].y] = -1 # mark snake pos on snake state
            
            # mark snake pos on control state as a wall
            Control_state[snake.body[-i - 1].x][snake.body[-i - 1].y] = 200 


        if snake.snake_id == you_snake_id:
            queue.append(snake.body[0]) # save snake head to queue
            Control_state[snake.body[0].x][snake.body[0].y] = 1 # mark snake head in control state 1
            length_you = len(snake.body)
        else:
            queue_opp.append(snake.body[0]) # save snake head to opp queue
            Control_state[snake.body[0].x][snake.body[0].y] = -1 # mark snake head in control state -1
            length_opp = len(snake.body) # NOTE where to store length of opp

    ## end snake for loop

    
    if length_you > length_opp:


        # 11*11 = 121
        for i in range(1, 121):

            # check if queues are already empty
            if not queue and not queue_opp:
                break

            # check if we are almost dead or not
            you_end = almost_dead(board, queue, length_you, Control_you, you_food, low_wall_you, you_end, you_snake_id, Control_state, state)

            # check if opp is almost dead
            opp_snake_id = 15000
            for snake in board.snakes:
                if snake.snake_id != you_snake_id:
                    opp_snake_id = snake.snake_id

            opp_end = almost_dead(board, queue_opp, length_opp, Control_opp, opp_food, low_wall_opp, opp_end, opp_snake_id, Control_state, state)

            # flood fill our snake
            Control_state, you_food, Control_you, queue_neu, wall_you, low_wall_you, wall_you_2 = food_fill(queue, Control_state, state, you_food, Control_you, queue_neu, wall_you, low_wall_you, i, wall_you_2, player_piece=1)

            # flood fill opp : equal to player flood fill
            Control_state, opp_food, Control_opp, queue_opp_neu, wall_opp, low_wall_opp, wall_opp_2 = food_fill(queue_opp, Control_state, state, opp_food, Control_opp, queue_opp_neu, wall_opp, low_wall_opp, i, wall_opp_2, player_piece= -1)

            if you_end:

                # add wall part to queue if reachable in i steps
                Control_state, Control_you, queue = update_queue(i, wall_you, Control_state, Control_you, queue, wall_you_2, player_piece= 1)
                

            if opp_end:
                # add wall part to queue if reachable in i steps
                Control_state, Control_opp, queue_opp = update_queue(i, wall_opp, Control_state, Control_opp, queue_opp, wall_opp_2, player_piece= -1)

    else: # if length_you <= length_opp:
        for i in range(1, 121):

            # check if there are still open (0) fields to explore
            if not queue and not queue_opp:
                break

            # check if we are almost dead or not
            you_end = almost_dead(board, queue, length_you, Control_you, you_food, low_wall_you, you_end, you_snake_id, Control_state, state)

            # check if opp is almost dead
            opp_snake_id = 15000
            for snake in board.snakes:
                if snake.snake_id != you_snake_id:
                    opp_snake_id = snake.snake_id

            opp_end = almost_dead(board, queue_opp, length_opp, Control_opp, opp_food, low_wall_opp, opp_end, opp_snake_id, Control_state, state)

            # flood fill opp first, because opp is longer
            Control_state, opp_food, Control_opp, queue_opp_neu, wall_opp, low_wall_opp, wall_opp_2 = food_fill(queue_opp, Control_state, state, opp_food, Control_opp, queue_opp_neu, wall_opp, low_wall_opp, i, wall_opp_2, player_piece= -1)

            # flood fill for us second, because we are shorter than opp
            Control_state, you_food, Control_you, queue_neu, wall_you, low_wall_you, wall_you_2 = food_fill(queue, Control_state, state, you_food, Control_you, queue_neu, wall_you, low_wall_you, i, wall_you_2, player_piece=1)


    for i in range(11):
        for j in range(11):

            # add snake body to control area of corresponding snake
            if Control_state[i][j] == 200:
                # area under our control (with body)
                if snake_state[i][j] == 1:
                    Control_state[i][j] = 1
                    Control_you += 1

                # area under opp control (with body)
                else:
                    Control_state[i][j] = -1
                    Control_opp += 1
    
    # check for empty fields that are blocked by snake bodies (at the moment)
    for i in range(11):
        for j in range(11):
            if Control_state[i][j] == 0:
                flag_you = 0
                flag_opp = 0
                valid_neighbors = get_valid_neighbors(i, j)

                # add field to nearest snake control area
                for neighbor in valid_neighbors:
                    if Control_state[neighbor[0]][neighbor[1]] == 1:
                        flag_you = 1
                    if Control_state[neighbor[0]][neighbor[1]] == -1:
                        flag_opp = 1
                if flag_you == 1 and flag_opp == 0:
                    Control_state[i][j] = 1
                    Control_you += 1
                    queue.append(Position(x=i, y=j))
                if flag_you == 0 and flag_opp == 1:
                    Control_state[i][j] = - 1
                    Control_opp += 1
                    queue_opp.append(Position(x=i, y=j))

    
    if length_you > length_opp:
        for i in range(1, 121):
            if not queue and not queue_opp:
                break

            Control_state, Control_you, queue_neu = update_queue_neu(queue, Control_state, Control_you, queue_neu, player_piece= 1)
            Control_state, Control_opp, queue_opp_neu = update_queue_neu(queue_opp, Control_state, Control_opp, queue_opp_neu, player_piece= -1)

            queue = copy.deepcopy(queue_neu)
            queue_neu = []
            queue_opp = copy.deepcopy(queue_opp_neu)
            queue_opp_neu = []
    else: # length_you <= length_opp:
        for i in range(1, 121):
            if not queue and not queue_opp:
                break

            Control_state, Control_opp, queue_opp_neu = update_queue_neu(queue_opp, Control_state, Control_opp, queue_opp_neu, player_piece= -1)
            Control_state, Control_you, queue_neu = update_queue_neu(queue, Control_state, Control_you, queue_neu, player_piece= 1)

            queue = copy.deepcopy(queue_neu)
            queue_neu = []
            queue_opp = copy.deepcopy(queue_opp_neu)
            queue_opp_neu = []

    result = Control_you - Control_opp
    if opp_end != you_end:
        if not you_end:# we are almost dead (!= we are dead)
            result = Control_you / 2 - 120 # very small reward
        else: # opp is almost dead
            result = 120 - Control_opp / 2 # relatively high reward (because opp almost dead)
    return result




def get_valid_neighbors(x, y):
    neighbors = [
        [x + 1, y],
        [x - 1, y],
        [x, y + 1],
        [x, y - 1]
    ]
    valid_neighbors = [n for n in neighbors if 10 >= n[0] >= 0 and 10 >= n[1] >= 0]
    return valid_neighbors



def almost_dead(board, queue, length_you, Control_you, you_food, low_wall_you, you_end, you_snake_id, Control_state, state):
    if not queue:
    

        # (length_you > Control_you + 1 - you_food): check if we have room to live under our control
        if (length_you > Control_you + 1 - you_food):

            # check if snake is already doomed
            # (low_wall_you > Control_you + 1 - you_food): no time to escape blocked area :(
            # low_wall_you != np.inf: spot in wall could become free in time
            if (low_wall_you > Control_you + 1 - you_food) and low_wall_you != np.inf :
                you_end = False # set life status to false

            else: # we could still have a chance, maybe
                # fk. it is too complicated  :( check here, if the snake is still alive or not. you_end = True -> alive
                queue_check = []
                flag = True
                Control_check = 0
                wall_check = []
                queue_check_neu = []
                check_state = np.zeros(shape=(board.width, board.height), dtype='int32')
                for snake in board.snakes:
                    if snake.snake_id == you_snake_id:
                        queue_check.append(snake.body[0]) # add our head to queue
                
                you_end = False
                while flag:
                    flag = False

                    while queue_check:
                        current_field = queue_check.pop()
                        valid_neigbors = get_valid_neighbors(current_field.x, current_field.y)
                        for neighbor in valid_neigbors:
                                if Control_state[neighbor[0]][neighbor[1]] == 1 and check_state[neighbor[0]][neighbor[1]] == 0:
                                    flag = True
                                    nummer = 0
                                    for neighbor_neighbor in get_valid_neighbors(neighbor[0], neighbor[1]):
                                        if Control_state[neighbor_neighbor[0]][neighbor_neighbor[1]] == 1:
                                            nummer += 1
                                    if nummer >= 3:
                                        queue_check.append(Position(x=neighbor[0], y=neighbor[1]))
                                        check_state[neighbor[0]][neighbor[1]] = 1
                                        Control_check += 1
                                    else:
                                        queue_check_neu.append(Position(x=neighbor[0], y=neighbor[1]))
                                        check_state[neighbor[0]][neighbor[1]] = 1
                                if Control_state[neighbor[0]][neighbor[1]] == 200 and check_state[neighbor[0]][neighbor[1]] == 0:
                                    check_state[neighbor[0]][neighbor[1]] = 1
                                    wall_check.append(Position(x=neighbor[0], y=neighbor[1]))
                    flag_1 = False
                    for Wall in wall_check:
                        if state[Wall.x][Wall.y] <= Control_check + 1:
                            flag_1 = True
                            you_end = True
                    if flag_1:
                        break
                    queue_check = copy.deepcopy(queue_check_neu)
                    wall_check = []
                    while queue_check_neu:
                        current_field = queue_check_neu.pop()
                        for neighbor in get_valid_neighbors(current_field.x, current_field.y):
                            if Control_state[neighbor[0]][neighbor[1]] == 200 and check_state[neighbor[0]][neighbor[1]] == 0:
                                wall_check.append(Position(x=neighbor[0], y=neighbor[1]))
                                check_state[neighbor[0]][neighbor[1]] = 1
                    for Wall in wall_check:
                        if state[Wall.x][Wall.y] <= Control_check + 2:
                            flag_1 = True
                            you_end = True
                    if flag_1:
                        break
                    wall_check = []
                    Control_check = Control_check + len(queue_check)
    return you_end


def food_fill(queue, Control_state, state, you_food, Control_you, queue_neu, wall_you, low_wall_you, i, wall_you_2, player_piece):
    while queue:
            current_field = queue.pop()

            for neighbor in get_valid_neighbors(current_field.x, current_field.y):
                if Control_state[neighbor[0]][neighbor[1]] == 0: # check if field was visited before
                    Control_state[neighbor[0]][neighbor[1]] = player_piece # set field to our number (1)
                    
                    # check if food is in neighboring field
                    if state[neighbor[0]][neighbor[1]] == 500:
                        you_food += 1
                    
                    # count controlled fields
                    Control_you += 1

                    # add current field as Postion obj to queue neu
                    queue_neu.append(Position(x=neighbor[0], y=neighbor[1]))

                # check if field is blocked by snake body
                if Control_state[neighbor[0]][neighbor[1]] == 200:

                    # store body parts postition in wall_you
                    if state[neighbor[0]][neighbor[1]] not in wall_you:
                        if state[neighbor[0]][neighbor[1]] <= i: # check if in i steps reachable
                            wall_you[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                        else:
                            if state[neighbor[0]][neighbor[1]] < low_wall_you: # update low_wall_you
                                low_wall_you = state[neighbor[0]][neighbor[1]] # 'smallest' wall part
                    
                    else: 
                        # NOTE copy of wall_you?
                        if state[neighbor[0]][neighbor[1]] <= i:
                            wall_you_2[state[neighbor[0]][neighbor[1]]] = Position(x=neighbor[0], y=neighbor[1])
                        else:
                            if state[neighbor[0]][neighbor[1]] < low_wall_you:
                                low_wall_you = state[neighbor[0]][neighbor[1]]


    return Control_state, you_food, Control_you, queue_neu, wall_you, low_wall_you, wall_you_2

def update_queue(i, wall_you, Control_state, Control_you, queue, wall_you_2, player_piece):
    if i in wall_you:
        Control_state[wall_you[i].x][wall_you[i].y] = player_piece
        Control_you += 1
        queue.append(wall_you[i])
        if i in wall_you_2:
            Control_state[wall_you_2[i].x][wall_you_2[i].y] = player_piece
            Control_you += 1
            queue.append(wall_you_2[i])
    return Control_state, Control_you, queue

def update_queue_neu(queue, Control_state, Control_you, queue_neu, player_piece):
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
                    Control_state[neighbor[0]][neighbor[1]] = player_piece
                    Control_you += 1
                    queue_neu.append(Position(x=neighbor[0], y=neighbor[1]))
    return Control_state, Control_you, queue_neu
import typing, math
import numpy as np
from environment.battlesnake_environment import BattlesnakeEnvironment
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.Position import Position
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.board_state import BoardState
from environment.Battlesnake.model.grid_map import GridMap
from agents.KILabAgentGroup8.old_board_control.BoardControlV1_5backup import BoardControl
from agents.RandomAgent.RandomAgent import RandomAgent
import copy
import time


class UCTNode:
    def __init__(
            self,
            boardState: BoardState,
            you: Snake,
            action: int,
            parent: typing.Optional["UCTNode"] = None,
    ):
        self.state = boardState
        self.active_player = you.snake_id
        self.parent = parent
        self.action = action
        self.children: typing.Dict[int, "UCTNode"] = {}
        self.child_values = np.zeros(shape=(9,), dtype=np.float32)  # 1 you win -1 opp win
        self.child_Average_values = np.zeros(shape=(9,), dtype=np.float32)  # 1 you win -1 opp win
        self.child_visits = np.zeros(shape=(9,), dtype=np.float32)
        self.child_valid = np.ones(shape=(9,), dtype=bool)
        self.end = False  # search end
        self.game_end = False

    @property
    def visits(self):
        if self.parent:
            return self.parent.child_visits[self.action]
        else:
            return np.sum(self.child_visits)

    @visits.setter
    def visits(self, visits):
        self.parent.child_visits[self.action] = visits

    @property
    def value(self):
        if self.parent:
            return self.parent.child_values[self.action]
        else:
            return np.sum(self.child_values)

    @value.setter
    def value(self, value):
        self.parent.child_values[self.action] = value

    def policy(self):
        action_probabilities = self.child_visits * 3
        action_probabilities /= np.sum(action_probabilities)
        return action_probabilities


    def policy_snake(self):
        action_value = np.zeros(9)
        for i in range(9):
            if i in self.children:
                action_value[i] = np.max(self.children[i].policy_snake())
            else:
                action_value[i] = self.child_values[i]
        value = np.zeros(3)
        for i in range(3):
            value[i] = np.sum(np.cbrt(action_value[i * 3:i * 3 + 3])) / 3
        return value

    def policy_snake_test(self):
        action_value = np.zeros(9)
        for i in range(9):
            if i in self.children:
                if self.child_visits[i] <= 1:
                    action_value[i] = self.child_values[i]
                else:
                    action_value[i] = np.max(self.children[i].policy_snake_test())
                    if action_value[i] > 0:
                        action_value[i] -= 0.2
                    if action_value[i] < 0:
                        action_value[i] += 0.2
            else:
                action_value[i] = self.child_values[i]
        value = np.zeros(3)
        for i in range(3):
            if action_value[i * 3] >= 118 and action_value[i * 3 + 1] >= 118 and action_value[i * 3 + 2] >= 118:
                value[i] = (action_value[i * 3] + action_value[i * 3 + 1] + action_value[i * 3 + 2]) / 3
                return value
        for i in range(3):
            if action_value[i] <= -118 and action_value[i + 3] <= -118 and action_value[i + 6] <= -118:
                value[0] = (action_value[i] + action_value[i + 3] + action_value[i + 6]) / 3
                value[1] = value[0]
                value[2] = value[1]
                return value

        # for i in range(3):
        #     values = [action_value[n] for n in [i*3, i*3+1, i*3+2] if self.child_visits[n] != 0]
        #     if len(values) == 0:
        #         value[i] = 0
        #     else:
        #         value[i] = np.mean(values)
        opp_ps = np.zeros(3)
        opp_value = np.zeros(3)

        for j in range(3):
            action_values = [action_value[n] for n in [j, j+3, j+6] if self.child_visits[n] != 0]
            if len(action_values) == 0:
                opp_value[j] = 117
            else:
                opp_value[j] = np.mean(action_values)
            if opp_value[j] > 118:
                opp_value[j] = 0
            else:
                opp_value[j] = (119 - opp_value[j]) * (119 - opp_value[j])


        for i in range(3):
            values = [action_value[n] for n in [i*3, i*3+1, i*3+2] if self.child_visits[n] != 0]
            if len(values) == 0:
                value[i] = 0
            else:
                value[i] = np.mean(values)
        return value


    def policy_snake_power(self):
        action_value = np.zeros(9)
        for i in range(9):
            if i in self.children:
                action_value[i] = np.max(self.children[i].policy_snake_power())
            else:
                action_value[i] = self.child_values[i]
        value = np.zeros(3)
        for i in range(3):
            value[i] = np.sum(np.power(action_value[i * 3:i * 3 + 3], 3)) / 3
        return value


    def __eq__(self, other):
        order = ['state', 'active_player', 'action', 'children', 'num_actions', 'valid_actions', 'child_values',
                 'child_visits', 'parent']
        if isinstance(other, self.__class__):
            own_ordered_self = {k: self.__dict__[k] for k in order}
            own_ordered_other = {k: other.__dict__[k] for k in order}
            return str(own_ordered_self.items()) == str(own_ordered_other.items())
        else:
            return False

    def uct(self, c: float) -> np.ndarray:
        """
        Upper Confidence Bound applied to Trees (UCT)
        Berechnet UCT für alle möglichen Unterknoten und gibt ein numpy-Array der Größe num_actions zurück
        """
        # if np.sum(self.child_visits) == 0:
        #     return np.zeros(9)
        # if self.parent is None:
        #     ln_n = np.log(np.sum(self.child_visits))
        # else:
        #     ln_n = np.log(np.sum(self.parent.child_visits))
        # uct = np.zeros(9)
        # for i in range(9):
        #     if i in self.children:
        #         if self.children[i].end:
        #             uct[i] = -1
        #         else:
        #             w_i = self.child_values[i]
        #             n_i = self.child_visits[i]
        #             uct[i] = (w_i/n_i) + c * np.sqrt(ln_n/n_i)
        #     else:
        #         if self.child_values[i] < 0:
        #             uct[i] = -1
        #         else:
        #             uct[i] = np.inf
        uct = np.zeros(9)
        if np.sum(self.child_visits) == 0:
            for i in range(9):
                if self.child_values[i] != 0:
                    uct[i] = -100
            return uct
        if self.parent is None:
            ln_n = np.log(np.sum(self.child_visits))
        else:
            ln_n = np.log(np.sum(self.parent.child_visits))
        for i in range(9):
            if not self.child_valid[i]:
                uct[i] = -np.inf
            else:
                uct[i] = 100 - self.child_visits[i]
            if i in self.children:
                if self.children[i].end:
                    uct[i] = -np.inf
        return uct

    def select(self, env, c: float = np.sqrt(2)):
        ######
        # TODO Hier Select-Phase aus Aufgabe 2 implementieren
        ######
        uct = self.uct(c)
        best_action_idx = np.argmax(uct)
        if uct[best_action_idx] == -np.inf:
            self.end = True
            return None, None
        # get highest valid action

        if best_action_idx not in self.children:
            current_node = self
        else:
            current_node, best_action_idx = self.children[best_action_idx].select(env, c)
        return current_node, best_action_idx

    def expand(self, env, next_action: int):

        ######
        # TODO Hier Expand-Phase aus Aufgabe 2 implementieren
        ######
        you_alive = True
        opp_alive = True
        env_board_state = copy.deepcopy(env.board)
        env.board = copy.deepcopy(self.state)
        opp_snake = copy.deepcopy(
            [n for n in self.state.get_alive_and_dead_snakes() if n.snake_id != self.active_player][0])
        snack = copy.deepcopy(self.state.get_alive_or_dead_snake_by_id(self.active_player))
        you_new_field = snack.body[0].advanced(snack.possible_actions()[int(next_action / 3)])
        opp_new_field = opp_snake.body[0].advanced(opp_snake.possible_actions()[int(next_action % 3)])
        if you_new_field.x > 10 or you_new_field.x < 0 or you_new_field.y > 10 or you_new_field.y < 0:
            you_alive = False
            self.child_valid[next_action] = False
        else:
            for b in snack.body[:-1]:
                if b.x == you_new_field.x and b.y == you_new_field.y:
                    you_alive = False
                    self.child_valid[next_action] = False
            for b in opp_snake.body[:-1]:
                if b.x == you_new_field.x and b.y == you_new_field.y:
                    you_alive = False
                    self.child_valid[next_action] = False
        if opp_new_field.x > 10 or opp_new_field.x < 0 or opp_new_field.y > 10 or opp_new_field.y < 0:
            opp_alive = False
            self.child_valid[next_action] = False
        else:
            for b in snack.body[:-1]:
                if b.x == opp_new_field.x and b.y == opp_new_field.y:
                    opp_alive = False
                    self.child_valid[next_action] = False
            for b in opp_snake.body[:-1]:
                if b.x == opp_new_field.x and b.y == opp_new_field.y:
                    opp_alive = False
                    self.child_valid[next_action] = False
        if opp_new_field.x == you_new_field.x and opp_new_field.y == you_new_field.y:
            if snack.get_length() <= opp_snake.get_length():
                you_alive = False
            else:
                opp_alive = False

        env.step_action(snack.possible_actions()[int(next_action / 3)],
                        opp_snake.possible_actions()[int(next_action % 3)], self.active_player)
        child = UCTNode(
            boardState=env.board,
            you=snack,
            parent=self,
            action=next_action
        )
        self.children[next_action] = child
        val = BoardControl(env.board, snack)
        env.board = env_board_state
        if not self.child_valid[next_action]:
            return child, val
        if not you_alive:
            child.end = True
            return child, val
        if not opp_alive:
            child.end = True
            return child, val
        return child, val

    def simulate(self, env, timess):
        """
        Simuliert ein zufälliges Spiel

        :param env:
        :return: outcome des Spiels
        """
        start_time = time.time()
        env_board = copy.deepcopy(env.board)
        env.board = copy.deepcopy(self.state)
        while (not env.step()) and (time.time() - start_time) < timess:
            pass
        win = copy.deepcopy(env.board.snakes)
        if (time.time() - start_time) > timess:
            env.board = env_board
            return None
        if len(win) == 0:
            if 0 < env.board.dead_snakes[0].get_length() - env.board.dead_snakes[1].get_length():
                win = copy.deepcopy(env.board.dead_snakes[0].snake_id)
                env.board = env_board
                return win
            if 0 > env.board.dead_snakes[0].get_length() - env.board.dead_snakes[1].get_length():
                win = copy.deepcopy(env.board.dead_snakes[1].snake_id)
                env.board = env_board
                return win
            env.board = env_board
            return None
        env.board = env_board

        return win[0].snake_id

    def backup(self, winner):
        ######
        # TODO Hier Backup-Phase aus Aufgabe 2 implementieren
        ######

        current_node = self
        # iterate over all parent nodes until root node is reached
        while current_node.parent is not None:
            current_node.parent.child_values[current_node.action] += winner
            current_node.parent.child_visits[current_node.action] += 1

            current_node = current_node.parent

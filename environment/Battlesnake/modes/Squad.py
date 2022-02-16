
from typing import Iterator, List, Union, Dict
from collections import defaultdict

from environment.Battlesnake.modes.Standard import StandardGame, CollisionElimination
from environment.Battlesnake.model.EliminationEvent import EliminatedCause, EliminationEvent
from environment.Battlesnake.helper.helper import Helper
from environment.Battlesnake.model.GameInfo import GameInfo
from environment.Battlesnake.model.Snake import Snake
from environment.Battlesnake.model.RulesetSettings import RulesetSettings
from environment.Battlesnake.model.board_state import BoardState

class SquadManager():
    """Collection of allied snakes."""
    def __init__(self, snakes: List[Snake], ruleset_settings: RulesetSettings):
        self.squad_dict = defaultdict(list)
        for snake in snakes:
            self.squad_dict[snake.squad].append(snake)
        self.squads = list(self.squad_dict.values())
        self.rs = ruleset_settings
    
    def __iter__(self) -> Iterator:
        return iter(self.squads)
    
    def get_squad(self, squad: Union[int, List[Snake]]) -> List[Snake]:
        if isinstance(squad, int):
            squad_ = self.squad_dict(squad)
        else:
            squad_ = squad
        return squad_
    
    def is_squad_alive(self, squad: Union[int, List[Snake]]) -> bool:
        squad_ = self.get_squad(squad)
        squad_alive = [snake.is_alive() for snake in squad_]
        if self.rs.squad_sharedElimination:
            return all(squad_alive)
        return any(squad_alive)

    def squad_contains_invalid_length(self, squad: Union[int, List[Snake]]) -> bool:
        squad_ = self.get_squad(squad)
        if self.rs.squad_sharedLength:
            return len(squad_[0].body) <= 0
        return any([len(snake.body) <= 0 for snake in squad_])

    def is_squad_out_of_health(self, squad: Union[int, List[Snake]]) -> bool:
        squad_ = self.get_squad(squad)
        if self.rs.squad_sharedHealth:
            return squad_[0].health <= 0
        return any([snake.health <= 0 for snake in squad_])

    def feed_squad(self, squad: Union[int, List[Snake]], max_health: int, eating_snake: Snake) -> None:
        squad_ = self.get_squad(squad)
        for snake in squad_:
            if len(snake.body) > 0:
                if snake == eating_snake or self.rs.squad_sharedLength:
                    tail = snake.get_tail()
                    snake.body.append(tail)
            if snake == eating_snake or self.rs.squad_sharedHealth:
                snake.health = max_health

    def set_elimination_event(self, squad: Union[int, List[Snake]], event: EliminationEvent, guilty_snake: Union[Snake, str] = None):
        squad_ = self.get_squad(squad)
        for snake in squad_:
            if self.rs.squad_sharedElimination:
                snake.elimination_event = event
            elif not self.rs.squad_sharedHealth and event.cause == EliminatedCause.EliminatedByOutOfHealth:
                if snake.is_alive() and snake.health <= 0:
                    snake.elimination_event = event

        if not self.rs.squad_sharedElimination and guilty_snake is not None:
            if isinstance(guilty_snake, str):
                retrieved_snake = [snake for snake in squad_ if snake.snake_id == guilty_snake][0]
                if retrieved_snake.is_alive():
                    retrieved_snake.elimination_event = event
            elif guilty_snake.is_alive():
                guilty_snake.elimination_event = event



class SquadGame(StandardGame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def ruleset_name():
        return 'squad'

    def maybeEliminateSnakes(self, board: BoardState):
        # First order snake indices by length.
        # In multi-collision scenarios we want to always attribute elimination to the longest snake.
        snakes_by_length = sorted(board.snakes, key=lambda s: len(s.body))
        squads = SquadManager(board.snakes, self.ruleset_settings)

        # First, iterate over all non-eliminated snakes and eliminate the ones
        # that are out of health or have moved out of bounds.
        for squad in squads:
            if not squads.is_squad_alive(squad):
                continue
            
            if squads.squad_contains_invalid_length(squad):
                raise ValueError('snake / squad is length zero')

            if squads.is_squad_out_of_health(squad):
                ee = EliminationEvent(cause=EliminatedCause.EliminatedByOutOfHealth, turn=board.turn, by=None)
                squads.set_elimination_event(squad, ee)
                continue

            for snake in squad:
                if self.snake_is_out_of_bounds(snake, board_width=board.width, board_height=board.height):
                    # snake.eliminated_cause = EliminatedCause.EliminatedByOutOfBounds
                    ee = EliminationEvent(cause=EliminatedCause.EliminatedByOutOfBounds, turn=board.turn, by=None)
                    squads.set_elimination_event(squad, ee, snake)
                    break

        # Next, look for any collisions. Note we apply collision eliminations
        # after this check so that snakes can collide with each other and be properly eliminated.

        collision_eliminations: List[CollisionElimination] = []

        for squad in squads:
            if not squads.is_squad_alive(squad):
                continue

            if squads.squad_contains_invalid_length(squad):
                raise ValueError('snake / squad is length zero')

            

            # Check for body collisions with other snakes second
            has_body_collided = False
            for snake in squad:
                if not snake.is_alive():
                    continue

                # Check for self-collisions first
                if not self.ruleset_settings.squad_allowBodyCollisions and self.snake_has_body_collided(snake, snake):
                    collision_eliminations.append(CollisionElimination(
                        snake_id=snake.snake_id,
                        cause=EliminatedCause.EliminatedBySelfCollision,
                        by=snake.snake_id)) 
                    continue

                for other_snake in snakes_by_length:
                    if snake == other_snake:
                        continue

                    if not other_snake.is_alive():
                        continue

                    if self.snake_has_body_collided(snake, other_snake):
                        collision_eliminations.append(CollisionElimination(
                            snake_id=snake.snake_id,
                            cause=EliminatedCause.EliminatedByCollision,
                            by=other_snake.snake_id))
                        has_body_collided = True
                        break

            if has_body_collided:
                continue

            # Check for head-to-heads last
            has_head_collided = False

            for snake in squad:
                if not snake.is_alive():
                    continue

                for other_snake in snakes_by_length:
                    if snake.snake_id == other_snake.snake_id:
                        continue

                    if not other_snake.is_alive():
                        continue

                    if self.snake_has_lost_head_to_head(snake, other_snake):
                        collision_eliminations.append(CollisionElimination(
                            snake_id=snake.snake_id,
                            cause=EliminatedCause.EliminatedByHeadToHeadCollision,
                            by=other_snake.snake_id))
                        has_head_collided = True
                        break

            if has_head_collided:
                continue

        # Apply collision eliminations
        for elimination in collision_eliminations:
            for squad in squads:
                if elimination.snake_id in squad:
                    ee = EliminationEvent(cause=elimination.cause, turn=board.turn, by=elimination.by)
                    squads.set_elimination_event(squad, ee, elimination.snake_id)
                    break


    def snake_has_body_collided(self, s: Snake, other: Snake):
        # Allied snakes bodies (not heads) are allowed to overlap in squad mode

        if self.ruleset_settings.squad_allowBodyCollisions and s.squad == other.squad:
            return False

        return super().snake_has_body_collided(s, other)
    
    def maybeFeedSnakes(self, board: BoardState):
        # All allied snakes benefit from food in squad mode. Only one food per turn though
        food_not_eaten = []
        squads = SquadManager(board.snakes, self.ruleset_settings)
        for f in board.food:

            food_has_been_eaten = False
            for squad in squads:

                # Ignore eliminated and zero-length snakes, they can't eat.
                if not squads.is_squad_alive(squad) or squads.squad_contains_invalid_length(squad):
                    continue
                
                squad_has_eaten = False
                for snake in squad:
                    head = snake.get_head()
                    if head.is_position_equal_to(f):
                        # Squad can only grow once per turn
                        if not squad_has_eaten:
                            squads.feed_squad(squad, self.snake_max_health, snake)
                            if self.ruleset_settings.squad_sharedLength and self.ruleset_settings.squad_sharedHealth:
                                squad_has_eaten = True
                        food_has_been_eaten = True

            if not food_has_been_eaten:
                food_not_eaten.append(f)
                
        board.food = food_not_eaten
    
    def is_game_over(self, board: BoardState) -> bool:
        num_squads_remaining = 0
        squads = SquadManager(board.snakes, self.ruleset_settings)
        for squad in squads:
            if squads.is_squad_alive(squad):
                num_squads_remaining += 1
        return num_squads_remaining <= 1
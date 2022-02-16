from enum import Enum


class SnakeStatus(Enum):
    Alive = 0,
    KilledHeadOnHead = 1,
    KilledEnemyBody = 2,
    KilledStarvation = 3,
    KilledOwnBody = 4,
    KilledWall = 5


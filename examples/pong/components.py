from pygame.sprite import Sprite

from consts import Team
from pyved import component


@component
class ComVisible:
    sprite: Sprite
    x: int
    y: int


@component
class ComMotion:
    speed_x: int
    speed_y: int


@component
class ComScore:
    score: int


@component
class ComTeam:
    team: int

    def __post_init__(self):
        assert self.team in Team.values, 'team value not in Team.values'


@component
class ComWait:
    wait_ms: int

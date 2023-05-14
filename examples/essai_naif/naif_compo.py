from typing import Iterable

import pyved
from pyved import component, entity


pygame = pyved.pygame_proxy()


@component
class Repr2d:
    image: pygame.Surface


@component
class Position:
    x: int
    y: int


@component
class Speed:
    vx: float
    vy: float


@component
class Health:
    max_hp: int
    hp: int
    num_lives: int


@component
class Perks:
    li_perks: Iterable[str]


@component
class MessagingCompo:
    ev_listener: int  # object
    ev_buffer: list

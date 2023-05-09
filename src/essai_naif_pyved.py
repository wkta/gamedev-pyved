from typing import Iterable

import pygame

import pyved as pyv


@pyv.component
class Position:
    x: int
    y: int


@pyv.component
class Speed:
    vx: float
    vy: float


@pyv.component
class Health:
    max_hp: int
    hp: int


@pyv.component
class Perks:
    li_perks: Iterable[str]


# --- def entités ---
@pyv.entity
class Player(Health, Perks, Position, Speed):
    pass


# programme principal

t = Player(
    x=0, y=256, max_hp=125, hp=None, li_perks=['toughGuy', 'kamikaze'],
    vx=0.0, vy=0.0
)

print(t)


# SysInit(entities),
# SysControl(entities, pygame.event.get),
# SysMovement(entities),
# SysRoundStarter(entities, clock),
# SysGoal(entities),
# SysDraw(entities, screen),


class SysInput(pyv.System):
    def __init__(self, entities):
        self.gameover = False
        self.entities = entities

    def proc(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.gameover = True

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.gameover = True
                elif ev.key == pygame.K_UP:
                    pl_obj = next(self.entities.get_by_class(Player))
                    pl_obj.vy = -1.845
                elif ev.key == pygame.K_DOWN:
                    pl_obj = next(self.entities.get_by_class(Player))
                    pl_obj.vy = +1.744

            elif ev.type == pygame.KEYUP:
                tmp = pygame.key.get_pressed()
                if not tmp[pygame.K_DOWN] and not tmp[pygame.K_UP]:
                    pl_obj = next(self.entities.get_by_class(Player))
                    pl_obj.vy = 0


class SysEntityMover(pyv.System):
    def __init__(self, ent):
        self.entities = ent

    def proc(self):
        pl_obj = next(self.entities.get_by_class(Player))
        if pl_obj.vx != 0.0:
            pl_obj.x += pl_obj.vx
        if pl_obj.vy != 0.0:
            pl_obj.y += pl_obj.vy


class SysGraphicalRepr(pyv.System):
    def __init__(self, entities, screen):
        self.entities = entities
        self.screen = screen

    def proc(self):
        self.screen.fill('antiquewhite2')
        pl_obj = next(self.entities.get_by_class(Player))
        pygame.draw.circle(self.screen, 'red', (pl_obj.x, pl_obj.y), 8)
        # for visible_entity in self.entities.get_by_class(Table, Score, Ball, Racket, Spark):
        #    self.screen.blit(visible_entity.sprite.image, (visible_entity.x, visible_entity.y))


# ---
def run_game():
    pygame.init()  # init all imported pygame modules
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode((800, 500))  # w h
    clock = pygame.time.Clock()

    entities_mger = pyv.EntityManager()
    entities_mger.add(
        t
    )

    system_manager = pyv.SystemManager([
        SysInput(entities_mger),
        SysEntityMover(entities_mger),
        SysGraphicalRepr(entities_mger, screen)
    ])

    system_manager.init_all()

    # game_state_info: GameStateInfo = next(entities.get_by_class(GameStateInfo))
    # while game_state_info.play:
    #    clock.tick_busy_loop(60)  # tick_busy_loop точный + ест проц, tick грубый + не ест проц
    #    system_manager.update_systems()
    #    pygame.display.flip()  # draw changes on screen

    while not system_manager['SysInput'].gameover:
        system_manager.proc_all()
        pygame.display.flip()
        clock.tick_busy_loop(60)

    system_manager.cleanup_all()
    print('All Systems stopped')


run_game()

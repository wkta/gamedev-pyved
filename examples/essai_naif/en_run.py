import pygame
import pyved as pyv
from naif_entities import Player, PlayersEvListener, HudScore, HudEvListener
from en_systems import SysInput, SysEvent, SysEntityMover, SysGraphicalRepr, SysGamestate
import ndefs
import naif_util


def run_game():
    pyv.init()  # init all imported pygame modules
    pyv.get_ev_manager().setup(ndefs.MyEvTypes)

    # --- init PLAYER
    player_2drepr = pygame.surface.Surface((32, 32))
    player_2drepr.fill((255, 0, 255))
    pygame.draw.circle(player_2drepr, 'pink', (16, 16), 15)
    player_2drepr.set_colorkey((255, 0, 255))

    pl_obj = Player(
        image=player_2drepr,
        num_lives=3,
        x=0, y=256, max_hp=125, hp=100, li_perks=['toughGuy', 'kamikaze'],
        vx=0.0, vy=0.0,
        ev_buffer=[], ev_listener=PlayersEvListener().bind()
    )
    print(pl_obj)

    # --- init HUD
    hud = HudScore(
        x=380, y=16,
        image=naif_util.font_render(f'#Lives = {pl_obj.num_lives}'),
        ev_buffer=[], ev_listener=HudEvListener().bind()
    )

    pygame.display.set_caption('Pong')
    screen = pyv.get_surface()  # pygame.display.set_mode((800, 500))  # w h
    clock = pygame.time.Clock()

    entities_mger = pyv.EntityManager()
    entities_mger.add(
        pl_obj, hud
    )

    gs = SysGamestate(entities_mger)
    system_manager = pyv.SystemManager([
        gs,
        SysInput(entities_mger, gs),
        SysEvent(entities_mger),
        SysEntityMover(entities_mger),
        SysGraphicalRepr(entities_mger, screen)
    ])

    system_manager.init_all()

    # game_state_info: GameStateInfo = next(entities.get_by_class(GameStateInfo))
    # while game_state_info.play:
    #    clock.tick_busy_loop(60)  # tick_busy_loop точный + ест проц, tick грубый + не ест проц
    #    system_manager.update_systems()
    #    pygame.display.flip()  # draw changes on screen

    while not gs.gameover:
        system_manager.proc_all()
        pyv.flip()
        clock.tick_busy_loop(60)

    system_manager.cleanup_all()
    print('All Systems stopped')


run_game()

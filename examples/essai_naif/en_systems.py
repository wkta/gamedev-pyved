import ndefs
import pyved as pyv
from naif_compo import MessagingCompo, Position, Repr2d
from naif_entities import Player


pygame = pyv.pygame_proxy()
# SysInit(entities),
# SysControl(entities, pygame.event.get),
# SysMovement(entities),
# SysRoundStarter(entities, clock),
# SysGoal(entities),
# SysDraw(entities, screen),


class SysEvent(pyv.System):
    def __init__(self, entities):
        self.gameover = False
        self.entities = entities

    def initialize(self):
        for pubsub_entity in self.entities.get_with_component(MessagingCompo):
            listener_id = pubsub_entity.ev_listener
            li_obj = pyv.EvListener.lookup(listener_id)
            li_obj.parent = pubsub_entity  # can the parent entity back!
            li_obj.turn_on()

    def proc(self):
        GlEvManager = pyv.get_ev_manager()

        # push events down the queue
        for pubsub_entity in self.entities.get_with_component(MessagingCompo):
            while len(pubsub_entity.ev_buffer) > 0:
                p = pubsub_entity.ev_buffer.pop()
                print('posting event type:', p[0])
                GlEvManager.post(p[0], **p[1])

        # proc all callbacks
        GlEvManager.update()

    def quit(self):
        for pubsub_entity in self.entities.get_with_component(MessagingCompo):
            listener_id = pubsub_entity.ev_listener
            li_obj = pyv.EvListener.lookup(listener_id)
            li_obj.turn_off()


class SysGamestate(pyv.System):
    def __init__(self, ent):
        self.entities = ent
        self.gameover = False


class SysInput(pyv.System):
    def __init__(self, entities, gs):
        self.entities = entities
        self.gs = gs

    def proc(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.gs.gameover = True

            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.gs.gameover = True

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    pl_obj = next(self.entities.get_by_class(Player))
                    pl_obj.vy = -1.845
                    return

                if ev.key == pygame.K_DOWN:
                    pl_obj = next(self.entities.get_by_class(Player))
                    pl_obj.vy = +1.744
                    return

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

        # detection of death
        if pl_obj.y <= 60 and pl_obj.hp > 0:
            pl_obj.ev_buffer.append(
                (ndefs.MyEvTypes.PlayerDies, {'hp_val': pl_obj.hp})
            )
            pl_obj.num_lives -= 1
            pl_obj.ev_buffer.append(
                (ndefs.MyEvTypes.LivesChange, {'num_lives': pl_obj.num_lives})
            )


class SysGraphicalRepr(pyv.System):
    def __init__(self, entities, screen):
        self.entities = entities
        self.screen = screen

    def proc(self):
        self.screen.fill('antiquewhite2')
        for game_entity in self.entities.get_with_component(Position, Repr2d):
            self.screen.blit(game_entity.image, (game_entity.x, game_entity.y))

        # pl_obj = next(self.entities.get_by_class(Player))
        # pygame.draw.circle(self.screen, 'red', (pl_obj.x, pl_obj.y), 8)

        # for visible_entity in self.entities.get_by_class(Table, Score, Ball, Racket, Spark):
        #    self.screen.blit(visible_entity.sprite.image, (visible_entity.x, visible_entity.y))

    def cleanup(self):
        pyv.quit()

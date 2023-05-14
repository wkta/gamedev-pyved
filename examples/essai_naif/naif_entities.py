"""
  DEF of entities + "reactions"
"""
from naif_compo import *
import naif_util


class PlayersEvListener(pyved.EvListener):
    def __init__(self):
        super().__init__()
        self.parent = None  # will be set from outside

    def on_player_dies(self, ev):
        print(' --> Reception player dies, hp_val=', ev.hp_val)
        self.parent.hp = -1
        print('nouvelle valeur', self.parent, self.parent.hp)


@entity
class Player(Position, Repr2d, MessagingCompo, Health, Perks,  Speed):
    pass


class HudEvListener(pyved.EvListener):
    def __init__(self):
        super().__init__()
        self.parent = None  # will be set from outside

    def on_lives_change(self, ev):
        self.parent.image = naif_util.font_render(f'#Lives = {ev.num_lives}')
        print('hud re-drawn ->yes!')


@entity
class HudScore(Position, Repr2d, MessagingCompo):
    pass

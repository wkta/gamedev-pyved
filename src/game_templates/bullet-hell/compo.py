import katagames_engine as kengi


_Listener = kengi.event2.EvListener


class BhCtrl(_Listener):
    def __init__(self, refview, gameref):
        super().__init__()
        self._v = refview
        self._g = gameref
        self._currdir = None
        self._cpt = 0

    def _trigger_visual_change(self):
        self._v.curr_idx = (self._v.curr_idx + 1) % self._v.sprsheet_a.card
        self._v.curr_idx_b = (self._v.curr_idx_b + 1) % self._v.sprsheet_b.card

    def on_gamepad_dir(self, ev):
        # this could work:
        # -
        # self._currdir = {
        #     'north': (+0, -1),
        #     'east':  (+1,  0),
        #     'west':  (-1,  0),
        #     'south': (+0, +1),
        #
        #     'south-west': (-1, +1),
        #     'south-east': (+1, +1),
        #     'north-east': (+1, -1),
        #     'north-west': (-1, -1),
        #     None: None
        # }[ev.dir]

        # this solution might be better, it depends on your particular needs!
        # -
        if (not ev.value[0]) and (not ev.value[1]):
            self._currdir = None
        else:
            self._currdir = ev.value

    def on_update(self, ev):
        if self._currdir:
            if self._cpt > 25:
                a, b = self._currdir
                self._v.blitpos[0] += a * self._v.MOV_INCREM
                self._v.blitpos[1] += b * self._v.MOV_INCREM
                self._cpt = -1
            self._cpt += 1

    def on_keydown(self, ev):
        self._trigger_visual_change()

    def on_gamepaddown(self, ev):
        self._trigger_visual_change()

    def on_quit(self, ev):
        self._g.gameover = True


class BhView(_Listener):
    MOV_INCREM = 8

    def __init__(self):
        super().__init__()
        self.sprsheet_a = kengi.gfx.Spritesheet('topdown-shooter-sprsheet.png')
        self.sprsheet_a.set_infos((32, 32))

        self.sprsheet_b = kengi.gfx.Spritesheet('topdown-shooter-sprsheet.png')
        self.sprsheet_b.set_infos((16, 16))
        self.curr_idx = self.curr_idx_b = 0
        self.blitpos = [0, 0]

    def on_paint(self, ev):
        ev.screen.fill('orange')
        ev.screen.blit(self.sprsheet_a[self.curr_idx], self.blitpos)
        ev.screen.blit(self.sprsheet_b[self.curr_idx_b], (48, 48))

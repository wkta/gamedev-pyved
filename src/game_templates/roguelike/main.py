import pyved_engine as kengi
kengi.bootstrap_e()


from MazeninjaCompo import NinjamazeMod, NinjamazeView, NinjamazeCtrl, MyEvTypes


def print_tuto():
    print('\n' + '*'*32)
    print('This example showcases capabilities of the kengi.rogue')
    print('submodule... You can easily generate a RANDOM MAZE')
    print('you can also use a field-of-view generic algorithm')
    print('to simulate the "fog of war"/unknown parts of the map.')
    print('>>CONTROLS<< SPACE to regen maze | ESCAPE to quit\n' + '*'*32)


if __name__ == '__main__':
    kengi.init()
    kengi.get_ev_manager().setup(MyEvTypes)

    m = NinjamazeMod()
    NinjamazeView(m).turn_on()
    NinjamazeCtrl(m).turn_on()
    print_tuto()
    gctrl = kengi.get_game_ctrl()
    gctrl.turn_on()
    gctrl.loop()

    kengi.quit()
    print('bye!')

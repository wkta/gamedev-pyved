import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage
from pygame_gui import UIManager, UI_TEXT_ENTRY_CHANGED
from pygame_gui.elements import UIWindow, UITextEntryBox, UITextBox

from .pong.pong import PongGame

import os  # so i can open file to read src code!


PONG_WINDOW_SELECTED = pygame.event.custom_type()


APP_W, APP_H = 1380, 800
KTG_W, KTG_H = 960, 720
# ktg sont les dim. d'un jeu
POS_PREVIEW = (200, 0)

target_dir = None
target_file = None


class PongWindow(UIWindow):
    def __init__(self, gamename, position, ui_manager):
        super().__init__(pygame.Rect(position, (KTG_W+32, KTG_H+59)), ui_manager,
                         window_display_title=gamename,
                         object_id='#pong_window',
                         draggable=False)

        game_surface_size = self.get_container().get_size()
        print('surf pour affichage jeu:', game_surface_size)

        self.game_surface_element = UIImage(pygame.Rect((0, 0),
                                                        game_surface_size),
                                            pygame.Surface(game_surface_size).convert(),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)

        self.pong_game = PongGame()
        self.is_active = False

    def process_event(self, event):
        handled = super().process_event(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == "#pong_window.#title_bar" and
                event.ui_element == self.title_bar):
            handled = True
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            window_selected_event = pygame.event.Event(PONG_WINDOW_SELECTED,
                                                       event_data)
            pygame.event.post(window_selected_event)
        if self.is_active:
            handled = self.pong_game.process_event(event)
        return handled

    def update(self, time_delta):
        if self.alive() and self.is_active:
            self.pong_game.update(time_delta)

        super().update(time_delta)

        self.pong_game.draw(self.game_surface_element.image)


class MiniGamesApp:
    def __init__(self):
        pygame.init()

        self.root_window_surface = pygame.display.set_mode((APP_W, APP_H))

        self.background_surface = pygame.Surface((APP_W, APP_H)).convert()
        self.background_surface.fill(pygame.Color('#505050'))
        self.ui_manager = UIManager((APP_W, APP_H), 'data/themes/theme_3.json')
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.pong_window_1 = PongWindow(
            'Pong demo',
            POS_PREVIEW,
            self.ui_manager
        )
        # self.pong_window_2 = PongWindow((50, 50), self.ui_manager)
        self.pong_window_1.is_active = True

        # - text related stuff
        notepad_window = UIWindow(pygame.Rect(50, 20, 300, 400), window_display_title="Pygame Notepad")
        output_window = UIWindow(pygame.Rect(400, 20, 300, 400), window_display_title="Pygame GUI Formatted Text")

        # swap to editable text box
        self.text_entry_box = UITextEntryBox(
                relative_rect=pygame.Rect((0, 0), notepad_window.get_container().get_size()),
                initial_text="",
                container=notepad_window)

        self.text_output_box = UITextBox(
                relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
                html_text="",
                container=output_window)
        if target_dir is not None:
            thefile = os.path.join(target_dir, target_file)
            with open(thefile, 'r') as fptr:
                self.text_entry_box.set_text(fptr.read())

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.ui_manager.process_events(event)

                if event.type == PONG_WINDOW_SELECTED:
                    event.ui_element.is_active = True
##                    if event.ui_element == self.pong_window_1:
##                        self.pong_window_2.is_active = False
##                    elif event.ui_element == self.pong_window_2:
##                        self.pong_window_1.is_active = False
                elif event.type == UI_TEXT_ENTRY_CHANGED and event.ui_element == self.text_entry_box:
                    self.text_output_box.set_text(event.text)

            self.ui_manager.update(time_delta)

            self.root_window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.root_window_surface)

            pygame.display.update()


def run_editor():
    app = MiniGamesApp()
    app.run()

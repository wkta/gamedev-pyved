import pyved


pygame = pyved.pygame_proxy()
_font_obj = None


def font_render(txt):
    global _font_obj
    if _font_obj is None:
        _font_obj = pygame.font.Font(None, 18)
    return _font_obj.render(txt, False, 'red')

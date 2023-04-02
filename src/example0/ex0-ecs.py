
import pygame
import sys


class Entity:
    def __init__(self):
        self.components = []
        self.systems = []

    def add_component(self, component):
        for component_ in self.components:
            if isinstance(component_, type(component)):
                print('Entity already has component')
                return

        self.components.append(component)

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component

        print('No component found')  # raise error instead?
        return

    def has_component(self, component):
        for component_ in self.components:
            if isinstance(component_, type(component)):
                return True
        return False

    def add_system(self, system):
        for system_ in self.systems:
            if isinstance(system_, type(system)):
                print('Entity already has system')
                return
        self.systems.append(system)

    def get_system(self, system):
        for system_ in self.systems:
            if isinstance(system_, system):
                return system_
        return None


class PositionComponent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y


class MovementComponent:
    def __init__(self, speed):
        self.direction = pygame.math.Vector2()
        self.speed = speed


class RectComponent:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class SpriteComponent:
    def __init__(self, image_file, width, height, x_start, y_start, scale=1):
        self.sprite_sheet = pygame.image.load(image_file).convert_alpha()
        self.image = self.load_image(width, height, x_start, y_start, scale)

    def load_image(self, width, height, x_start, y_start, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite_sheet = self.sprite_sheet
        image.blit(sprite_sheet, (0, 0), (x_start, y_start, width, height))
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        return image


class DirectionComponent:
    def __init__(self, init_direction: str):
        self.directions = ['up', 'down', 'left', 'right']
        if init_direction.lower() not in self.directions:
            init_direction = 'right'

        self.direction = init_direction


class StatusComponent:
    def __init__(self):
        self.status = 'idle'


class StatusSystem:
    def __init__(self, entity):
        self.entity = entity

    @property
    def status(self):
        direction_component: DirectionComponent = self.entity.get_component(DirectionComponent)
        status_component: StatusComponent = self.entity.get_component(StatusComponent)
        return f'{direction_component.direction}_{status_component.status}'

    def run(self):
        return


class AnimationComponent:
    def __init__(self, animation_speed):
        self.animation_speed = animation_speed
        self.animation_index = 0
        self.animations = {}

    def add_animation(self, required_status: str, animation_sprites: list[pygame.Surface]):
        if required_status not in self.animations.keys():
            self.animations[required_status] = animation_sprites
        else:
            print('required status already in use')  # raise error instead?
            return


class DrawSpriteSystem:
    def __init__(self, entity, screen_surface):
        self.screen_surface = screen_surface
        self.entity = entity

    def run(self):
        sprite_component: SpriteComponent = self.entity.get_component(SpriteComponent)
        position_component: PositionComponent = self.entity.get_component(PositionComponent)
        sprite = sprite_component.image

        self.screen_surface.blit(sprite, (position_component.get_pos()))


class AnimationSystem:
    def __init__(self, entity):
        self.entity = entity

    def run(self):
        status_system: StatusSystem = self.entity.get_system(StatusSystem)
        status = status_system.status

        animation_component: AnimationComponent = self.entity.get_component(AnimationComponent)
        animations = animation_component.animations
        animation = animations[status]
        animation_index = animation_component.animation_index
        animations_speed = animation_component.animation_speed

        sprite_component: SpriteComponent = self.entity.get_component(SpriteComponent)

        animation_component.animation_index = animation_index + animations_speed
        if animation_component.animation_index >= len(animation):
            animation_component.animation_index = 0

        sprite_component.image = animation[int(animation_component.animation_index)]


class MovementSystem:
    def __init__(self, entity):
        self.entity = entity

    def run(self):
        position_component: PositionComponent = self.entity.get_component(PositionComponent)
        movement_component: MovementComponent = self.entity.get_component(MovementComponent)
        rect_component: RectComponent = self.entity.get_component(RectComponent)

        if movement_component.direction.magnitude() != 0:
            movement_component.direction = movement_component.direction.normalize()

        position_component.x += movement_component.direction.x * movement_component.speed
        position_component.y += movement_component.direction.y * movement_component.speed

        rect_component.rect.x = position_component.x
        rect_component.rect.y = position_component.y


class InputSystem:
    def __init__(self, entity):
        self.entity = entity
        self.actions = {}

    def run(self):
        keys_pressed = pygame.key.get_pressed()

        self.entity.get_component(StatusComponent).status = 'idle'

        # Vertical
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.entity.get_component(MovementComponent).direction.y = -1
            self.entity.get_component(DirectionComponent).direction = 'up'
            self.entity.get_component(StatusComponent).status = 'walking'

        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.entity.get_component(MovementComponent).direction.y = 1
            self.entity.get_component(DirectionComponent).direction = 'down'
            self.entity.get_component(StatusComponent).status = 'walking'

        else:
            self.entity.get_component(MovementComponent).direction.y = 0

        # Horizontal
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.entity.get_component(MovementComponent).direction.x = -1
            self.entity.get_component(DirectionComponent).direction = 'left'
            self.entity.get_component(StatusComponent).status = 'walking'

        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.entity.get_component(MovementComponent).direction.x = 1
            self.entity.get_component(DirectionComponent).direction = 'right'
            self.entity.get_component(StatusComponent).status = 'walking'

        else:
            self.entity.get_component(MovementComponent).direction.x = 0


class Player(Entity):
    def __init__(self):
        super(Player, self).__init__()

        # -- System Init
        self.add_system(MovementSystem(self))
        self.add_system(InputSystem(self))
        self.add_system(DrawSpriteSystem(self, screen))
        self.add_system(StatusSystem(self))
        self.add_system(AnimationSystem(self))

        # -- Component Init
        self.add_component(PositionComponent(640, 360))
        self.add_component(MovementComponent(7))
        self.add_component(RectComponent(640, 360, 48, 96))
        self.add_component(SpriteComponent('mystic_woods_free_v0.2/sprites/characters/player.png',
                                           16, 16 * 2, 16, 16, scale=3))
        self.add_component(DirectionComponent('right'))
        self.add_component(StatusComponent())
        self.add_component(AnimationComponent(0.15))

        self.get_animations()

    def get_animations(self):
        sprite_component: SpriteComponent = self.get_component(SpriteComponent)
        sprite_sheet = sprite_component.sprite_sheet

        right_idle = []
        left_idle = []
        left_walking = []
        right_walking = []

        down_idle = []
        down_walking = []
        up_idle = []
        up_walking = []

        # Left & Right Idle
        for i in range(16, 257, 48):
            image = pygame.Surface((16, 16 * 2), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (i, 64, 16, 16 * 2))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))

            right_idle.append(image)
            left_idle.append(pygame.transform.flip(image, True, False))

        # Left & Right Walking
        for i in range(16, 257, 48):
            image = pygame.Surface((16, 16 * 2), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (i, 208, 16, 16 * 2))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))

            right_walking.append(image)
            left_walking.append(pygame.transform.flip(image, True, False))

        # Down Idle
        for i in range(16, 257, 48):
            image = pygame.Surface((16, 16 * 2), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (i, 16, 16, 16 * 2))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))

            down_idle.append(image)

        # Down Walking
        for i in range(16, 257, 48):
            image = pygame.Surface((16, 16 * 2), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (i, 160, 16, 16 * 2))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))

            down_walking.append(image)

        # Up Idle
        for i in range(16, 257, 48):
            image = pygame.Surface((16, 16 * 2), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (i, 112, 16, 16 * 2))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))

            up_idle.append(image)

        # Up Walking
        for i in range(16, 257, 48):
            image = pygame.Surface((16, 16 * 2), pygame.SRCALPHA)
            image.blit(sprite_sheet, (0, 0), (i, 256, 16, 16 * 2))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))

            up_walking.append(image)

        animation_component: AnimationComponent = self.get_component(AnimationComponent)
        animation_component.add_animation('right_idle', right_idle)
        animation_component.add_animation('left_idle', left_idle)
        animation_component.add_animation('right_walking', right_walking)
        animation_component.add_animation('left_walking', left_walking)

        animation_component.add_animation('up_idle', up_idle)
        animation_component.add_animation('down_idle', down_idle)
        animation_component.add_animation('up_walking', up_walking)
        animation_component.add_animation('down_walking', down_walking)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill('#555358')
    clock = pygame.time.Clock()

    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.get_system(InputSystem).run()
        player.get_system(AnimationSystem).run()

        # screen refresh
        screen.fill('#555358')
        player.get_system(DrawSpriteSystem).run()

        player.get_system(MovementSystem).run()
        pygame.draw.rect(screen, 'red', player.get_component(RectComponent).rect, 2)

        pygame.display.update()
        clock.tick(60)

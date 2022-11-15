import pygame
pygame.init()
pygame.font.init()

#font setup
default_font = "freesansbold.ttf"
def get_font(size, font = default_font):
    return pygame.font.Font(font, size)


screens = {}
def get_screens():
    return screens

class text(pygame.sprite.Sprite):
    def __init__(self, text_content, color, pos, font):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.font = font
        self.text_content = text_content
        self.surf = self.font.render(self.text_content, True, color)
        self.rect = self.surf.get_rect(center=pos)

    def update_text(self, updated_text):
        self.text_content = updated_text
        self.surf = self.font.render(text, self.text_content, self.color)

    def update_pos(self, pos):
        self.rect = self.surf.get_rect(center=pos)
        self.update_text(self.text_content)

class screen:
    def __init__(self, screen_name, init_func, load_func, update_func):
        self.screen_name = screen_name
        self.init_func = init_func #runs once
        self.load_func = load_func #runs at the start when a screen is switched to
        self.update_func = update_func # runs every frame

        screens[self.screen_name] = self

        self.init_func()
        self.load_func()

    def update(self):
        return self.update_func()
    
    def load(self):
        self.load_func()

class button(pygame.sprite.Sprite):
    def __init__(self, text, position=None, size=None, rect=None, bg_color = (255,255,255), text_color=(0,0,0), on_hover=None, on_press=None, on_click=None):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.position = position
        self.size = size

        self.state = "not_pressed"

        if rect:
            self.rect = rect
        else:
            self.rect = pygame.rect((position[0] + size[0]/2, position[1] + size[1]/2),(size[1], size[1],))

        self.surf = pygame.Surface((self.rect.w, self.rect.h))

        self.bg_color = bg_color
        self.text_color = text_color

        self.on_hover = on_hover
        self.on_press = on_press
        self.on_click = on_click

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_click:
                if self.state == "not_pressed":
                    if self.on_click:
                        self.on_click()
                    self.state = "clicked"
                else:
                    if self.on_press:
                        self.on_press()
                    self.state = "pressed"
            else:
                if self.on_hover:
                    self.on_hover()
                self.state = "not_pressed"
        else:
            self.state = "not_pressed"

        return self.state
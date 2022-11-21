import pygame
pygame.init()
pygame.font.init()

# font setup
default_font = "freesansbold.ttf" # set this to the font that we want
# easier way to get fonts
def get_font(size, font = default_font):
    return pygame.font.Font(font, size)


screens = {} # stores all the screens and their names
def get_screens(): # returns the screens dict
    return screens


class screen: # class for managing differnt screens
    def __init__(self, screen_name, init_func, load_func, update_func):
        self.screen_name = screen_name
        self.init_func = init_func #runs once
        self.load_func = load_func #runs at the start when a screen is switched to
        self.update_func = update_func # runs every frame

        screens[self.screen_name] = self # add to the screens dict

        self.init_func() # run the init function

    # call update_func
    def update(self):
        return self.update_func()
    
    # call load_func
    def load(self):
        self.load_func()

class text(pygame.sprite.Sprite): # class for easier text creation
    def __init__(self, text_content, pos, color=(255,255,255), font=get_font(20), group = None):
        pygame.sprite.Sprite.__init__(self) # inherits the pygame sprite class
        self.color = color
        self.font = font

        self.update_text(text_content)
        self.rect = self.surf.get_rect(center=pos) # convert position into a rect

        self.group = group
        if self.group != None:
            self.group.add(self)

    # changes the text if needed
    def update_text(self, updated_text):
        self.text_content = updated_text
        self.text_size = self.font.size(updated_text)
        self.surf = self.font.render(self.text_content, False, self.color)

    # changes the pos if needed
    def update_pos(self, pos):
        self.rect = self.surf.get_rect(center=pos)
        self.update_text(self.text_content)

class button(pygame.sprite.Sprite): # easier button creation
    def __init__(self, text_content, position=None, size=None, rect=None, bg_color = (100,100,100), text_color=(0,0,0), on_hover=None, on_press=None, on_click=None, group = None):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.size = size

        self.state = "not_pressed" 

        if rect:
            self.rect = rect # used rect if provided
        else:
            self.rect = pygame.rect((position[0] + size[0]/2, position[1] + size[1]/2),(size[1], size[1],)) # creates one otherwise

        self.bg_color = bg_color
        self.text_color = text_color

        self.text_content = text_content
        self.text_sprite = text(text_content, (0,0), color=self.text_color) # uses text class to render the text

        self.draw_surf()

        self.on_hover = on_hover # runs when hovered
        self.on_press = on_press # runs when pressed
        self.on_click = on_click # runs when clicked

        self.group = group
        if self.group != None:
            self.group.add(self)
    
    def draw_surf(self):
        self.surf = pygame.Surface((self.rect.w, self.rect.h)) # creates button surface based on the rect
        self.surf.fill(self.bg_color) # fills in the bg color
        
        text_w, text_h = self.text_sprite.text_size
        self.surf.blit(self.text_sprite.surf, (self.rect.w/2-text_w/2, self.rect.h/2-text_h/2))

    def update_text(self, text_content):
        self.text_content = text_content
        self.text_sprite.update_text(text_content)
        self.draw_surf()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos() # get variable storing the mouse position
        mouse_click = pygame.mouse.get_pressed()[0] # get varible storing if the mouse was clicked

        if self.rect.collidepoint(mouse_pos):
            if mouse_click:
                if self.state == "hovered":
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
                self.state = "hovered"
        else:
            self.state = "not_pressed"

        return self.state
    
class slider(pygame.sprite.Sprite): # easier button creation
    def __init__(self, rect, slider_min, slider_max, slider_length, text_content="", bg_color=(100,100,100), text_color=(0,0,0), slider_color=(255,255,255), knob_color=(255,0,0), group=None, default_value=None):
        pygame.sprite.Sprite.__init__(self)

        self.rect = rect # used rect if provided
        self.value = default_value

        self.slider_min = slider_min
        self.slider_max = slider_max
        self.slider_length = slider_length

        self.bg_color = bg_color
        self.text_color = text_color
        self.slider_color = slider_color
        self.knob_color = knob_color

        self.text_content = text_content
        self.text_sprite = text(text_content, (0,0), color=self.text_color) # uses text class to render the text

        text_w, text_h = self.text_sprite.text_size
        self.text_pos = (self.rect.w/2-text_w/2, self.rect.h*0.25-text_h/2)

        self.slider_rect = pygame.Rect(0, 0, self.slider_length, 15)
        self.slider_rect.center = (self.rect.w/2, self.rect.h*0.60)

        self.knob_rect = pygame.Rect(0, 0, 15, 15)

        self.draw_surf()
        self.get_knob_value(self.value)

        self.group = group
        if self.group != None:
            self.group.add(self)
    
    def draw_surf(self):
        self.surf = pygame.Surface((self.rect.w, self.rect.h)) # creates button surface based on the rect
        self.surf.fill(self.bg_color) # fills in the bg color

        self.surf.blit(self.text_sprite.surf, self.text_pos)
        pygame.draw.rect(self.surf, self.slider_color, self.slider_rect)

    def get_knob_value(self, value=None):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        mouse_x = mouse_pos[0] - self.rect.x
        mouse_y = mouse_pos[1] - self.rect.y

        #print(mouse_x, mouse_y, self.knob_rect)
        if not mouse_click or not self.slider_rect.collidepoint((mouse_x, mouse_y)):
            return self.value
        
        knob_x = max(self.slider_rect.left, min(self.slider_rect.right, mouse_x))

        self.knob_rect.center = (knob_x, self.slider_rect.centery)
        self.draw_surf() # can be optomized
        pygame.draw.rect(self.surf, self.knob_color, self.knob_rect)

        self.value = (knob_x-25/self.slider_length) * (self.slider_max - self.slider_min)
        return self.value

    def update_text(self, text_content):
        self.text_content = text_content
        self.text_sprite.update_text(text_content)

    def slider_update(self):
        mouse_pos = pygame.mouse.get_pos() # get variable storing the mouse position
        mouse_click = pygame.mouse.get_pressed()[0] # get varible storing if the mouse was clicked

        if self.rect.collidepoint(mouse_pos):
            if mouse_click:
                pass

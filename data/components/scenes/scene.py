import pygame

class Scene():
    def __init__(self, name):
        self.name = name
        self.control = None

        self.gui_list = []
        self.menu_dict = {}
        self.active_menu = None

        self.next_scene  = None

    def update(self):
        pass

    def render(self, screen):
        self.render_contents(screen)
        self.render_gui(screen)
        pygame.display.update()

    def render_contents(self, screen):
        screen.fill((255,255,255))

    def render_gui(self, screen):
        for gui in self.gui_list:
            gui.render(screen)

        if self.active_menu:
            current_menu = self.menu_dict[self.active_menu]
            current_menu.render(screen)

    #=======================#
    #=== Event Handling ====#
    #=======================#

    def on_event(self, event):
        if self.active_menu:
            current_menu = self.menu_dict[self.active_menu]
            current_menu.on_event(event)
            return

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.click(mouse_pos, event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.unclick(mouse_pos, event)
        else:
            self.other_event(mouse_pos, event)

    def click(self, mouse_pos, event):
        pass

    def unclick(self, mouse_pos, event):
        pass

    def other_event(self, mouse_pos, event):
        pass

    def handle_server_data(self, data_type, data=None):
        pass

    #=======================#
    #=== Get & Set & Add ===#
    #=======================#

    def add_menu(self, menu):
        self.menu_dict[menu.name] = menu

    def set_active_menu(self, menu):
        self.active_menu = menu

    def set_control(self, control):
        self.control = control
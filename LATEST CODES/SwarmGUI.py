import pygame
import pygame_gui


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1080, 800))

background = pygame.Surface((1080, 800))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((1080, 800))

Login = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130, 41.667), (100, 50)),
                                            text='Login Here',
                                            manager=manager)
Calibration = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, 41.667), (200, 50)),
                                            text='Begin Calibration',
                                            manager=manager)
Task = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((490, 41.667), (100, 50)),
                                            text='Performance Task',
                                            manager=manager)
Save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 41.667), (100, 50)),
                                            text='Save last Score',
                                            manager=manager)
Logs = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((850, 41.667), (100, 50)),
                                            text='Show Log File',
                                            manager=manager)
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Login:
                    print('Hello Patient x903')

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Calibration:
                    print('CALIBRATED: "Number"')

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Task:
                    print('Beginning Performance Pardigmn')

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Save:
                    print('Saved! - TIME')

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Logs:
                    print('Log Files "here"')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
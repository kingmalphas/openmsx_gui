import pygame


def get_controller_input():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    done = False
    buttons = joystick.get_numbuttons()
    hats = joystick.get_numhats()
    analogs = joystick.get_numaxes()
    print(analogs)
    print('wainting for input')
    while done == False:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():  # User did something
            for i in range(buttons):
                button = joystick.get_button(i)
                if button == 1:
                    inp = i
                    pygame.quit()
                    return inp
            for i in range(hats):
                hat = joystick.get_hat(i)
                if str(hat) != '(0, 0)':
                    inp = hat
                    pygame.quit()
                    return inp
            for i in range(analogs):
                analog = joystick.get_axis(i)
                print(analog)
                #pygame.quit()



print(get_controller_input())


<command> bind "joy1 button9 up" "keymatrixup 6 0x20" </command>
#<command> dict lappend joystick1_config DOWN D_hat0 </command>

#



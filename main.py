import pygame
import serial

# First game (Testing the use of the joystick controlling a character)
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = pygame.Rect(200, 150, 30, 30)
ser = serial.Serial('COM10', 9600)
trying = True

while trying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            trying = False
    try:
        joystick_data = ser.readline().decode().strip().split(',')
        if len(joystick_data) == 2:
            joystickX, joystickY = map(int, joystick_data)
            player.x += int((joystickX - 512) / 50)
            player.y += int((joystickY - 512) / 50)
            player.x = max(0, min(player.x, SCREEN_WIDTH - player.width))
            player.y = max(0, min(player.y, SCREEN_HEIGHT - player.height))
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), player)
            pygame.display.update()
    except (ValueError, UnicodeDecodeError):
        pass
pygame.quit()

import pygame
import random
import serial

pygame.init()

# Set up the game window
CELL_SIZE = 60
MAZE_WIDTH = 10
MAZE_HEIGHT = 7
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tutle Treasure:Maze Game')

# Loading the background image
background_image = pygame.image.load("bg-1.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define wall color
WALL_COLOR = (255, 255, 255)
# Maze layout
maze = [[1 for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]
visited = [[False for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]

# Start the maze generation from a random cell
start_x = random.randint(1, MAZE_WIDTH - 2)
start_y = random.randint(1, MAZE_HEIGHT - 2)
maze[start_y][start_x] = 0
visited[start_y][start_x] = True

# Directions for movement
directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]


def generate_maze(x, y):
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 1 <= nx < MAZE_WIDTH - 1 and 1 <= ny < MAZE_HEIGHT - 1 and not visited[ny][nx]:
            maze[ny][nx] = 0
            maze[y + dy // 2][x + dx // 2] = 0
            visited[ny][nx] = True
            generate_maze(nx, ny)


"""
maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
"""

generate_maze(start_x, start_y)

# Define player object
turtle_image = pygame.image.load("player.png")
turtle_image = pygame.transform.scale(turtle_image, (CELL_SIZE, CELL_SIZE))


class Player:
    def __init__(self, x, y):
        self.image = turtle_image
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE

    def draw(self, screen):
        screen.blit(self.image, self.rect)


player = Player(3, 2)  # Starting position of the player

# Define treasure object
treasure_image = pygame.image.load("treasure_2.png")
treasure_image = pygame.transform.scale(treasure_image, (CELL_SIZE, CELL_SIZE))
treasure_pos = (random.randint(1, len(maze[0]) - 2) * CELL_SIZE,
                random.randint(1, len(maze) - 2) * CELL_SIZE)
treasure_rect = pygame.Rect(treasure_pos[0], treasure_pos[1],
                            CELL_SIZE, CELL_SIZE)

# Initialize serial communication
ser = serial.Serial('COM10', 9600)  # Replace 'COM10' with your actual serial port

# Load sound effects
collect_sound = pygame.mixer.Sound("collect.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# Game loop
running = True
clock = pygame.time.Clock()
MOVEMENT_SPEED = 5

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get joystick input from serial port
    try:
        joystick_data = ser.readline().decode().strip().split(',')
        if len(joystick_data) == 2:
            joystickX, joystickY = map(int, joystick_data)
            player.rect.x += int((joystickX - 512) / 50) * MOVEMENT_SPEED
            player.rect.y += int((joystickY - 512) / 50) * MOVEMENT_SPEED

            # Check for collision with walls
            for row in range(len(maze)):
                for col in range(len(maze[row])):
                    if maze[row][col] == 1:
                        wall_rect = pygame.Rect(col * CELL_SIZE,
                                                row * CELL_SIZE,
                                                CELL_SIZE,
                                                CELL_SIZE)
                        if player.rect.colliderect(wall_rect):
                            hit_sound.play()
                            player.rect.x -= int((joystickX - 512) / 50) * MOVEMENT_SPEED
                            player.rect.y -= int((joystickY - 512) / 50) * MOVEMENT_SPEED

            # Check for collision with treasure
            if player.rect.colliderect(treasure_rect):
                collect_sound.play()
                running = False
    except (ValueError, UnicodeDecodeError):
        pass

    # Draw background and maze
    screen.blit(background_image, (0, 0))
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                wall_rect = pygame.Rect(col * CELL_SIZE,
                                        row * CELL_SIZE,
                                        CELL_SIZE,
                                        CELL_SIZE)
                pygame.draw.rect(screen, WALL_COLOR, wall_rect)

    # Draw treasure object
    screen.blit(treasure_image, treasure_pos)

    # Draw player and update display
    player.draw(screen)
    pygame.display.update()

# Game over screen
font = pygame.font.Font(None, SCREEN_HEIGHT // 10)
text_surf = font.render("Well Done!", True, (0, 255, 0))
text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2,
                                       SCREEN_HEIGHT // 2))
screen.blit(text_surf, text_rect)
pygame.display.update()

# Close the serial connection
ser.close()

pygame.time.wait(3000)
pygame.quit()

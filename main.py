import pygame

WIDTH = 800
HEIGHT = 480
TILE = 40
SPEED = 5
GRAVITY = 1
JUMP_SPEED = -16

LEVEL = [
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                              C  C                          ",
    "                              ####                          ",
    "            C C            CC           C C C               ",
    "            ###            ##                               ",
    "  P                        ##                               ",
    "######  ############  ############   #######################",
    "######  ############  ############   #######################",
    "######  ############  ############   #######################",
]


def load_level():
    walls = []
    coins = []
    for row, line in enumerate(LEVEL):
        for col, letter in enumerate(line):
            x = col * TILE
            y = row * TILE
            if letter == "#":
                walls.append(pygame.Rect(x, y, TILE, TILE))
            elif letter == "C":
                coins.append(pygame.Rect(x + 12, y + 12, 16, 16))
            elif letter == "P":
                start = (x, y)
    return walls, coins, start


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Run")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

walls, coins, start = load_level()
player = pygame.Rect(start[0], start[1], 30, 40)
y_speed = 0
on_ground = False
score = 0
level_width = len(LEVEL[0]) * TILE
running = True

while running:
    # 1. Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                y_speed = JUMP_SPEED

    # 2. Update
    keys = pygame.key.get_pressed()
    x_speed = 0
    if keys[pygame.K_LEFT]:
        x_speed = -SPEED
    if keys[pygame.K_RIGHT]:
        x_speed = SPEED

    # Move sideways, then push out of any wall we walked into
    player.x += x_speed
    for wall in walls:
        if player.colliderect(wall):
            if x_speed > 0:
                player.right = wall.left
            if x_speed < 0:
                player.left = wall.right

    # Fall, then push out of any wall we landed on or bumped into
    y_speed += GRAVITY
    player.y += y_speed
    on_ground = False
    for wall in walls:
        if player.colliderect(wall):
            if y_speed > 0:
                player.bottom = wall.top
                on_ground = True
            if y_speed < 0:
                player.top = wall.bottom
            y_speed = 0

    # Coins
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    # 3. Draw
    camera_x = player.centerx - WIDTH // 2
    camera_x = max(0, min(camera_x, level_width - WIDTH))

    screen.fill((135, 206, 235))
    for wall in walls:
        pygame.draw.rect(screen, (90, 160, 70), wall.move(-camera_x, 0))
    for coin in coins:
        pygame.draw.ellipse(screen, (250, 200, 30), coin.move(-camera_x, 0))
    pygame.draw.rect(screen, (40, 70, 200), player.move(-camera_x, 0))

    text = font.render("Coins: " + str(score), True, (20, 20, 20))
    screen.blit(text, (16, 16))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame

WIDTH = 800
HEIGHT = 480
SPEED = 5
GRAVITY = 1
JUMP_SPEED = -16

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Run")
clock = pygame.time.Clock()

player = pygame.Rect(20, 320, 30, 40)
walls = [
    pygame.Rect(0, 360, 320, 120),
    pygame.Rect(440, 360, 360, 120),
    pygame.Rect(80, 260, 120, 40),
    pygame.Rect(540, 240, 160, 40),
    pygame.Rect(720, 280, 40, 80),
]
y_speed = 0
on_ground = False
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

    # 3. Draw
    screen.fill((135, 206, 235))
    for wall in walls:
        pygame.draw.rect(screen, (90, 160, 70), wall)
    pygame.draw.rect(screen, (40, 70, 200), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

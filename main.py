import pygame

WIDTH = 800
HEIGHT = 480
SPEED = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Run")
clock = pygame.time.Clock()

player = pygame.Rect(100, 320, 30, 40)
ground = pygame.Rect(0, 360, WIDTH, 120)
running = True

while running:
    # 1. Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= SPEED
    if keys[pygame.K_RIGHT]:
        player.x += SPEED

    # 3. Draw
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (90, 160, 70), ground)
    pygame.draw.rect(screen, (40, 70, 200), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

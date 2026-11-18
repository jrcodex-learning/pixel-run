import pygame

WIDTH = 800
HEIGHT = 480

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Run")
clock = pygame.time.Clock()
running = True

while running:
    # 1. Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update: nothing moves yet

    # 3. Draw
    screen.fill((135, 206, 235))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

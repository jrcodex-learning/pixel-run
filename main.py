import asyncio

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
    "  P                        ##               E      E    F   ",
    "######  ############  ############   #######################",
    "######  ############  ############   #######################",
    "######  ############  ############   #######################",
]


def load_level():
    walls = []
    coins = []
    enemies = []
    for row, line in enumerate(LEVEL):
        for col, letter in enumerate(line):
            x = col * TILE
            y = row * TILE
            if letter == "#":
                walls.append(pygame.Rect(x, y, TILE, TILE))
            elif letter == "C":
                coins.append(pygame.Rect(x + 12, y + 12, 16, 16))
            elif letter == "E":
                enemies.append({"rect": pygame.Rect(x, y + 10, TILE, 30), "speed": 2, "start_x": x})
            elif letter == "P":
                start = (x, y)
            elif letter == "F":
                flag = pygame.Rect(x + 15, y - 40, 10, 80)
    return walls, coins, enemies, start, flag


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Run")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


level_width = len(LEVEL[0]) * TILE


async def main():
    state = "new"
    running = True

    while running:
        # 0. A new game: build the level and put the player at the start
        if state == "new":
            walls, coins, enemies, start, flag = load_level()
            player = pygame.Rect(start[0], start[1], 30, 40)
            y_speed = 0
            on_ground = False
            score = 0
            state = "playing"

        # 1. Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground and state == "playing":
                    y_speed = JUMP_SPEED
                if event.key == pygame.K_r and state != "playing":
                    state = "new"

        # 2. Update
        if state == "playing":
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

            # Enemies walk two tiles each way from where they started
            for enemy in enemies[:]:
                enemy["rect"].x += enemy["speed"]
                if abs(enemy["rect"].x - enemy["start_x"]) > 2 * TILE:
                    enemy["speed"] = -enemy["speed"]
                if player.colliderect(enemy["rect"]):
                    if y_speed > 0 and player.bottom < enemy["rect"].centery:
                        enemies.remove(enemy)  # landed on top: stomped!
                        y_speed = JUMP_SPEED // 2
                    else:
                        state = "lost"

            if player.top > HEIGHT:
                state = "lost"
            if player.colliderect(flag):
                state = "won"

        # 3. Draw
        camera_x = player.centerx - WIDTH // 2
        camera_x = max(0, min(camera_x, level_width - WIDTH))

        screen.fill((135, 206, 235))
        for wall in walls:
            pygame.draw.rect(screen, (90, 160, 70), wall.move(-camera_x, 0))
        for coin in coins:
            pygame.draw.ellipse(screen, (250, 200, 30), coin.move(-camera_x, 0))
        for enemy in enemies:
            pygame.draw.rect(screen, (200, 50, 50), enemy["rect"].move(-camera_x, 0))
        pygame.draw.rect(screen, (60, 60, 60), flag.move(-camera_x, 0))
        pygame.draw.polygon(screen, (250, 120, 30), [
            (flag.right - camera_x, flag.top),
            (flag.right - camera_x + 30, flag.top + 12),
            (flag.right - camera_x, flag.top + 24),
        ])
        pygame.draw.rect(screen, (40, 70, 200), player.move(-camera_x, 0))

        text = font.render("Coins: " + str(score), True, (20, 20, 20))
        screen.blit(text, (16, 16))
        if state == "won":
            text = font.render("You win! Press R to play again", True, (20, 20, 20))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 120))
        if state == "lost":
            text = font.render("Ouch! Press R to try again", True, (20, 20, 20))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 120))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # lets the browser keep up

    pygame.quit()


asyncio.run(main())

import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
MOVE_SPEED = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catching falling object")
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_rect = pygame.Rect(player_x-20, player_y+200, PLAYER_WIDTH, PLAYER_HEIGHT)


def main():

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += MOVE_SPEED

        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_rect)

        pygame.display.update()

        pygame.time.Clock().tick(60)  # cap the frame rate

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

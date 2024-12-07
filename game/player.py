import pygame
from game.constants import PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH, MOVE_SPEED


class Player:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += MOVE_SPEED

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, self.rect)

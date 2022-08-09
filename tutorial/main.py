import pygame, math
pygame.init()


SCREEN = pygame.display.set_mode((512, 512))
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
FOV = math.radians(60)
WALL_HEIGHT = 64
PLANE_DIST = (SCREEN_WIDTH/2)/math.tan(FOV/2)


class Player:
  def __init__(self):
    self.x = 32
    self.y = 32
    self.z = 32
    self.angle = 0


def main():
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT: run = False

    

    SCREEN.fill((255, 255, 255))

    pygame.display.update()


if __name__ == "__main__":
  main()
pygame.quit()
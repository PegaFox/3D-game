import pygame, math
pygame.init()

# open the window
SCREEN = pygame.display.set_mode((1024, 512))
map = [
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 0, 0, 1, 0, 0, 0, 1],
  [1, 0, 0, 1, 0, 0, 1, 1],
  [1, 0, 0, 1, 0, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 0, 0, 0, 0, 1],
  [1, 0, 0, 0, 0, 0, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1]
]

width = int((SCREEN.get_width()/2)/len(map[0]))
height = int(SCREEN.get_height()/len(map))
tall = 50
FOV = math.radians(60)
RES = 128



class Player:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.angle = 0

  # setup how the player state changes every frame
  def update(self):
    xVel = 0
    yVel = 0
    # player movement
    if pygame.key.get_pressed()[pygame.K_a]: self.angle -= 0.1
    if pygame.key.get_pressed()[pygame.K_d]: self.angle += 0.1
    if pygame.key.get_pressed()[pygame.K_w]:
      xVel += math.cos(self.angle)
      yVel += math.sin(self.angle)
    if pygame.key.get_pressed()[pygame.K_s]:
      xVel -= math.cos(self.angle)
      yVel -= math.sin(self.angle)
    if pygame.key.get_pressed()[pygame.K_q]:
      xVel -= math.cos(self.angle+math.radians(90))
      yVel -= math.sin(self.angle+math.radians(90))
    if pygame.key.get_pressed()[pygame.K_e]:
      xVel += math.cos(self.angle+math.radians(90))
      yVel += math.sin(self.angle+math.radians(90))

    # run collisions
    if map[math.floor(self.y/height)][math.floor(((self.x+xVel)-SCREEN.get_width()/2)/width)] == 1: xVel = 0
    if map[math.floor((self.y+yVel)/height)][math.floor((self.x-SCREEN.get_width()/2)/width)] == 1: yVel = 0

    # draw the top-down player
    self.x += xVel
    self.y += yVel
    pygame.draw.line(SCREEN, (0, 0, 255), (self.x, self.y), (self.x+(math.cos(self.angle)*20), self.y+(math.sin(self.angle)*20)), 3)
    pygame.draw.circle(SCREEN, (0, 0, 255), (self.x, self.y), 5)


    # calculate rays
    lineFov = self.angle-(FOV/2)
    for line in range(RES):
      endX = self.x
      endY = self.y
      distance = 0
      while True:
        endX += math.cos(lineFov)
        endY += math.sin(lineFov)
        distance += 1
        if map[math.floor(endY/height)][math.floor((endX-SCREEN.get_width()/2)/width)] == 1: break
      pygame.draw.line(SCREEN, (0, 0, 255), (self.x, self.y), (endX, endY))
      distance *= math.cos(self.angle - lineFov)
      color = 50 / (1 + distance * distance * 0.0001)
      tangle = pygame.Rect(line*((SCREEN.get_width()/2)/RES), 0, (SCREEN.get_width()/2)/RES, (tall*SCREEN.get_height()) / distance)
      tangle.centery = self.z
      pygame.draw.rect(SCREEN, (color+100, 0, 0), tangle)

      lineFov += FOV/RES

# main function
def main():
  global RES, FOV
  clock = pygame.time.Clock()
  player = Player(700, 200, 256)
  run = True
  while run:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT: run = False
      if event.type == pygame.KEYDOWN:
        if event.scancode == 82:
          RES = int(RES*2)
        if event.scancode == 81:
          RES = int(RES/2)
        if event.scancode == 80:
          FOV = math.radians(math.degrees(FOV)-1)
        if event.scancode == 79:
          FOV = math.radians(math.degrees(FOV)+1)

    
    # draw everything
    SCREEN.fill((255, 255, 255))
    for yNum, y in enumerate(map):
      for xNum, x in enumerate(y):
        if x == 1:
          pygame.draw.rect(SCREEN, (0, 0, 0), ((xNum*width)+SCREEN.get_width()/2, yNum*height, width-1, height-1))
    player.update()
    pygame.display.set_caption("FPS: "+str(round(clock.get_fps()))+", FOV: "+str(round(math.degrees(FOV)))+", RES: "+str(RES))
    pygame.display.update()

# run the program
if __name__ == "__main__":
  main()
pygame.quit()
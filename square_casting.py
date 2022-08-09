import pygame, math
pygame.init()

# open the window
SCREEN = pygame.display.set_mode((1024, 512))
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
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

width = int((SCREEN_WIDTH/2)/len(map[0]))
height = int(SCREEN_HEIGHT/len(map))
tall = 256
FOV = math.radians(60)
RES = 512



class Player:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.angle = 1

  # setup how the player state changes every frame
  def update(self):
    global tall
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
    if pygame.key.get_pressed()[pygame.K_SPACE]: self.z += 100
    if pygame.key.get_pressed()[pygame.K_LSHIFT]: self.z -= 100
    if pygame.key.get_pressed()[pygame.K_z]: tall -= 10
    if pygame.key.get_pressed()[pygame.K_x]: tall += 10
    #fix angle
    if self.angle > math.pi*2: self.angle = 0
    if self.angle < 0: self.angle = math.pi*2
    # run collisions
    if map[math.floor(self.y/height)][math.floor(((self.x+xVel)-SCREEN_WIDTH/2)/width)] == 1: xVel = 0
    if map[math.floor((self.y+yVel)/height)][math.floor((self.x-SCREEN_WIDTH/2)/width)] == 1: yVel = 0

    # draw the top-down player
    self.x += xVel
    self.y += yVel
    pygame.draw.line(SCREEN, (0, 0, 255), (self.x, self.y), (self.x+(math.cos(self.angle)*20), self.y+(math.sin(self.angle)*20)), 3)
    pygame.draw.circle(SCREEN, (0, 0, 255), (self.x, self.y), 5)


    rayAngle = self.angle - (FOV/2)
    if rayAngle < 0: rayAngle += math.pi*2
    for ray in range(RES):
      # calculate vertical rays
      vStartX = self.x
      vStartY = self.y
      rayX = 0
      rayY = 0
      if rayAngle > math.pi and rayAngle < math.pi*2: # if looking up
        vStartY = math.floor(self.y/height)*(height) - 1
        vStartX = self.x + (self.y-vStartY)/-math.tan(rayAngle)
        rayY = -height
        rayX = -height/math.tan(rayAngle)
      elif rayAngle > 0 and rayAngle < math.pi: # if looking down
        vStartY = math.floor(self.y/height)*(height) + height
        vStartX = self.x + (self.y-vStartY)/-math.tan(rayAngle)
        rayY = height
        rayX = height/math.tan(rayAngle)

      for i in range(8):
        try:
          if map[math.floor(vStartY/height)][math.floor((vStartX-(SCREEN_WIDTH/2))/width)] == 1: break
        except: pass
        vStartX += rayX
        vStartY += rayY


      # calculate horizontal rays
      hStartX = self.x
      hStartY = self.y
      rayX = 0
      rayY = 0
      if rayAngle > math.pi*0.5 and rayAngle < math.pi*1.5: # if looking left
        hStartX = math.floor(self.x/width)*(width) - 1
        hStartY = self.y + (self.x-hStartX)*-math.tan(rayAngle)
        rayX = -width
        rayY = -width*math.tan(rayAngle)
      elif rayAngle > 1.5 or rayAngle < math.pi*0.5: # if looking right
        hStartX = math.floor(self.x/height)*(height) + height
        hStartY = self.y + (self.x-hStartX)*-math.tan(rayAngle)
        rayX = width
        rayY = width*math.tan(rayAngle)

      for i in range(8):
        try:
          if map[math.floor(hStartY/height)][math.floor((hStartX-(SCREEN_WIDTH/2))/width)] == 1: break
        except: pass
        hStartX += rayX
        hStartY += rayY

    
      vDis = math.sqrt(((self.x - vStartX) ** 2) + ((self.y - vStartY) ** 2))
      hDis = math.sqrt(((self.x - hStartX) ** 2) + ((self.y - hStartY) ** 2))

      if vDis < hDis and not vDis == 0:
        distance = vDis
        rayCollide = "vertical"
        endX = vStartX
        endY = vStartY
        pygame.draw.line(SCREEN, (0, 0, 255), (self.x, self.y), (vStartX, vStartY), 1)
      if vDis > hDis and not hDis == 0:
        distance = hDis
        rayCollide = "horizontal"
        endX = hStartX
        endY = hStartY
        pygame.draw.line(SCREEN, (0, 255, 0), (self.x, self.y), (hStartX, hStartY), 1)

      distance *= math.cos(self.angle - rayAngle)
      if round(distance) == 0: distance = 1
      color = 50 / (1 + distance * distance * 0.0001)
      rectSelect = pygame.Rect(ray*((SCREEN_WIDTH/2)/RES), 0, (SCREEN_WIDTH/2)/RES, (height*SCREEN_HEIGHT) / round(distance))
      rectSelect.centery = tall+((self.z/distance)*10)
      pygame.draw.rect(SCREEN, (color+100, color, color), rectSelect)

      #if rayCollide == "vertical":
      #  img = pygame.image.load("Assets/wall/brick.png").subsurface((endX%width, 0, 1, 64))
      #if rayCollide == "horizontal":
      #  img = pygame.image.load("Assets/wall/brick.png").subsurface((endY%width, 0, 1, 64))
      #SCREEN.blit(pygame.transform.scale(img, (rectSelect.width, rectSelect.height)), rectSelect)
      rayAngle += FOV/RES
      if rayAngle > math.pi*2: rayAngle -= math.pi*2


# main function
def main():
  global RES, FOV, tall
  clock = pygame.time.Clock()
  player = Player(650, 200, 32)
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

      if pygame.key.get_pressed()[pygame.K_f]: tall -= 1
      if pygame.key.get_pressed()[pygame.K_g]: tall += 1

    
    # draw everything
    SCREEN.fill((255, 255, 255))
    for yNum, y in enumerate(map):
      for xNum, x in enumerate(y):
        if x == 1:
          pygame.draw.rect(SCREEN, (0, 0, 0), ((xNum*width)+SCREEN_WIDTH/2, yNum*height, width-1, height-1))
    player.update()
    pygame.display.set_caption("FPS: "+str(round(clock.get_fps()))+", FOV: "+str(round(math.degrees(FOV)))+", RES: "+str(RES))
    pygame.display.update()

# run the program
if __name__ == "__main__":
  main()
pygame.quit()
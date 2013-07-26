#######################
# AUTHOR:     stm
# DATE:       23/06/13
# PROJECT:    explorer.py
# Version:    0.2
#######################

# Imports
import sys
import pygame
import os
from pygame.locals import *

class Obstacle(pygame.sprite.Sprite):
  '''This is a generic class for building
    clouds, walls and other objects that
    move across the screen at some rate.
    
    This is only designed for objects that
    move from right to left, as all of our
    player interacting objects behave in
    this way.'''
  def __init__(self, scale=2, zLevel=0, location, image="resources/Cloud.bmp"):
    pygame.sprite.Sprite.__init__(self)
    temp = game.load_image(image, -1)
    temp = (pygame.transform.scale(temp[0],(temp[0].get_width()/scale,temp[0].get_height()/scale)), temp[1])
    self.image, self.rect = temp
    self.rect = self.image.get_rect()
    self.rect.center = location

  def move(self):
    if self.rect.center[0] < -(self.rect.width) or self.rect.center[1] < -(self.rect.height):
      return False
    self.rect.center = (self.rect.center[0]-3,self.rect.center[1])
    return True


class Alien(pygame.sprite.Sprite):
  ''' This class is the basis of our
    hero Space Nigga' This is z-level 1'''
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = game.load_image("resources/alien.bmp", -1)
    self.screen = pygame.display.get_surface()
    self.area = self.screen.get_rect()
    self.rect.center = (self.rect.width/2+10, game.screen.get_height()-(self.rect.height/2)-10) 
    self.sound = game.load_sound('../../../supportFiles/sounds/rocket.wav')
    self.sound.set_volume(0.5)

  def thrusters(self): 
      self.move(0, -3)

  def move(self, dx, dy):
    self.rect = self.rect.move(dx, dy)

class GameEngine:
  '''This is the game engine.
    It is responsible trackging the physics
    and generating game objects as well as writing
    to the game screen and setup'''
  def main(self):
    ''' This is the main game function
      responsible for the creating of
      all processes and characters.'''

    # Set the size of the screen
    self.height = 400 
    self.width = 700
  
    # Initiate the game 
    pygame.init()
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption('Move the monkey')
    pygame.mouse.set_visible(1)
    background = pygame.Surface(self.screen.get_size())
    background = background.convert()
  
    # Drawing the screen and the background
    # also the sprite
    background.fill((200,200,200))
    self.screen.blit(background, (0,0))
    pygame.display.flip()

    # Create the obstacles
    obstacles = []
    obstacles.append(Obstacle((self.width,self.height/2)))

    alien = Alien()
    allsprites = pygame.sprite.RenderPlain((alien,obstacles))
    clock = pygame.time.Clock()
    keydown = False


    # Set the variable for the alien's default position
    alienHome = game.screen.get_height()-(alien.rect.height/2)-10

    # Event loop to keep track of
    # what is happening
    while True:
      clock.tick(60)
      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit(0)
        if event.type == KEYDOWN:
          if event.dict['key'] == 32:
            alien.thrusters()
            alien.sound.play(-1)
            keydown = True
        if event.type == KEYUP:
          keydown = False
          alien.sound.fadeout(200)
      print len(obstacles)
      for obstacle in obstacles:
        checkStillThere = obstacle.move()
        if not checkStillThere:
          obstacles.remove(obstacle)
          obstacles.append(Obstacle((self.width,self.height/2)))
          allsprites = pygame.sprite.RenderPlain((alien,obstacles))
          checkStillThere = True


      # This piece of logic deals with the gravity of the game.
      # When the key is not pressed i.e. when thrusters are 
      # disabled and the alien isn't in the home position
      # it is falling. We encountered a bug here in that the
      # alien would miss the landing spot and fall forever
      # but we fixed that using the > clause.
      if not keydown and alien.rect.center[1] != alienHome:
        moveDis = 2
        if alien.rect.center[1] > alienHome:
          alien.move(0, alienHome - alien.rect.center[1])
          modeDis = 0
        alien.move(0,moveDis)
      elif keydown:
        alien.move(0,-3)


      # Update the images on screen ensure they
      # also persist
      allsprites.update()
      self.screen.blit(background, (0,0))
      allsprites.draw(self.screen)
      pygame.display.flip()

  def load_image(self,img, colorkey):
    '''This image loads images for use in sprites
      and surfaces'''
    try:
      image = pygame.image.load(img)
    except pygame.error, message:
      sys.stderr.write('Cannot load image ' + image)
      raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
      if colorkey is -1:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

  def load_sound(self,sound):
    class NoneSound():
      def play(): pass
    if not pygame.mixer:
      return NoneSound()
    try: 
      sound =  pygame.mixer.Sound(sound)
    except pygame.error, message:
      sys.stderr.write('Cannot open file',wav)
      raise SystemExit, message
    return sound



if __name__ == "__main__":
  global game
  game = GameEngine()
  game.main()

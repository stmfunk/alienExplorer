#######################
# AUTHOR:     stm
# DATE:       23/06/13
# PROJECT:    explorer.py
# Version:    0.1
#######################

# Imports
import sys
import pygame
import os
from pygame.locals import *


class Alien(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = game.load_image("alien.bmp", -1)
    self.screen = pygame.display.get_surface()
    self.area = self.screen.get_rect()
    self.rect.center = (self.rect.width/2+10, game.screen.get_height()-(self.rect.height/2)-10) 

  def move(self, dx, dy):
    self.rect = self.rect.move(dx, dy)

class GameEngine:
  '''This is the game engine.
    It is responsible trackging the physics
    and generating game objects as well as writing
    to the game screen and setup'''
  def main(self):
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
    alien = Alien()
    allsprites = pygame.sprite.RenderPlain((alien))
    clock = pygame.time.Clock()
    keydown = False

    # Event loop to keep track of
    # what is happening
    while True:
      clock.tick(60)
      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit(0)
        if event.type == KEYDOWN:
          if event.dict['key'] == 32:
            alien.move(0,-3)
            keydown = True
        if event.type == KEYUP:
          keydown = False
      if not keydown and alien.rect.center[1] != game.screen.get_height()-(alien.rect.height/2)-10:
        alien.move(0,2)
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


if __name__ == "__main__":
  global game
  game = GameEngine()
  game.main()

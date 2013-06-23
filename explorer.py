#######################
# AUTHOR:     stm
# DATE:       23/06/13
# PROJECT:    explorer.py
# Version:    0.1
#######################

# Imports
import sys
import pygame


class Alien(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = game.load_image("alien.bmp")

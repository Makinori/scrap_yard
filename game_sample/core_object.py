import sys, os
import pygame
from pygame.locals import *
from constants import *

####


def map_coord_to_screen_coord(x, y,
                              width=CHARACTER_WIDTH, half_width=int(CHARACTER_WIDTH/2)):
  return (x*width+half_width, y*width+half_width)

def screen_coord_to_map_coord(x, y,
                              width = CHARACTER_WIDTH):
  return (round(x/width), round(y/width))

def relative_map_coord(splite1, splite2):
  dx = splite2.x - splite1.x
  dy = splite2.y - splite1.y
  
  return (round(dx/CHARACTER_WIDTH), round(dy/CHARACTER_WIDTH))
  
class Object:
  def __init__(self, dict):
    pass
  def update(self, dict):
    pass        


    
class Splite(Object):
  # x, y : center of characters
  def __init__(self, dict, color=(0,0,0), x=0, y=0):
    self.color = color
    self.x, self.y = x, y

    self.width = CHARACTER_WIDTH
    self.half_width = self.width/2



  def draw(self, dict):
    pygame.draw.rect(dict['screen'], self.color,
                     Rect(self.x-self.half_width, self.y-self.half_width,
                          self.width, self.width))
    
  def change_width(self, width):
    width = round(width)
    if width%2 == 1 :
      width -= 1
    self.width = width
    self.half_width = width/2

  def rect(self):
    return Rect(self.x-self.half_width, self.y-self.half_width, self.width, self.width)

  def rect_when_xy(self, x, y):
    return Rect(x-self.half_width, y-self.half_width, self.width, self.width)
  
  def collision(self, splite):
    self_rect = self.rect()
    splite_rect = splite.rect()
    
    return self_rect.colliderect(splite_rect)

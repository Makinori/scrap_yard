import pygame
from pygame.locals import *

from core_object import *


####


  
class Physics(Splite):
  def __init__ (self, dict, color=(0,0,0), x=0, y=0):
    super(Physics, self).__init__(dict, color, x, y)
    self.ax, self.ay = 0, 0
    self.vx, self.vy = 0, 0
    self.dx, self.dy = 0, 0

  def update(self, dict, collision_splite=None):
    self.update_vec()

    if(collision_splite!=None):
      self.adjust(collision_splite)
      
    self.update_place()
    

  def update_vec(self):
    self.vx += self.ax; self.vy += self.ay
    self.dx += self.vx; self.dy += self.vy

  def update_place(self):
    self.x += self.dx; self.y += self.dy
    self.dx = 0; self.dy = 0
  
  def move(self, dx, dy):
    self.dx += dx
    self.dy += dy

  def stop_x(self):
    self.dx = 0
    self.vx = 0
    self.ax = 0

  def stop_y(self):
    self.dy = 0
    self.vy = 0
    self.ay = 0
    
  def adjust(self, splite_list):
    # standard of splite_list, adjust physics of self
    # used for situation such as players hit the wall
    x_hit = self.adjust_x(splite_list)
    y_hit = self.adjust_y(splite_list)
    return (x_hit, y_hit)
    
  def adjust_x (self, splite_list):
    new_x = self.x + self.dx
    new_rect = self.rect_when_xy(new_x, self.y)

    for splite in splite_list:
      s_rect = splite.rect()
      collide = new_rect.colliderect(s_rect)
      
      if collide:
        if self.dx > 0:
          self.x = s_rect.left - self.half_width
          self.stop_x()
          return 'rgiht'
        if self.dx < 0:
          self.x = s_rect.right + self.half_width
          self.stop_x()
          return 'left'
    return None

  def adjust_y(self, splite_list):
    #width = self.width
    new_y = self.y + self.dy
    new_rect = self.rect_when_xy(self.x, new_y)

    for splite in splite_list:
      s_rect = splite.rect()
      collide = new_rect.colliderect(s_rect)

      if collide :
        if self.dy > 0:
          self.y = s_rect.top - self.half_width
          self.stop_y()
          return 'bottom'
        if self.dy < 0:
          self.y = s_rect.bottom + self.half_width
          self.stop_y()
          return 'top'
    return None

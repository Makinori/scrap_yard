
import sys, os
import pygame
from pygame.locals import *

from constants import *
from core_object import *


###


class SystemEvent(Object):
  def update(self, dict):
    # key board
    for event in dict['event']:
      if event.type == QUIT: sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE: sys.exit()
        if event.key == K_d: sys.exit()

class ParamArea(Object):
  # to show many parameter of game
  
  def __init__(self, dict):
    # df : default font
    self.char_width = 20
    self.df = pygame.font.SysFont(None, self.char_width)
    self.line_length = 30
    self.white = (255,255,255)
    self.text_list = []
    
    self.black = (0,0,0)
    self.fps = None

  def text_render(self, text):
    return self.df.render(text, True, self.black)

  def update_text_list(self, text_list):
    return list(map(lambda text: self.text_render(text[0:self.line_length]),
                    text_list))

  def draw_text_list (self, screen, text_list, x=0, y=0):
    pygame.draw.rect(screen, (0,0,255), Rect(x-5,y-5,
                                             self.line_length*self.char_width*0.4+5,
                                             self.line_length*len(text_list)*0.7+5),
                     2)
    for i in range(len(text_list)):
      screen.blit(text_list[i], (x, y+i*self.char_width))
    
  def update(self, dict):

    ### text_list1
    # key_text
    pk = dict['event_pressed'] # pressed_keys
    pressed_list = [pk[K_LEFT], pk[K_UP], pk[K_DOWN], pk[K_RIGHT]]
    # coin text
    coin_frame = str(dict['coin'].contact_frame)+ ' , '+ str(dict['coin'].alone_frame)
    coin_get_left = str(dict['coin'].got_coin)+ ', '+ str(dict['coin'].left_coin)

    
    self.text_list1 = self.update_text_list(
      ["game params",
       "",
       "fps : " + str(dict['fps']),
       "left up down up : "+   str(pressed_list),
       "=== player ============================== ",
       str(dict['player']),
       "x, y : "+ str(int(dict['player'].x))[:5]+ " , "+ str(int(dict['player'].y))[:5],
       "mode, on_floar: "+ str(dict['player'].mode)+ ", "+ str(dict['player'].on_floar),
       "=== coin =============================== ",
       "x, y : " + str(int(dict['coin'].x))[:5]+ ", "+ str(int(dict['coin'].y))[:5],
       "touch, leave : " + coin_frame,
       "get, left : " + coin_get_left
     ])
    
  def draw(self, dict):
    screen = dict['screen']
    self.draw_text_list(screen, self.text_list1, x=20, y=240)
    
  


import sys, os
import pygame
from pygame.locals import *

from copy import copy

from util import list_tree_to_list
import maps as maps
from constants import *
from physics import *
from character import *
from game_object import *


#### init game


def create_map(game_dict, map_dict):
    
  (player_map_x, player_map_y) = map_dict['player_place']
  player_x, player_y = map_coord_to_screen_coord(player_map_x, player_map_y)
  game_dict['player'] = Player(game_dict, x=player_x, y=player_y)

  
  walls_place = copy(map_dict['wall_place_list'])
  wall_coord = list(map(lambda place : map_coord_to_screen_coord(place[0] ,place[1]),
                        walls_place))
  game_dict["wall_list"] = list(map(lambda crd: Wall(game_dict ,x=crd[0], y=crd[1]),
                                    wall_coord))

  
  coins_place = copy(map_dict['coin_place_list'])
  coin_coord = list(map(lambda place : map_coord_to_screen_coord(place[0] ,place[1]),
                        coins_place))
  game_dict["coin"] = Coin(game_dict, coord_list=coin_coord)

  
  (warp_exit_map_x, warp_exit_map_y) = map_dict['warp_exit_place']
  warp_exit_x, warp_exit_y = map_coord_to_screen_coord(warp_exit_map_x, warp_exit_map_y)
  
  warp_place = copy(map_dict['warp_place_list'])
  warp_coord = list(map(lambda place : map_coord_to_screen_coord(place[0] ,place[1]),
                        warp_place))
  game_dict["warmhole_list"] = (
    list(map(lambda crd: Warmhole(game_dict ,x=crd[0], y=crd[1],
                                  exit_x=warp_exit_x, exit_y = warp_exit_y), 
             warp_coord)))
  
  
class Game:
  def __init__(self):
    self.game_dict = {}

  def run_game(self):
    self.init_game()
    self.game_loop()    

  #### game init
  
  def init_game(self):
    self.system_init()
    self.data_init()

  def system_init(self):
    self.game_dict['fps_rate'] = FPS
    
    pygame.init()
    self.game_dict['screen']=pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(u"sample game")

    clock = pygame.time.Clock()
    self.game_dict['clock'] = clock

    self.game_dict['frame_start'] = pygame.time.get_ticks()
    self.game_dict['frame_end'] = pygame.time.get_ticks()
    self.game_dict['fps'] = 0
    
    self.game_dict['system_event'] = SystemEvent(dict)
  

  def data_init(self):
    self.map_init()
    
    self.splite_init()

    self.params_init()


  def map_init(self):
    map_str = maps.map_str
    coin_coord = maps.map_coins
    self.game_dict['map_str'] = map_str
    self.game_dict['coin_coord'] = coin_coord
    create_map(self.game_dict, maps.read_map(map_str=self.game_dict['map_str'],
                                             map_coins=self.game_dict['coin_coord']))

  def splite_init(self):
    self.game_dict['splite_tree'] = [self.game_dict['player'],
                                     self.game_dict['wall_list'],
                                     self.game_dict['warmhole_list'],
                                     self.game_dict['coin']]
  def params_init(self):
    param_area = ParamArea(self.game_dict)
    self.game_dict['param_area'] = param_area
    self.game_dict['param_list'] = [self.game_dict['param_area']]

    
  #### game loop

  def game_loop(self):
    while True :
      self.update()
      self.draw()
      self.delay_frame()

  def update(self):
  
    # system
    self.game_dict['fps'] = self.game_dict['clock'].get_fps()
  
    self.game_dict['event'] = copy(pygame.event.get())
    self.game_dict['event_pressed'] = copy(pygame.key.get_pressed())
    self.game_dict['system_event'].update(self.game_dict)

    # characters
    self.game_dict['player'].update(self.game_dict)
    self.game_dict['coin'].update(self.game_dict)
  
    # param_area
    list(map(lambda param : param.update(self.game_dict),
             self.game_dict['param_list']))


  def draw(self):
    self.game_dict['screen'].fill((180, 250, 150))
    list(map(lambda splite : splite.draw(self.game_dict),
             list_tree_to_list(self.game_dict['splite_tree'])))

    list(map(lambda param : param.draw(self.game_dict),
             self.game_dict['param_list']))
    pygame.display.update()

  
  def delay_frame(self):
    self.game_dict['frame_end'] = pygame.time.get_ticks()
    pygame.time.wait(round(1000/self.game_dict['fps_rate'])
                     -(self.game_dict['frame_end'] - self.game_dict['frame_start']))
    self.game_dict['clock'].tick()
    self.game_dict['frame_start'] = pygame.time.get_ticks()      


#### main

def main():

  game = Game()
  game.run_game()

    
if __name__ =="__main__":
  main()


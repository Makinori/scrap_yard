'''


'''

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


#### game

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

  
def update(dict):
  
  # system
  dict['fps'] = dict['clock'].get_fps()
  
  dict['event'] = copy(pygame.event.get())
  dict['event_pressed'] = copy(pygame.key.get_pressed())
  dict['system_event'].update(dict)

  # characters
  dict['player'].update(dict)
  dict['coin'].update(dict)
  
  # param_area
  dict['param_area'].update(dict)


def draw(dict):
  dict['screen'].fill((180, 250, 150))
  list(map(lambda splite : splite.draw(dict),
           list_tree_to_list(dict['splite_tree'])))

  dict['param_area'].draw(dict)
  pygame.display.update()
  
      
def main():
  ### initial
  game_dict = {}

  # system
  pygame.init()
  game_dict['screen']=pygame.display.set_mode(SCREEN_SIZE)
  pygame.display.set_caption(u"sample game")

  clock = pygame.time.Clock()
  game_dict['clock'] = clock

  game_dict['frame_start'] = pygame.time.get_ticks()
  game_dict['frame_end'] = pygame.time.get_ticks()
  game_dict['fps'] = 0
  
  game_dict['system_event'] = SystemEvent(dict)

  # data
  create_map(game_dict, maps.read_map())
  
  game_dict['splite_tree'] = [game_dict['player'],
                              game_dict['wall_list'],
                              game_dict['warmhole_list'],
                              game_dict['coin']]
  
  param_area = ParamArea(game_dict)
  game_dict['param_area'] = param_area

  # game loop
  while True:
    update(game_dict)
    draw(game_dict)

    game_dict['frame_end'] = pygame.time.get_ticks()
    pygame.time.wait(round(1000/FPS)-(game_dict['frame_end']- game_dict['frame_start']))
    game_dict['clock'].tick()
    game_dict['frame_start'] = pygame.time.get_ticks()

  



if __name__ =="__main__":
  main()


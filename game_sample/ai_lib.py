import sys, os
import pygame
from pygame.locals import *

import numpy as np

from copy import copy

from util import list_tree_to_list
import maps as maps
from constants import *
from physics import *
from character import *
from game_object import *
from game import *

#### AI player

def around_terrain(splite, dict, width):
  # returns treeain around splite
  #
  # <ex> width = 2
  # *****
  # ****#
  # **P**
  # *****
  # *###W
  #
  # # : 1 in wall dimension
  # W : 1 in warp dimension
  #
  #=====================
  #width = w => ret = [([wall, warp, coin] = 3) * ([(w+1)*2+1]^2)]
  #grid : [wall, warp, coin]

  splite_x, splite_y = screen_coord_to_map_coord(splite.x, splite.y)
  grid = np.array([[0]*(width*2+3)]*(width*2+3))
  grid_index_list = [[(col, row) for col in range(-width, width+1)]
                              for row in range(-width, width+1)]
  flat_grid_indexs = list_tree_to_list(grid_index_list)


  ### wall
  wall_grid = copy(grid)
  wall_list = dict['wall_list']
  wall_coord_list = list(map(lambda wall : relative_map_coord(splite, wall), wall_list))

  for wall_coord in wall_coord_list:
    if wall_coord in flat_grid_indexs:
      wall_grid[width+wall_coord[1]+1, width+wall_coord[0]+1] = 1

  ### walp hole
  warp_grid = copy(grid)
  warp_list = dict['warmhole_list']
  warp_coord_list = list(map(lambda warp : relative_map_coord(splite, warp), warp_list))

  for warp_coord in warp_coord_list:
    if warp_coord in flat_grid_indexs:
      warp_grid[width+warp_coord[1]+1, width+warp_coord[0]+1] = 1

  ### coin
  coin_grid = copy(grid)
  coin_list = [dict['coin']]
  coin_coord_list = list(map(lambda coin : relative_map_coord(splite, coin), coin_list))
  coin_coord = coin_coord_list[0]

  for coin_coord in coin_coord_list:
    if coin_coord in flat_grid_indexs:
      coin_grid[width+coin_coord[1]+1, width+coin_coord[0]+1] = 1

  ## coin_direction
  # x
  if coin_coord[0] < -width :
    coin_grid[width+1, 0] = 1
  if coin_coord[0] > width :
    coin_grid[width+1, 2*width+2] = 1
  # y
  if coin_coord[1] < -width :
    coin_grid[0 , width+1] = 1
  if coin_coord[1] > width :
    coin_grid[2*width+2, width+1] = 1    


  return list([wall_grid, warp_grid, coin_grid])

  
class AIPlayer(Player):
  def __init__(self, dict, x=0, y=0):
    super(AIPlayer, self).__init__(dict, x, y)

    # informations AI get
    self.input_data = []
    
    # key output AI presses
    # 0:left, 1:up, 2:down, 3:right. (0.0 ~ 1.0)
    self.output_data = [0,0,0,0]
    
    # threshold to key down
    self.threshold = 0.5

    self.vision = 2

    self.coin_relate_coord=(0,0)
    self.map_data = None

  def move_by_keys(self, ignore):
    # move by self output data
    if (self.threshold <= self.output_data[3]):
      self.move(self.move_speed, 0)
    if (self.threshold <= self.output_data[0]):
      self.move(-self.move_speed, 0)
      
    if self.on_floar :
      if (self.threshold <= self.output_data[1]):
        self.vy -= self.jump_v
    else:
      if (self.threshold <= self.output_data[1]):
        self.ay -= self.fall_ctrl_acc
      if (self.threshold <= self.output_data[2]):
        self.ay += self.fall_ctrl_acc

  def update(self, dict): 
    if self.mode == 'warp' :
      self.warp_update(dict)
    elif self.mode == 'normal':
      self.normal_update(dict)
      
      self.ai_action(dict)

    
  def ai_action(self, dict):
    self.watch_world(dict)
    self.output_data[1] = 1


  def watch_world(self, dict):
    self.coin_relate_coord=relative_map_coord(self, dict['coin'])
    self.map_data = around_terrain(self, dict, self.vision)    

    

    
#### AI status
class AIParam(ParamArea):
  def update(self, dict):
    
    map_data =  np.array(dict['player'].map_data)

    output_data = ""
    for val in dict['player'].output_data:
      val_str =  ("%0.03f, " % val)
      output_data = output_data + val_str
    
    self.text_list1 = self.update_text_list(
      ["AI params",
       str(dict['player']),
       "output_data : " ,
       output_data,
       "coin_relate_coord: "+ str(dict['player'].coin_relate_coord),
     ])
    
  def draw(self, dict):
    screen = dict['screen']
    self.draw_text_list(screen, self.text_list1, x=270, y=240)
    
  

        
#### AI mode
class AIMode (Game):
  def __init__(self, ai=AIPlayer, params=[ParamArea, AIParam]):
    super(AIMode, self).__init__()
    self.ai = ai
    self.params = params
  
  def data_init(self):
    # data
    self.map_init()

    self.game_dict['player'] = self.ai(self.game_dict,
                                       x=self.game_dict['player'].x,
                                       y=self.game_dict['player'].y)

    self.splite_init()
    
    self.params_init()
  
  def params_init(self):
    params = list(map(lambda param : param(self.game_dict),
                      self.params))
    
    self.game_dict['param_list'] = params
  
  
def main():
  ai_mode = AIMode(ai=AIPlayer)
  ai_mode.run_game()

  
if __name__ == '__main__'  :
  main()

  

  

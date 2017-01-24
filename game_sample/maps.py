from copy import copy

class ReadMap():
  def __init__(self, map_str,coin_list):
    self.map_str = map_str
    self.coin_list = coin_list
    
    self.place_dict ={}
    self.place_dict['player_place'] = None
    self.place_dict['wall_place_list'] = []
    self.place_dict['coin_place_list'] = []
    self.place_dict['warp_exit_place'] = None
    self.place_dict['warp_place_list'] = []


  def read_map_str(self):
    row_map_str = copy(self.map_str.split('\n'))
    col_row_str = ""
  
    for row in range(len(row_map_str)):
    
      col_row_str = list(row_map_str[row])
      for col in range(len(col_row_str)):
        here = (col, row)
        here_char = col_row_str[col]

        if here_char == 'P':
          self.place_dict['player_place'] = here
        if here_char == '#':
          self.place_dict['wall_place_list'] = self.place_dict['wall_place_list'] + [here]
        if here_char == 'P':
          self.place_dict['warp_exit_place'] = here
        if here_char == 'W':
          self.place_dict['warp_place_list'] = self.place_dict['warp_place_list'] + [here]

    return self.place_dict
    
  def  read_coin(self):
    self.place_dict['coin_place_list'] = self.coin_list

    
#### samples  

# w * h ~= 34 * 21

map1_str ="""
.################################
.#..............................#
.#...................##......##.#
.#.###................#.#.#..#..#
.#...#....###..###....#.#....#..#
.#...#..................#..#.##.#
.#...#...............##.#....#..#
.#...#................#.#.#..#..#
.#.###..###.###.###...#.#....##.#
.#...#................#.#....#..#
.#...#P...............#.#....#..#
.#...##...............#.#...#. ##
.#...##...............#.#.......#
.#...##........W......#.#.......#
.#...##............####.#WWW###.#
.#....#############...#.#...#...#
.#...................##...#.....#
.####..######........##.#...#.###
.#W..##........##..#.##.#...#..##
.#...................##.#...#...#
.################################
"""

map1_coins = [(21,14), (21,6), (26,20), (26,10), (26,7), (15,3), (4,12), (21, 16),
              (2,20)]

map2_str = """
.................................
.................................
.................................
.................................
.................................
.................................
.################################
.#..............................#
.#..............................#
.#..............................#
.#..............................#
.#..............................#
.#....P.........................#
.################################
.................................
.................................
"""

map2_coins = [(15, 12), (30, 11), (3,11), (20, 10), (10, 10)]

map_str = map2_str
map_coins = map2_coins


def read_map(map_str=map_str, map_coins=map_coins):
  r_map = ReadMap(map_str, map_coins)
  r_map.read_map_str()
  r_map.read_coin()
  return r_map.place_dict


from constants import *
from physics import *


class Player(Physics):
  def __init__(self, dict, x=0, y=0):
    self.default_color = (0,0,255)
    super(Player, self).__init__(dict, self.default_color, x,y)

    self.change_width(ONE_METER*0.8)

    self.mode = 'normal' # mode : normal, warp
    
    self.move_speed = 3
    self.gravity = 0.1
    self.max_falling_speed = 4
    self.jump_v = 3.0
    self.fall_ctrl_acc = self.gravity * 0.95 # falling control acceleaion
    
    self.left_right_wall, self.bottom_top_wall = None, None
    self.on_floar = False

    self.warp_max_delay = 120
    self.warp_passed_time = 0

    self.flushing = False
    self.flush_period = 8
    self.flush_frame = 0
    self.disappear = False

    self.pressed_keys = []

  def flush(self):
    if self.flushing:
      self.flush_frame += 1
      if self.flush_period <= self.flush_frame :
        self.disappear = not self.disappear
        self.flush_frame = 0
    else :
      flush_frame = 0
      self.disappear = False

  def draw(self, dict):
    self.flush()
    if not(self.disappear) :
      super(Player, self).draw(dict)

      
  def move_by_keys(self, pressed_keys):
    if pressed_keys[K_RIGHT]:
      self.move(self.move_speed, 0)
    if pressed_keys[K_LEFT]:
      self.move(-self.move_speed, 0)
      
    if self.on_floar :
      if pressed_keys[K_UP]:
        self.vy -= self.jump_v
    else:
      if pressed_keys[K_UP]:
        self.ay -= self.fall_ctrl_acc
      if pressed_keys[K_DOWN]:
        self.ay += self.fall_ctrl_acc
        
  def warp_update(self, dict):
    self.warp_passed_time += 1
    if self.warp_max_delay <= self.warp_passed_time :
      self.warp_passed_time = 0
      
      self.mode = 'normal'
      
      self.flushing = False

  def physics_update(self, dict):
    if self.bottom_top_wall=='bottom':
      self.on_floar = True
    else:
      self.on_floar = False
      
    self.move_by_keys(dict['event_pressed'])
    
    self.ay += self.gravity
    if self.vy > self.max_falling_speed:
      self.vy = self.max_falling_speed
  
    self.update_vec()
    self.left_right_wall, self.bottom_top_wall = self.adjust(dict["wall_list"])
    
    self.update_place()
    
  def normal_update(self, dict):
    self.physics_update(dict)
    self.warp_check(dict)

  def warp_check(self, dict):
    for warmhole in dict['warmhole_list']:
      if self.collision(warmhole):
        self.x = warmhole.exit_x
        self.y = warmhole.exit_y
        self.mode = 'warp'

        self.flush_frame = -20
        self.flushing = True

        return
    
  def update(self, dict):    
    if self.mode == 'warp' :
      self.warp_update(dict)
    elif self.mode == 'normal':
      self.normal_update(dict)

      
class Wall(Splite):
  def __init__(self, dict, x=0, y=0):
    color=(185, 128, 88)
    super(Wall, self).__init__(dict, color, x, y)


class Coin(Splite):
  def __init__(self, dict, coord_list=[(0,0)]):
    
    super(Coin, self).__init__(dict, (0,0,0))

    self.max_contact_frame = 40
    self.contact_frame = 0
    self.got_coin = 0

    self.max_alone_flame = 60000
    self.alone_frame = 0
    self.left_coin = 0

    self.default_color = (0, 0 ,0)
    self.delta_color = 128/self.max_contact_frame
    
    
    self.coord_list=coord_list
    self.replace()


  def update(self, dict):
    self.alone_frame += 1

    self.key_event(dict['event'])
    
    collision = self.collision(dict['player'])
    if collision :
      self.alone_frame = 0
      self.contact_frame += 1
      self.color = (128 + self.contact_frame*self.delta_color,
                    0,
                    255 - self.contact_frame*self.delta_color * 1.5)
      
    if self.contact_frame >= self.max_contact_frame:
      self.replace()
      self.got_coin += 1

    if self.alone_frame >= self.max_alone_flame:
      self.replace()
      self.left_coin += 1

  def key_event(self, event):
    for eve in event:
      if eve.type == KEYDOWN:
        if eve.key == K_z:
          self.alone_frame = self.max_alone_flame
    
  def replace(self):
    self.x = self.coord_list[0][0]
    self.y = self.coord_list[0][1]
    self.coord_list = self.coord_list[1:] + [self.coord_list[0]]
    
    self.color = self.default_color
    self.contact_frame = 0
    self.alone_frame = 0
    

class Warmhole(Splite):
  def __init__(self, dict, x=0, y=0, exit_x=0, exit_y=0):
    self.color = (0, 100, 0)
    super(Warmhole, self).__init__(dict, self.color, x, y)
    
    self.exit_x = exit_x
    self.exit_y = exit_y


import sys
import numpy as np
import random as random

from ai_lib import *

import chainer
from chainer import cuda, Function, gradient_check, \
  Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L


#### Neural net
class AI(Chain):
  def __init__(self):
    super(AI, self).__init__(
      l1 = L.Linear(3*7*7, 200),
      l2 = L.Linear(200, 100),
      l3 = L.Linear(100, 50),
      l4 = L.Linear(50,4)
      )

  def __call__(self, x, t):
    y = self.forward(x)
    return F.mean_squared_error(y, t)

  def no_good(self, n):
    return F.mean_squared_error(np.array([0.0]).astype(np.float32),
                                np.array([n]).astype(np.float32))

  def forward(self, x):
    h1 = F.relu(self.l1(x))
    h2 = F.relu(self.l2(h1))
    h3 = F.relu(self.l3(h2))
    h4 = self.l4(h3)
    
    return h4
    

#### game_class

class NNPlayer(AIPlayer):
  def __init__(self, dict, x=0, y=0):
    super(NNPlayer, self).__init__(dict, x, y)

    self.threshold = 0.5
    
    self.frame_per_predict = 12
    self.now_frame = 0

    self.teaching = 'false'
    self.teach_data = self.output_data
    self.loss = 0
    
    self.model = AI()
    self.optimizer = optimizers.Adam()
    self.optimizer.setup(self.model)

    self.network_file_name = "neuralnet.model"
    
  
  def set_teach_data(self, dict):
    pressed_keys = dict['event_pressed']
    if pressed_keys[K_x]:
      self.teaching = 'by_key'
      self.teach_data = [
        pressed_keys[K_LEFT],
        pressed_keys[K_UP],
        pressed_keys[K_DOWN],
        pressed_keys[K_RIGHT]]
    elif pressed_keys[K_c]:
      self.teaching = 'no_good'
      self.teach_data = self.output_data
    else :
      self.teaching = 'false'

  def set_system_by_key(self, dict):
    for event in dict['event']:
      if event.type == KEYDOWN:
        if event.key == K_a: dict['fps_rate'] -= 10
        if event.key == K_q: dict['fps_rate'] += 10

        if event.key == K_s: self.frame_per_predict -= 1
        if event.key == K_w: self.frame_per_predict += 1
        if self.frame_per_predict <= 1 : self.frame_per_predict = 1

        if event.key == K_r : self.save()
        if event.key == K_f : self.load()

  def save(self):
    print("saveing network to")
    serializers.save_npz(self.network_file_name, self.model)

  def load(self):
    print("loading network from")
    serializers.load_npz(self.network_file_name, self.model)
  
  def config_by_key(self, dict):
    self.set_teach_data(dict)
    self.set_system_by_key(dict)

  def predict(self, input_data):
    out = self.model.forward(input_data)
    out = list(out[0].data)

    self.output_data = out

  def training(self, input_data):
    if self.training != 'false':
      self.model.zerograds()
      loss = None


      if self.teaching == 'no_good':
        teach_data = np.array(self.teach_data).reshape(1,4).astype(np.float32)
        loss = self.model(input_data, teach_data)
      
      elif self.teaching == 'by_key':
        teach_data = np.array(self.teach_data).reshape(1,4).astype(np.float32)
        loss = self.model(input_data,
                          teach_data)

      else :
        loss = self.model(input_data, np.array([self.output_data]))

      loss.backward()
      self.optimizer.update()
        
      self.loss = loss.data

  def ai_action(self, dict):
    self.now_frame += 1
    
    self.config_by_key(dict)

    if self.now_frame % self.frame_per_predict == 0:
      self.watch_world(dict)
      input_data = np.array(self.map_data).reshape(1,3*7*7).astype(np.float32)
      input_data = Variable(input_data)
    
      self.predict(input_data)

      self.training(input_data)



      

### Ai param

class NNParam(ParamArea):
  def update(self, dict):
    
    map_data =  np.array(dict['player'].map_data)

    
    self.text_list1 = self.update_text_list(
      ["Neural net",
       "teaching : " + str(dict['player'].teaching),
       "loss : " + str(dict['player'].loss),
       "frame/predict : " +str(dict['player'].frame_per_predict)
     ])
    
  def draw(self, dict):
    screen = dict['screen']
    self.draw_text_list(screen, self.text_list1, x=270, y=360)

    


# main

def main():

  
  ai_mode = AIMode(ai=NNPlayer, params=[ParamArea, AIParam, NNParam])
  ai_mode.run_game()
  
if __name__ == '__main__'  :
  """
  z : next coin
  x : teach use arrow key
  c : out of stack to network

  a : down fps rate
  q : up fps rate
  
  w : up frame_per_predict
  s : down frame_per_predict

  r : save network
  f : load_network

  d : exit
  """
  
  main()


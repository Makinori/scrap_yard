
class Bullet extends GameObject{
  int past_time;
  float force;
  Bullet () { 
  }
  void setup () {
  }
  void update () { 
  } 
  void draw () {
  }
}

// bullet scripts

class StraightBullet extends Bullet {
  float speed;
  float depth = 20;
  void setup (float _speed, float _x, float _y, float _dir) {
    x = _x;
    y = _y;
    speed = _speed;
    dir = _dir;
  }
  
  void update (){
    x+= cos (dir)*speed/frameRate;
    y+= sin (dir)*speed/frameRate;
  }
  void draw () {
    line(x,y, x+cos(dir)*depth, y+sin(dir)*depth);
  }
}
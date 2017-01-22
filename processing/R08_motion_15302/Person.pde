

class Person extends GameObject {
  int hp ;
  
  Person () {
  }
  void setup() {
  }
  
  void update () {
  }
  void draw () {
  }
  boolean dead () {
    return false;
  }
}

class OwnMachine extends Person {
  float distToMouse = 0;
  float loading_time = 0.1;
  float passed_time;
  float next_dir = 0;
  
  OwnMachine () {
    r = 16;
    x= 200; y= 200;
    speed = 150;
    image = loadImage("data/machine.png");
  }
  void setup () {
  }
  
  void update () {
    passed_time += 1/frameRate;
    dir = getRadFromTwoPoint(x,y, mouseX, mouseY);
    distToMouse = dist(x,y,mouseX,mouseY);
    next_dir = (PI-speed/frameRate/distToMouse) /2 ;
    
    if (keyPressed){
      move();
    }
    if (mousePressed){
      if (mouseButton==LEFT && passed_time > loading_time){
        StraightBullet bullet = new StraightBullet();
        bullet.setup(300,x,y, dir);
        stg_ctrl.addBullet(bullet);
        passed_time = 0;
      }
    }
  }
  
  void move () {
    if (key == 'w'){
        y+= sin(dir)*speed/frameRate ;
        x+= cos(dir)*speed/frameRate ;
      } else if (key == 's'){
        y-= sin(dir)*speed/frameRate;
        x-= cos(dir)*speed/frameRate;
      } else if (key == 'a'){
        y+= sin(dir-next_dir)*speed/frameRate;
        x+= cos(dir-next_dir)*speed/frameRate;
      } else if (key == 'd'){ 
        x+= cos(dir+next_dir)*speed/frameRate;
        y+= sin(dir+next_dir)*speed/frameRate;
        //y= sin(dir+PI-(speed/frameRate/distToMouse))*distToMouse + mouseY ;
        //x= cos(dir+PI-(speed/frameRate/distToMouse))*distToMouse + mouseX ;
      }
  }
  
  void draw () {
    //image(image, x-r, y-r);
    showImage (image, x, y, r, dir);
  }
  
}
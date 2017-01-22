

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
}

class OwnMachine extends Person {
  float distToMouse = 0;
  float loading_time = 0.1; //second
  float passed_time;
  
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
    
    if (keyPressed){
      move();
    }
    if (mousePressed){
      if (mouseButton==LEFT && passed_time>= loading_time){
        StraightBullet bullet = new StraightBullet();
        bullet.setup(200,x,y, dir);
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
        y= sin(dir+PI+(speed/frameRate/distToMouse))*distToMouse + mouseY ;
        x= cos(dir+PI+(speed/frameRate/distToMouse))*distToMouse + mouseX ;
      } else if (key == 'd'){ 
        y= sin(dir+PI-(speed/frameRate/distToMouse))*distToMouse + mouseY ;
        x= cos(dir+PI-(speed/frameRate/distToMouse))*distToMouse + mouseX ;
      }
  }
  
  void draw () {
    //image(image, x-r, y-r);
    showImage (image, x, y, r, dir);
  }
  
}
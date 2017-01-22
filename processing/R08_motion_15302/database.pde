// functions

boolean pointHitJudge (float x1, float y1, float x2, float y2, float r2) {
  return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) < r2;
}

float getRadFromTwoPoint(float x1, float y1, float x2, float y2){ 
  return -atan2(x2-x1, y2-y1) + PI/2 ;
}

void showImage (PImage image, float x, float y, float r,float dir){
  translate(x, y);
  rotate (dir+PI/2);

  image (image, 0, 0);
  stroke(255);

  rotate (-dir-PI/2);
  translate(-x, -y);
}

// 
int enemy = 1;
int ally = 2;

// datas
int screen_width = 400;
int screen_height = 400;

// constr
OwnMachine hero;

STGCtrl stg_ctrl;
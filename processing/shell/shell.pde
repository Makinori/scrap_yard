
void  setup (){
  frameRate (1);
  size (600, 600);
  strokeWeight (1);
}

void shell (int stair, float x, float y, float r ){
  if (stair == 0){
    point (x, y);
  }else {
  shell (stair-1, x+r/2, y+r/2, r/2) ;
  shell (stair-1, x,     y-r/2, r/2) ;
  shell (stair-1, x-r/2, y+r/2, r/2) ;
  }
}

void draw () {
  background (0);
  stroke (0, 255,0);
  shell (9, 300, 300,250);
}
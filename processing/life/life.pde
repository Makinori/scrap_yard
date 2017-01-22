//game of life
//author: Makinori Ikegami <maau3p@gmail.com>


boolean livingJudge(boolean adj_cell[]) {
  int adj_living=0;
  boolean center = adj_cell[4];
  int contl=0; // contact_living
  
  for (int i=0; i<9; i++){
    if (adj_cell[i]) {
      adj_living++; 
      contl++;
      if (i==4) contl--;
    }
  }
  int adjl = adj_living; // abridgement of adj_living
  
  if (center && (contl==2||contl==3)) return true;
  else if (!center && (contl==3))     return true;
  else                                return false;
}

void setup (){
  size (400,400);
  rect_size_x = width/map_width;
  rect_size_y = height/map_height;
  
  map = randomInit(map, 0.30);
  
  frameRate(3);
  fill(0,155,0);
  stroke (127);
}



void draw () {  
  // update  
  map = updateMap(map);

  //print
  background(0);
  showMap (map); 
}
final int map_width = 100;
final int map_height = 100;

float rect_size_x;
float rect_size_y;

boolean map[][] = new boolean[map_height][map_width];


boolean[][] updateMap (boolean map[][]){
  int height_d = map.length -1 ;
  int width_d  = map[0].length -1;
  int above, right, under, left;
  
  boolean new_map [][] = new boolean [height_d+1][width_d+1];
  
  for (int y = 0; y<=height_d; y++){
    for (int x=0; x<=width_d; x++){
      above = y==0        ? height_d : y-1;
      right = x==width_d  ? 0        : x+1;
      under = y==height_d ? 0        : y+1;
      left  = x==0        ? width_d  : x-1;
      
      boolean adj_lis [] = {
        map[above][left], map[above][x], map[above][right],
        map[y][left]    , map[y][x]    , map[y][right],
        map[under][left], map[under][x], map[under][right]
      };
      
      new_map[y][x] = livingJudge(adj_lis);
    }
  } 
  return new_map;
}

boolean[][] randomInit(boolean map[][], float keisuu){
  for (int y=0; y<map_height; y++){
    for (int x=0; x<map_width; x++){
      map[y][x] = random(0,1)<=keisuu;
    }
  }
  return map;
}

void showMap (boolean map[][]) { 
  for (int y=0; y<map_height; y++){
    for (int x=0; x<map_width; x++){
      if (map[y][x]) fill(0,192,0);
      else           fill(0);
      rect(x*rect_size_x,y*rect_size_y, rect_size_x, rect_size_y);
    }
  }
}
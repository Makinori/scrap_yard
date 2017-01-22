//Mandelbrot set 
//author: Makinori Ikegami <maau3p@gmail.com>
//refrenced: http://www.purika.sakura.ne.jp/program/pro_002mset.shtml

//操作法
//矢印キー: 視点移動
//w/sキー: 拡大/縮小

final int point_width = 400;
final int point_height = 400;

void setup () {
  
  size (400,400);
 // strokeWeight (0);
  noStroke();
  //colorMode( HSB );
}

double xcenter = -0.75; 
double ycenter = 0.0;  
double radius = 4.0;  
double ppp = radius * 2.0 / (point_width < point_height ? point_width : point_height);

void drawPoint (int pointX, int pointY, int d ){ //d :: density
  if (d==64){
    fill (0);
  }else {
    fill (d*4,0,255-d*4);
  }
  rect(pointX,pointY,1,1);
}

void drawFractal (){
    for (int h=0; h<point_height; h++){
    for (int w=0; w<point_width; w++){
      final double a = xcenter + ppp *(w-point_width/2);
      final double b = ycenter - ppp *((h+1) - point_height/2);
      double t, x =0.0, y=0.0;
      
      int i=0;
      while (i < 64 && x*x+y*y<4){
        t= x*x-y*y+a; //x*x-y*y+a;
        y=2.0*x*y+b;
        x=t;
        i++;
      }
      drawPoint (w,h,i);
    }
  }
}

void userEvent () {
  if (keyPressed){
    if (key=='w'){
      radius/=1.2;
      ppp = radius * 2.0 / (point_width < point_height ? point_width : point_height);
    } else if (key=='s'){
      radius*=1.2;
      ppp = radius*2.0/(width<point_height ? point_width : point_height );
    } else if (keyCode == RIGHT){
      xcenter+=radius/20; //0.01;
    } else if (keyCode == LEFT) {
      xcenter-=radius/20; //0.01;
    } else if (keyCode == UP){
      ycenter +=radius/20;
    } else if (keyCode == DOWN){
      ycenter -=radius/20;
    }
    
  }
}

void draw () {
  background(0);
  
  drawFractal();
  
  userEvent () ;
}

void setup () {
  
  // set default datas
  imageMode(CENTER);
  
  
  // game config 
  size (400, 400);
  
  // test 
  stg_ctrl = new STGCtrl();
  hero = new OwnMachine ();
  

}

void draw () {
  background(0);
  
  hero.update();
  hero.draw();
  
  stg_ctrl.update();
  
  
}
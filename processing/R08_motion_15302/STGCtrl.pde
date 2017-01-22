class STGCtrl {
  int list_max = 1000;
  int bullet_pos = 0;
  int person_pos = 0;
  Bullet[] bullets = new Bullet[list_max];
  Person[] persons = new Person[list_max];
  
  STGCtrl () {
    for (int i=0; i<list_max; i++){
      bullets[i] = new Bullet();
      persons[i] = new Person();
    }
    
  }
  
  void addBullet (Bullet bullet) {
    bullets[bullet_pos] = bullet;
    bullet_pos ++;
  }
  void addPerson(Person person){
    persons[person_pos] = person;
    person_pos ++;
  }
  
  void update() {
    for (int i =0; i<bullet_pos; i++){
      bullets[i].update();
      bullets[i].draw();
    }
    for (int i =0; i<person_pos; i++){
      persons[i].update();
      persons[i].draw();
    }
  }
  
}
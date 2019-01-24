float centerx = 200.0;
float centery = 200.0;

int i = 1;

float range = 100.0;

float sumx = 200.0;
float sumy = 200.0;


void setup() {
  background(255);
  size(400,400);  
  point(centerx, centery);
  frameRate(1000);
}

void draw() {
  background(255);
  float randx = random(400);
  float randy = random(400);
  ellipse(centerx, centery, range*2,range*2);
  
  if (sqrt(pow(randx - centerx,2) + pow(randy - centery,2)) <= range) {
    i = i+1;
    //point(randx, randy);
    
    sumx = sumx + randx;
    sumy = sumy + randy;

    centerx = sumx/i;
    centery = sumy/i;
    fill(0,255,0);
    ellipse(centerx, centery, range*2,range*2);
 
    //println(centerx + "; " + centery);
    //println("x = " + randx + "y = " + randy);
    
  }
}

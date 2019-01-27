float centerx = 100.0;
float centery = 200.0;

float centerxb = 300.0;
float centeryb = 200.0;

int i = 1;
int ib = 1;

float range = 100.0;

float sumx = centerx;
float sumy = centery;

float sumxb = centerxb;
float sumyb = centeryb;


void setup() {
  background(255);
  size(400,400);  
  point(centerx, centery);
  frameRate(5000);
}

void draw() {
  //background(255);
  float randx = random(400);
  float randy = random(400);
  //ellipse(centerx, centery, range*2,range*2);
  
  if (sqrt(pow(randx - centerx,2) + pow(randy - centery,2)) <= range) {
    i = i+1;
    stroke(255,0,0);
    point(randx, randy);
    
    sumx = sumx + randx;
    sumy = sumy + randy;

    centerx = sumx/i;
    centery = sumy/i;
    //fill(0,255,0);
    //ellipse(centerx, centery, range*2,range*2);
 
    //println(centerx + "; " + centery);
    //println("x = " + randx + "y = " + randy);
  } else if (sqrt(pow(randx - centerxb,2) + pow(randy - centeryb,2)) <= range) {
    ib = ib+1;
    stroke(0,255,0);
    point(randx, randy);
    
    sumxb = sumxb + randx;
    sumyb = sumyb + randy;

    centerxb = sumxb/ib;
    centeryb = sumyb/ib;
    //fill(0,255,0);
    //ellipse(centerx, centery, range*2,range*2);
 
    //println(centerx + "; " + centery);
    //println("x = " + randx + "y = " + randy);
  } else {
    stroke(0,0,255);
    point(randx, randy);
  }
}

// Range represents the length of the boxe
float range = 7.0;
float i = 0.0;

float h = random(range/2, 100-range/2);
float s = random(range/2, 100-range/2);
float v = random(range/2, 100-range/2);

void setup() {
  size(200, 200);
  colorMode(HSB, 100, 100, 100);
  h = h-range/2;
  s = s-range/2;
  //frameRate(10);
}

void draw() {
  //background(255);
  for (int j = 0; j< height; j++) {
    for (int k = 0; k < width; k++) {
      stroke(h + j*range/height, s + k * range/width, v + (range/2)*sin(i));
      point(j, k);
    }
  }
  //println(v + (range/2)*sin(i));
  i = i + 0.5;
  //range = mouseY;
}

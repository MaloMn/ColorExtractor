// Range represents the length of the boxe
float range = 7.0;
float i = 0.0;

float h, s, v;

void setup() {
  size(200, 300);

  colorMode(RGB, 100, 100, 100);

  //background(255);
}

void draw() {
  if (i%6.50 == 0) {
    h = random(range/2, 100-range/2);
    s = random(range/2, 100-range/2);
    v = random(range/2, 100-range/2);

    h = h-range/2;
    s = s-range/2;

    for (int j = 0; j< width/2; j++) {
      for (int k = 0; k < width/2; k++) {
        stroke(h + 2*j*range/width, s + k * 2*range/width, v - (range/2));
        point(j, width + k);
      }
    }

    for (int j = 0; j< width/2; j++) {
      for (int k = 0; k < width/2; k++) {
        stroke(h + 2*j*range/width, s + k * 2*range/width, v + (range/2));
        point(width/2 + j, width + k);
      }
    }
  }


  for (int j = 0; j< width; j++) {
    for (int k = 0; k < width; k++) {
      stroke(h + j*range/width, s + k * range/width, v + (range/2)*sin(i));
      point(j, k);
    }
  }

  i = i + 0.25;
  //noStroke();
}

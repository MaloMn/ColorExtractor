// Defining desired ranges
float hue_rez = 30;
float sat_rez = 0.17;
float val_rez = 0.1;

float hue_cen = 180.0;
float sat_cen = 0.5;
float val_cen = 0.5;

void setup() {
  size(600, 600);

  colorMode(HSB, 360, 1, 1);
 
  hue_cen = random(hue_rez, 360 - hue_rez);
  sat_cen = random(sat_rez, 1 - sat_rez);
  val_cen = random(val_rez, 1 - val_rez);

}

void draw() {
 
  background(0,0,1);  //light red background color
  hexagon(300, 300, 200, color(hue_cen, sat_cen, val_cen));
  // Hue
  hexagon(300, 100, 200, color(hue_cen - hue_rez, sat_cen, val_cen));
  hexagon(300, 500, 200, color(hue_cen + hue_rez, sat_cen, val_cen));
  // Sat
  hexagon(120, 200, 200, color(hue_cen, sat_cen - sat_rez, val_cen));
  hexagon(480, 400, 200, color(hue_cen, sat_cen + sat_rez, val_cen));
  // Val
  hexagon(120, 400, 200, color(hue_cen, sat_cen, val_cen - val_rez));
  hexagon(480, 200, 200, color(hue_cen, sat_cen, val_cen + val_rez));
}


void hexagon(int x, int y, int tall, color c) {  // (center x-coordinate, center y-coordinate, height)
 
  fill(c);  //light green fill
  strokeWeight(0);
  
  // Draw a hexagon by creating (x, y) vertices
  beginShape();
  vertex(x - 3/10.0 * tall, y - 1/2.0 * tall);
  vertex(x + 3/10.0 * tall, y - 1/2.0 * tall);
  vertex(x + 3/5.0 * tall, y);
  vertex(x + 3/10.0 * tall, y + 1/2.0 * tall);
  vertex(x - 3/10.0 * tall, y + 1/2.0 * tall);
  vertex(x - 3/5.0 * tall, y);
  endShape(CLOSE);  //closes the first and last point
}

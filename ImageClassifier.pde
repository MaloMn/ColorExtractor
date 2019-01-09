PImage img;
color[] colors = new  color[4];
File dir = new File(dataPath(""));
String[] list = dir.list();

void setup() {
  size(500,500);
  print(list[0]);
  //for (int i = 0; i < list.length; i++) {
  //  println('[' + i + ']' + list[i]);
  //}
  
  
  img = loadImage("th.jpg");
  img.loadPixels();
  
  img.resize(2,2);
  for (int i = 0; i < 4; i++) {
    colors[i] = img.pixels[i];
  }
  for (int i = 0; i < 4; i++) {
    noStroke();
    fill(colors[i]);
    rect((i%2)*width/2, floor(i/2)*height/2, width/2, height/2);
  }





}

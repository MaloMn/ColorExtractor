PImage img;
color[] colors = new  color[4];
// We get the list of the files in the data folder
File dir = new File(dataPath(""));
String[] list = dir.list();
color[] colorList = new color[list.length*4];

size(400,800);

for (int i = 0; i < list.length; i++) {
  println("[" + i + "] " + list[i]);
}

for (int i = 0; i < list.length; i++) {
  // Loading the image
  img = loadImage(list[i]);
  img.loadPixels();
  
  //image(img, 0, 0, width, width);
  
  // Getting the four dominant colors of the image
  img.resize(2,2);
  for (int j = 0; j < 4; j++) {
    colors[j] = img.pixels[j];
  }
  colorList = append(colors, ';');
  // Displaying colors
  for (int j = 0; j < 4; j++) {
    noStroke();
    fill(colors[j]);
    rect(j*width/4, i*height/list.length, width/4, height/list.length);
  }
}

println(colorList);

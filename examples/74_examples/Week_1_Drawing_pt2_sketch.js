let slider;
let slider1;

function setup() {
  createCanvas(710, 400);
  background(0);
  colorMode(HSB);
  
  label = createDiv('Color');
  label.position(0, 400);
  slider = createSlider(0, 255, 255);
  slider.position(0, 415);
  
  
  label1 = createDiv('Stroke Size')
  label1.position(0, 430);
  slider1 = createSlider(1, 10, 5);
  slider1.position(0, 450);
}



function draw() {
  stroke(slider.value(), 100, 100);
  strokeWeight(slider1.value());
  if (mouseIsPressed === true) {
    drawLine(mouseX, mouseY, pmouseX, pmouseY);
    drawLine(width-mouseX, mouseY, width-pmouseX, pmouseY)
    drawSquare(10, 10, 20);
  }
}

function drawLine(mx, my, pmx, pmy) {
  line(mx, my, pmx, pmy);
}

function drawSquare(w, h, c) {
  fill(slider.value(), 100, 100, 127);
  square(w, h, c);
}
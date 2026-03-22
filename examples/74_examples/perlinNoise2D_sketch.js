let start = 0; // move noise horizontally
let yoff = 0;

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(30);

}

function draw() {
  smooth();
  stroke(142, 169, 237, 50);
  noFill();

  beginShape();

  let xoff = start;
  for (let x = 0; x < width; x += 10) {
    // 2D noise changes y position as well
    let y = map(noise(xoff, yoff), 0, 1, 120, height - 120);

    vertex(x, y);
    xoff += 0.05;

  }
  yoff += 0.008;

  endShape();

  // start+=0.001; move noise horizontally

  if (yoff > 2.5) {
    noLoop();
  }
}
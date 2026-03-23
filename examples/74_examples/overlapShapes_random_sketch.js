let x, y, i;

function setup() {
  createCanvas(windowWidth, windowHeight);
  colorMode(HSB, 100, 100, 100);
}

function draw() {
  noLoop();
    background(0, 0, 0, 30);

  for (y = 0; y < height - 20; y += 100) {
    for (x = 0; x < width - 20; x += 100) {
      for (i = 0; i < 15; i++) {

        fill(random(0, 100), 100, 100, random(0.8));
        noStroke();
        triangle(x + random(60), y + random(60), x + random(60), y + random(60), x + random(60), y + random(60));
        ellipse(x + random(70), y + random(70), i, i);
      }
    }
  }
}

// function mousePressed() {

// }
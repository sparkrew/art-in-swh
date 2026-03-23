let angle = 0;
let angle2 = 0;
let speed = 0.001;

function setup() {
  createCanvas(windowWidth, windowHeight);

  noFill();
}

function draw() {
  let speed = map(mouseY, 0, height, -0.2, 0.2);
  let arm = map(mouseX, 0, width, 10, 300);
  let color = map(arm, 10, 400, 0, 300);
  let color2 = map(angle, 0, TWO_PI, 0, 300);

  background(255);
  translate(width / 2, height / 2);
  pinWheel(arm, color, color2, angle, true);

  for (let i = 0; i < 10; i++) {
    push();
    rotate((i * TWO_PI) / 10);
    translate(0, 2 * arm);
    pinWheel(arm / 2, 255, 255, -2 * angle, true);

    pop();
  }
}

function pinWheel(arm, color, color2, rotateSpeed, hasCircles) {
  rotate(rotateSpeed);
  let shearValue = map(mouseY, 0, height, 1, 10);

  for (let i = 0; i < 10; i++) {
    push();
    if (mouseIsPressed) {
      shearX((i * TWO_PI) / shearValue);
      shearY((i * TWO_PI) / shearValue);
    }
    //shearX((i * TWO_PI) / shearValue)
    rotate((i * TWO_PI) / 10);
    translate(0, arm);
    circle(0, 0, 10);
    line(0, 0, arm, arm / 2);

    line(0, 0, arm / 2, arm);

    strokeWeight(3);
    stroke(0, 0, 255);
    line(-40, -40, arm / 2, angle);
    stroke(0);
    //triangle(-15,20, 40, 10, 100, 20)
    fill(color, 0, 255, 40);
    triangle(-15, arm / 2, arm, 10, 40, 20);

    triangle(-15, -arm / 2, arm, 10, 40, 20);
    strokeWeight(0);
    fill(0, 255, color, 150);
    triangle(0, -arm, -200, 10, arm / 5, 10);
    noFill();
    fill(255, 0, color, 150);
    triangle(0, -arm, -arm / 2, 10, 200, 50);
    noFill();
    strokeWeight(1);
    stroke(0);
    line(-15, -arm, arm, 100);

    stroke(255, arm, 0);
    strokeWeight(arm / 50);
    line(-15, -arm, arm, 200);
    strokeWeight(1);
    stroke(0);

    if (hasCircles) {
      rotate(angle2 / 2);
      circles(angle2, arm, speed);
      angle2 += speed;
    }

    pop();
  }

  angle += speed / 2;
}

function circles(angle2, arm, speed) {
  for (let j = 0; j < 3; j++) {
    push();
    rotate((j * TWO_PI) / 5);
    translate(0, arm);
    fill(255, 255, 0, 150);
    circle(0, 0, arm / 8);
    noFill();
    pop();
  }
}

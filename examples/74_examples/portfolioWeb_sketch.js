var particles = [];
var bg
const COL = createCols("https://coolors.co/app/f1e7b6-400082-fe346e-f3c623-06aed5");

function setup() {
  createCanvas(windowWidth, windowHeight);
  pixelDensity(1);
  background(255);
  bg = createGraphics(width, height);
  bg.background(255, 20);
  bg.noStroke();
  for (let i = 0; i < 300000; i++) {
    let x = random(width);
    let y = random(height);
    let s = noise(x * 0.01, y * 0.01) * 2;
    bg.fill(240, 50);
    bg.rect(x, y, s, s);
  }
}

function draw() {
  var newParticles = [];
  for (var i = 0; i < particles.length; i++) {
    particles[i].update();
    particles[i].wallBound();
    particles[i].display();
    if (particles[i].radius > 0) {
      newParticles.push(particles[i]);
    }
  }
  particles = newParticles;
  image(bg, 0, 0);
}

function mouseMoved() {
  var x = mouseX;
  var y = mouseY;
  var vx = (winMouseX - pwinMouseX) * 0.2;
  var vy = (winMouseY - pwinMouseY) * 0.2;
  if ((x > 50 && x < width - 50) && (y > 50 && y < height - 50)) {
    particles.push(new Particle(x, y, vx, vy));
  }
}

function touchMoved() {
  var x = mouseX;
  var y = mouseY;
  var vx = (winMouseX - pwinMouseX) * 0.2;
  var vy = (winMouseY - pwinMouseY) * 0.2;
  if ((x > 50 && x < width - 50) && (y > 50 && y < height - 50)) {
    particles.push(new Particle(x, y, vx, vy));
  }
}

var Particle = function(x, y, vx, vy) {
  this.position = createVector(x, y);
  this.velocity = createVector(vx, vy);
  this.friction = 0.009;
  this.fcolor = color(COL[int(random(COL.length))]);
  this.radius = random(10, 50);
}

Particle.prototype.update = function() {
  this.velocity = this.velocity.mult(1 - this.friction);
  this.position = this.position.add(this.velocity);
  this.radius -= 0.1;
}

Particle.prototype.wallThrough = function() {
  if (this.position.x >= width) {
    this.position.x = 0;
  }
  if (this.position.x <= 0) {
    this.position.x = width;
  }
  if (this.position.y >= height) {
    this.position.y = 0;
  }
  if (this.position.y <= 0) {
    this.position.y = height;
  }
}

Particle.prototype.wallBound = function() {
  if ((this.position.x >= width - this.radius) || (this.position.x <= this.radius)) {
    this.velocity.x = -this.velocity.x;
  } else if ((this.position.y >= height - this.radius) || (this.position.y <= this.radius)) {
    this.velocity.y = -this.velocity.y;
  } else {
    return;
  }
}

Particle.prototype.display = function() {
  push();
  translate(this.position.x, this.position.y);
  noStroke();
  fill(this.fcolor);
  ellipse(0, 0, 2 * this.radius, 2 * this.radius);
  pop();
}

function createCols(_url) {
  let slash_index = _url.lastIndexOf('/');
  let pallate_str = _url.slice(slash_index + 1);
  let arr = pallate_str.split('-');
  for (let i = 0; i < arr.length; i++) {
    arr[i] = '#' + arr[i];
  }
  return arr;
}
let noiseScale = 300;
let num = 300;
let particles_1 = [];
let particles_2 = [];
let particles_3 = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  background('#33658a');
  // background(187, 148, 87);
  for (let i = 0; i < num; i++) {
    particles_1[i] = new Particle(random(0, width), random(0, height));
    particles_2[i] = new Particle(random(0, width), random(0, height));
    particles_3[i] = new Particle(random(0, width), random(0, height));
  }
}

function draw() {
  noStroke();
 
  for (let i = 0; i < num; i++) {
    
    let r = map (i, 0,num,0.8,1.8);
    let alpha = map (i, 0,num,0,200);

    // fill(111, 29, 27,alpha);
    fill(134, 187, 216,alpha);
    particles_1[i].move();
    particles_1[i].display(r);
    particles_1[i].edges();
    
    // fill(67, 40, 24,alpha);
    fill(246, 174, 45,alpha);
    particles_2[i].move();
    particles_2[i].display(r);
    particles_2[i].edges();
    
    // fill(153, 88, 42,alpha);
    fill(242, 100, 25,alpha);
    particles_3[i].move();
    particles_3[i].display(r);
    particles_3[i].edges();
  }
}

function Particle(x, y) {
  this.dir = createVector(0, 0);
  this.vel = createVector(0, 0);
  this.pos = createVector(x, y);
  this.speed = 0.4;

  this.move = function() {
    let angle = noise(this.pos.x / noiseScale, this.pos.y / noiseScale) * TWO_PI*noiseScale;
    this.dir.x = cos(angle);
    this.dir.y = sin(angle);
    this.vel = this.dir.copy();
    this.vel.mult(this.speed);
    this.pos.add(this.vel);

  }

  this.edges = function() {
    if (this.pos.x < 0 || this.pos.x > width || this.pos.y < 0 || this.pos.y > height) {
      this.pos.x = random(0,width);
      this.pos.y = random(0,height);
    }
  }

  this.display = function(r) {
    ellipse(this.pos.x, this.pos.y, r, r);
  }

}
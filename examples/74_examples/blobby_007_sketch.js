let num = 200;
let yoff = 0;
let t =0;

function setup() {
  createCanvas(windowWidth, windowHeight);
}

function draw() {
  blendMode(BLEND);
  background(0);
 blendMode(ADD);
  noStroke();
  translate(width/2,height/2);
   fill(255, 0, 0);
  bobby(noise(t/2)*200-100,noise(t/2+1)*200-100,1,80);
    fill(0, 255, 0);
   bobby(noise(t/4+4)*200-100,noise(t/2+3)*200-100,2,80);
    fill(0, 0, 255);
   bobby(noise(t/4+6)*200-100,noise(t/2+5)*200-100,3,80)
  t+=0.001;
}

function bobby(xPos,yPos,zoff,radium) {
  let xoff = 0;

  push();
    beginShape();
  for (let a = 0; a < num; a += 0.1) {
    let offset = map(noise(xoff, yoff,zoff), 0, 1, -25, 25);
    let r = radium + offset;
    let x = r * cos(a)+xPos;
    let y = r * sin(a)+yPos;
    curveVertex(x,y);
    xoff+=0.08;
    zoff+=0.005;
  }
  endShape();
  pop();
  

  yoff += 0.01;


}
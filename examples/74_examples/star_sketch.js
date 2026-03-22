function setup() {
  createCanvas(windowWidth, windowHeight);


}

function draw() {
  blendMode(BLEND);
  background(255);
  blendMode(MULTIPLY);

  translate(width / 2, height / 2);
  fill(0,150,240);
  star(5);
  fill(240,0,240);
  star(-5);

}

function star(cNum){
   push();
  beginShape();
  let yoff = 0;
  for (let a = 0; a < TWO_PI; a += 0.01) {
      let xoff = 0;
    let offset = map(sin(a*cNum+frameCount*0.05), -1, 1, -10, 50);
    let r = 160+offset;
    let x = r*cos(a);
    let y = r*sin(a);
    noStroke();
   vertex(x,y);
    xoff += 0.1;
  }
  endShape();
  pop();
  yoff += 0.1;
}
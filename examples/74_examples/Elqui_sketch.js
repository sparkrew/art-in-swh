let starPoints = 1;
let desertColor = '#FFFFFF';
let radiusOne = 2;
let radiusTwo = 2;

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(220)
  
}


// STAR FUNCTION: from the p5 references
function star(x, y, radius1, radius2, npoints) {
  let angle = TWO_PI / npoints;
  let halfAngle = angle / 2.0;
  beginShape();
  for (let a = 0; a < TWO_PI; a += angle) {
    let sx = x + cos(a) * radius2;
    let sy = y + sin(a) * radius2;
    vertex(sx, sy);
    sx = x + cos(a + halfAngle) * radius1;
    sy = y + sin(a + halfAngle) * radius1;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}


function draw() {
  //fences()
  
 fill(desertColor)
  if (mouseIsPressed){
    star(mouseX, mouseY, radiusOne, radiusTwo, starPoints)
  }

  
  if(keyIsDown(RIGHT_ARROW)){
    starPoints += 1;
  }else if (keyIsDown(LEFT_ARROW) && starPoints>1) {
    starPoints -= 1;
  }else if (keyIsDown(65)&& radiusOne>1){
    console.log("Se apreta tecla")
    radiusOne -= 1
  }
  else if (keyIsDown(83)&& radiusOne>=1){
    console.log("Se apreta tecla")
    radiusOne += 1
  }
  else if (keyIsDown(81)&& radiusTwo>1){
    console.log("Se apreta tecla")
    radiusTwo -= 1
  }
  else if (keyIsDown(87)&& radiusTwo>=1){
    console.log("Se apreta tecla")
    radiusTwo += 1
  }
  
}

function keyPressed() {
  switch (keyCode){
    case 49:
      desertColor = '#63474D';
      break;
    case 50:
      desertColor = '#AA767C';
      break;
    case 51:
      desertColor = '#D6A184';
      break;
    case 52:
      desertColor = '#FFA686';
      break;
    case 53:
      desertColor = '#FEC196';
      break;
    case 0:
      desertColor = '#FFFFFF';
  }

}

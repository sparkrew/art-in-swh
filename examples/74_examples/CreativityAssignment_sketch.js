
function setup() {
  createCanvas(windowWidth, windowHeight);
  background(0)
  textSize(width / 8);
  textAlign(CENTER, CENTER);
  
  const randomWidth = random(windowWidth)
  const randomHeight = random(windowHeight)


  noFill();
  
  strokeWeight(2)
  
  
  for(let i=0; i<25; i++){
    strokeWeight(i/4)
    stroke(255-(20*i), 0, 250);
    bezier(0, 0, randomHeight*i, 10+i, 90+i, 90+i, 0, windowHeight);
    stroke(0, 255-(10*i), 200);
    bezier(0, 0, randomWidth*i, randomHeight*i, 120+10*i, 10*i, windowWidth, 0);
    stroke(255-(20*i), i*20,0);
    bezier(0, windowHeight, randomHeight*i, i, 120+i, 10+i, windowWidth, windowHeight);
  }
  
  fill(255)
  stroke(0)
  strokeWeight(0)
  text('Creativity', windowWidth/2, windowHeight/2);
  
  noFill();
  
  strokeWeight(1)
  for(let i=0; i<25; i++){
    stroke(100, i*20,100);
    strokeWeight(i/4)
    bezier(windowWidth, 0, randomWidth*i, i, randomHeight+i, 10+i, windowWidth, windowHeight);
  }
  
}

function piramids(bottom, top){
  for(let i=0; i<windowHeight+1000; i+=30){
    fill(255, 255, 0, 200)
    triangle(i, bottom*windowHeight/10, i, top*windowHeight/10, 81+i, bottom*windowHeight/10);

    fill(255, 0, 255, 200)
    triangle(i, bottom*windowHeight/10, i+30, top*windowHeight/10, 81+i, bottom*windowHeight/10);
  }
}

function inversePiramids(bottom, top){
  for(let i=0; i<windowHeight+1000; i+=30){
    fill(255, 0, 255, 200)
    triangle(i, bottom*windowHeight/10, i, top*windowHeight/10, 81+i, bottom*windowHeight/10);

    fill(255, 255, 0, 200)
    triangle(i, bottom*windowHeight/10, i+30, top*windowHeight/10, 81+i, bottom*windowHeight/10);
  }
}


function draw() {
  
  
  strokeWeight(0)
  inversePiramids(0,1)
  
  piramids(10,9)
  
  fill(0)
  stroke(0)
  strokeWeight(0)
  
  textSize(width / 20);
  text('what is', 1*windowWidth/10, 0.5*windowHeight/10);
  
  fill(0,255,255)
  text('what is', 1.03*windowWidth/10, 0.53*windowHeight/10);
  
  
  textSize(width / 8);
  
  
}
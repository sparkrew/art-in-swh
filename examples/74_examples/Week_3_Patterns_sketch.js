let angle = 0.0
let speed = 0.05

function setup() {
  createCanvas(700, 700);
  rectMode(CENTER)
}


function draw() {
  
  background(0);
  
  translate(width/2, height/2)
  

  rotate(angle/10)
  for (let i = 50; i < 700; i += 40) {
      rotate(-angle/100)
    for (let j = 50; j < 700; j += 40) {
      rotate(angle/300)
      push()
 
      noFill()
      stroke(mouseX - i, i, mouseY - j)  //color
      strokeWeight(3)
      
      shearY(3.0)
      shearX(2.0)
    
      let d = dist(700, 700, i +width/2, j +height/2)
      
      let r = d/5
      
      ellipse(i, j, r - 20, r - 20)

      ellipse(i, j, r, r)     
      
      pop()
      
      angle+=0.0003
    }
  }
}
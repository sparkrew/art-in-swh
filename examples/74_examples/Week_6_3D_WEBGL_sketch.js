function setup() {
  createCanvas(400, 400, WEBGL);
  img = loadImage('Galaxys.jpg'); //texture
}

function draw() {
  background(0);
  
  
  push();
  //ambientLight(205, 0, 0);
  rotateZ(frameCount - 0.01);
  //rotateX(frameCount * 0.01);
  rotateY(frameCount * 0.01);
  texture(img);
  box(25);
  pop();
  
  push();
  ambientLight(225, 225, 0); //light (supposed to be yellow)
  
  translate(69, 0)
  //normalMaterial();  //color
  rotateZ(frameCount + 0.5);
  rotateX(frameCount * 0.05);
  rotateY(frameCount * 0.05);
  sphere(10, 20);
  pop();
  
  

  push();
  ambientLight(225, 225, 0);
  
  translate(0,-100)
  //normalMaterial();  //color
  rotateZ(frameCount + 0.05);
  rotateX(frameCount * 0.05);
  rotateY(frameCount * 0.05);
  sphere(10, 20);
  pop();
  
  
  
  push();
  ambientLight(225, 225, 0);
  
  translate(0,100)
  //normalMaterial();  //color
  rotateZ(frameCount * 0.05);
  rotateX(frameCount * 0.05);
  rotateY(frameCount * 0.05);
  sphere(10, 20);
  pop();
  
  
  
  push();
  ambientLight(225, 225, 0);
  
  translate(-69,0)
  //normalMaterial();  //color
  rotateZ(frameCount + 0.05);
  rotateX(frameCount * 0.05);
  rotateY(frameCount * 0.05);
  sphere(10, 20);
  pop();
  
  
  
  //normalMaterial();  //color
  push();
  normalMaterial();  //color
  rotateZ(frameCount * 0.01);
  rotateX(frameCount * 0.01);
  rotateY(frameCount * 0.01);
  torus(90, 2);
  pop();
  
  push();
  normalMaterial();  //color
  rotateZ(frameCount * 0.03);
  rotateX(frameCount * 0.03);
  rotateY(frameCount * 0.03);
  torus(75, 2);
  pop();
  
  push();
  normalMaterial();  //color
  rotateZ(frameCount * 0.02);
  rotateX(frameCount * 0.02);
  rotateY(frameCount * 0.02);
  torus(85, 2);
  pop();
  
  
  push();
  normalMaterial();  //color
  rotateZ(frameCount * 0.04);
  rotateX(frameCount * 0.04);
  rotateY(frameCount * 0.04);
  torus(98, 2);
  pop();
  
  
  push();
  normalMaterial();  //Material
  rotateZ(frameCount * 0.05);
  rotateX(frameCount * 0.05);
  rotateY(frameCount * 0.05);
  torus(95, 2);
  pop();
  
  

  
}
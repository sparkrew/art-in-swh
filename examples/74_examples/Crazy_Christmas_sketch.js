function preload() {
  tree = loadModel('Lowpoly_tree_sample.obj');
  tree2 = loadModel('lowpolytree.obj');
  treeImg = loadImage('green-color-leaves-pattern-free-vector.png');
}

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  stroke(100)
  video = createCapture(VIDEO);
  video.size(windowWidth, windowHeight);
  video.hide()
}

function draw() {
  if (!mouseIsPressed){
    background(0);
  }
  //background(0);
  //translate(-width/3, -height/2, 0);
  /*
  push()
  translate(-10, 10, 0);
  let dirX = (mouseX / width - 0.5) * 2;
  let dirY = (mouseY / height - 0.5) * 2;
  directionalLight(250, 250, 250, -dirX, -dirY, -1);
  for (let i = 0; i<10; i++){
    translate(10, -10, 0);
    
    normalMaterial();
    push();
    //rotateZ(frameCount * 0.01);
    //rotateX(frameCount * 0.01);
    rotateY(frameCount * 0.01);
    for (let i = 0; i<10; i++){
    translate(0, 10, 0);
    
    normalMaterial();
    push();
    //rotateZ(frameCount * 0.01);
    //rotateX(frameCount * 0.01);
    rotateY(frameCount * 0.01);
    
    //rotateY(map(mouseX, 0, width, PI/2, -PI/2))
    torus(30, 10);
  }
    
    //rotateY(map(mouseX, 0, width, PI/2, -PI/2))
    torus(40, 10);
  }
  pop()*/
  
  //translate(-10, 10, 0);
  let dirX = (mouseX / width - 0.5) * 2;
  let dirY = (mouseY / height - 0.5) * 2;
  directionalLight(250, 250, 250, -dirX, -dirY, -1);
  let locX = mouseX - width / 2;
  let locY = mouseY - height / 2;
  
  pointLight(250, 250, 250, locX, locY, 50);
  shininess(10);
  
  push()
  normalMaterial();
  
  /*
  push()
     for (let i = 0; i<10; i++){
       translate(0, 10, 10)
       rotateY(frameCount * 0.01);
       cone(20, 40);
     }
  pop()*/
  
  texture(treeImg);
  textureMode(NORMAL);
  for (let i = 0; i<30; i++){
    
    
    //normalMaterial();
    push();
    rotateZ(frameCount * 0.01);
    //rotateX(frameCount * 0.01);
    rotateY(frameCount * 0.01);
    for (let i = 0; i<10; i++){
      translate(0, 10, 0);

      //normalMaterial();
      push();
      //rotateZ(frameCount * 0.01);
      //rotateX(frameCount * 0.01);
      rotateY(frameCount * 0.01);

      //rotateY(map(mouseX, 0, width, PI/2, -PI/2))
      //scale(1.1); 
      model(tree);
      
      push()
        translate(20, 20, 20)
        sphere(5)
      pop()


    }
    push()

      for (let j = 0; j<7; j++){

        normalMaterial();
        scale(1.5)
        translate(0, 10, 0);
        rotateX(frameCount * 0.01);
        model(tree2)
        scale(1)
      }
    pop()
    scale(1)
    //rotateY(map(mouseX, 0, width, PI/2, -PI/2))
    model(tree);

    texture(video);
    textureMode(NORMAL);
    sphere(30)

    texture(treeImg);
  textureMode(NORMAL);
    push()
    for (let i = 0; i<5; i++){
      specularMaterial(250);
        rotateX(frameCount * 0.05);
      rotateY(frameCount * 0.02);
      rotateZ(frameCount * 0.01);
        translate(20, 20, 20)
        sphere(5)
    }
    pop()
  }
  pop()
  
  
  
  
}
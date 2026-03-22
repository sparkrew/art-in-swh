var soundFile;
let flowerPositions = [];
let flowerScale = [];
let redFlowerPositions = [];
let redFlowerScale = [];

let nombres = ["Ariana Maritza Bravo Aracena", "Bartolita del Carmen Paredes Castillo", "Pamela Verónica Fonseca Rebolledo", "Brenda Cartes Guzmán", "Mariana Ariela Milla Nuñez", "Yorka Gonzalez Barrera", "Herlin Montaño Valencia", "Estefanía Constanza Breve Neira", "Kimberly Ugalde Palma", "Damaris Ana Meliñir Llanqui", "Norma Jeannette Quiroga Zúñiga", "Valeria Esmeralda Ortiz Oyarzún", "Carolina Ortega Cariqueo", "Michelle", "Valentina", "Carmen Rosa González Valdés", "Rosa Nélida Muñoz Antonapai", "Franshesca Tamara González Miranda", "María Teresa Sepúlveda Smith", "Stephanie Emilien", "Rosa Francisca Millanao Chule", "Paulina Alejandra Gatica González", "Maylin Rachel Guevara Guevara", "Catalina", "Jocelyn", "Laura Norma Maldonado Solís", "Yaritza Navarro González", "Gloria Yanet Labraña Aros", "Willianyis Rojas Rosales", "A.C.Contreras V.", "Verónica del Carmen Palacios Tapia", "María de Jesús Bermúdez Fuentes", "María Amparo Velásquez Garcés", "Mónica Astorga Vega", "Jéssica del Carmen González Toledo", "Jessica Angelina Ortiz Cisternas", "Verónica Cuero Cuero", "Madely Padilla Martínez", "Marjorie Caris Aillal ", "Olga del Tránsito Poblete Campos", "Jeanette de las Mercedes Sepulveda Curín", "Pamela Solange Álvarez Soto", "Rosa Fritis Barraza", "Gabriela Machicado Hurtado"]


let cloudPositions = [[-70 , -150 , 140], [-1000 , -150 , 70], [-100 , -100 , 100], [-70 , 70 , 70]];
var x = 0;
var y = 0;

var n_a_femicides = 163;
var n_femicides = 44;

let inconsolata;


function preload() {
  flower = loadModel("assets/12973_anemone_flower_v1_l2.obj");
  grass = loadModel("assets/10450_Rectangular_Grass_Patch_v1_iterations-2.obj");
  
  cloud = loadModel("assets/Cloud model.obj");

  flowerImg = loadImage("assets/12973_anemone_flower_diff.jpg");
  redFlowerImg = loadImage("assets/redFlower-1.jpg");
  grassImg = loadImage("assets/10450_Rectangular_Grass_Patch_v1_Diffuse.jpg");

  soundFile = loadSound("assets/clairdelune.mp3");
  inconsolata = loadFont('assets/Inconsolata.otf');
  
}

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);

  amplitude = new p5.Amplitude();
  soundFile.play();

  amplitude.setInput(soundFile);
  amplitude.smooth(0.9);

  fft = new p5.FFT();

  peakDetect = new p5.PeakDetect(20, 400, 0.2);
  normalMaterial();
  
  textFont(inconsolata);
  textSize(width / 40);
  textAlign(CENTER, CENTER);
  
  y = -width
  for (i = 0; i < 5; i++){
    cloudPositions.push([random(-1000, 100), random(-1000, 100), random(50, 200)])
  }
  
  
  noCursor()
}

function draw() {
  background(0, 100, 255);
  //normalMaterial()
  noStroke();
  x++;
  y += 0.2;
  
  if (y > width){
    y = -width
  }

  orbitControl(0.5, 0.5, 0.5);

  ambientLight(100);

  let dirX = mouseX / width - 0.5;
  let dirY = mouseY / height - 0.5;
  directionalLight(250, 250, 250, -dirX, -dirY, -1);

  let locX = mouseX - width / 2;
  let locY = mouseY - height / 2;

  pointLight(250, 250, 250, locX, locY, 50);

  let spectrum = fft.analyze();

  fft.analyze();
  peakDetect.update(fft);

  if (peakDetect.isDetected) {
    if (n_a_femicides > 0) {
      //console.log("red");
      redFlowerPositions.push([random(-150, 150), random(-140, 220), -40]);
      redFlowerScale.push(random(0.5, 2));

      n_a_femicides -= 1;
    } else if (n_femicides > 0) {
      //console.log("white");
      flowerPositions.push([random(-150, 150), random(-140, 220), -40]);
      flowerScale.push(random(1.5, 2.5));
      n_femicides -= 1;
    } 
  }
  
  if (n_femicides == 0 && n_a_femicides == 0){
    push()
    translate(0, 200, 0)
    text("In 2021, there were 163 attempted femicides and 44 consumed femicides in Chile. NO ESTAMOS TODAS.",  -width/2, 0, width)
    pop()
    for (let i = 0; i < flowerPositions.length; i++){
      push()
      translate(0, -200, 100)
      translate(flowerPositions[i][0],
      flowerPositions[i][1],
      flowerPositions[i][2])
      textSize(width / 100);
      text(nombres[i], 0, 0)
      pop()
    }
  }

  push();
  translate(0, 0, -100);
  rotateX(PI / 3);
  scale(1.5);
  //plane(400);
  texture(grassImg);
  textureMode(NORMAL);
  model(grass);
  pop();

  for (let i = 0; i < flowerPositions.length; i++) {
    push();
    rotateX(PI / 3);
    rotateZ(PI);
    texture(flowerImg);
    textureMode(NORMAL);
    translate(
      flowerPositions[i][0],
      flowerPositions[i][1],
      flowerPositions[i][2]
    );
    scale(flowerScale[i]);
    //rotateZ(PI)
    model(flower);

    pop();
  }

  for (let i = 0; i < redFlowerPositions.length; i++) {
    push();
    rotateX(PI / 3);
    rotateZ(PI);
    texture(redFlowerImg);
    textureMode(NORMAL);
    translate(
      redFlowerPositions[i][0],
      redFlowerPositions[i][1],
      redFlowerPositions[i][2]
    );
    scale(redFlowerScale[i]);
    //rotateZ(PI)
    model(flower);

    pop();
  }

  push();
  translate(-width / 2, -height / 2, 0);
  shininess(300);
  fill(255, 255, 0);
  translate(mouseX, mouseY, 50);
  sphere(20);
  pop();

  shininess(200);

  fill(0, 255, 0);
  
  for (let i = 0; i < cloudPositions.length; i ++){
    push()
      rotateX(PI/3)
      rotateZ(PI/3)
      fill(255, 255, 255, 100)
      translate( cloudPositions[i][0], cloudPositions[i][1]+ y, cloudPositions[i][2])

      model(cloud);
    pop()
  }
 
}

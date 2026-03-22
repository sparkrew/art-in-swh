function setup() {
  createCanvas(800, 800);
  
  background(0);

  
  for (let i = 0; i < 100; i++) {
    var x = random(0, 800);
    var y = random(0, 800);
    var r = 5;
    fill("yellow");
    circle(x, y, r);
  }
  
  for (let i = 0; i < 200; i++) {
    var l = random(0, 800);
    var z = random(0, 800);
    fill("white");
    circle(l, z, 5);
  }
  

  
  fill(192,192,192);
  circle(100, 100, 150);
  fill(40, 122, 184);
  arc(400, 900, 600, 500, PI, 0, CHORD);
  
  fill(52, 165, 111);
  circle(184, 770, 60);
  
  fill(255);
  circle(600, 400, 60);
  fill(52, 165, 111);
  circle(457, 770, 200);
  
  fill(105,105,105);
  circle(136,110, 40);
  fill(105,105,105);
  circle(64, 125, 60);
  circle(100, 41, 30);
  
  
  stroke("white");
  strokeWeight(3);
  line(607, 388, 412, 127);
  line(588, 401, 325, 326);
  line(577, 377, 370, 210);
  
  stroke("blue");
  strokeWeight(3);
  line(593, 371, 445, 84);
  line(570, 395, 273, 336);
  line(570, 395, 348, 244);
  line(593, 371, 378, 178);
  
  stroke("cyan");
  line(392, 371, 349, 354);
  line(517, 175, 525, 206);
  line(388, 311, 415, 335);
  line(459, 318, 500, 324);
  line(574, 257, 585, 286);
  line(542, 388, 484, 387);
  line(534, 261, 554, 314);
  
  stroke("grey");
  
  textSize(32);
  fill(255);
  text("The Starry Sky", 561, 50);
}

function draw() {
  // text("x: " + mouseX,10,20); // displays the mouse's x location
  // text("y: " + mouseY,10,40); // displays the mouse's y location
  // stroke("white");
}
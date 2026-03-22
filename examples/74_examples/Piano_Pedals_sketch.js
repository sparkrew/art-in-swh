let allOscs = [];
let oscType = "sine";
let oscCount = 5;
let upDown = "none";

function setup() {
  background(255);
  noStroke();
  fill(0);
  createCanvas(windowWidth, windowHeight);
  textAlign(CENTER, CENTER);
}
function draw() {
  background(0);
  //text("click to create an oscillator", width/2, height/2);
  if (frameCount % 30 == 0) {
    for (let i = 0; i < allOscs.length; i++) {
      allOscs[i].pan(map(mouseX, 0, width, -1, 1));
      if (upDown == "up") {
        allOscs[i].freq(allOscs[i].getFreq() + 10, 0.7);
      } else if (upDown == "down") {
        allOscs[i].freq(allOscs[i].getFreq() - 10, 0.7);
      }
      
    }
  }
  for (let i = 0; i < allOscs.length; i++) {

    line(map(allOscs[i].getFreq(), 100, 1200, 0, width), 0, map(allOscs[i].getFreq(), 100, 1200, 0, width), height)
  }
  
}

function keyPressed(e) {
  if (
    e.key != "1" &&
    e.key != "2" &&
    e.key != "3" &&
    e.key != "4" &&
    e.key != "6" &&
    e.key != "7" &&
    e.key != "8"
  ) {
    let osc = new p5.Oscillator();
    osc.setType(oscType);
    osc.freq(map(keyCode, 65, 90, 100, 1000));
    stroke(255);
    line(
      map(keyCode, 65, 90, 0, width),
      0,
      map(keyCode, 65, 90, 0, width),
      height
    );
    osc.amp(0.05);
    osc.start();
    allOscs.push(osc);
  }

  switch (e.key) {
    case "a":
      for (let i = 0; i < allOscs.length; i++) {
        allOscs[i].freq(allOscs[i].getFreq(), 0.7);
        allOscs[i].amp(0, 0.1, 0.7);
        //allOscs[i].stop();
      }
      allOscs = []
      background(0);
      break;
    case "1":
      oscType = "square";
      break;
    case "2":
      oscType = "sine";
      break;
    case "3":
      oscType = "sawtooth";
      break;
    case "4":
      oscType = "triangle";
      break;
    case "6":
      upDown = "none";
      break;
    case "7":
      upDown = "up";
      break;
    case "8":
      upDown = "down";
      break;
  }
}

function mousePressed() {
  let osc = new p5.Oscillator();
  osc.setType(oscType);
  osc.freq(map(mouseX, 0, width, 100, 1200), map(mouseY, 0, height, 0.01, 1));
  // osc.freq(constrain(200 + 1000 *(mouseY / height), 200, 1200))
  stroke(255);
  line(mouseX, 0, mouseX, height);
  osc.amp(0.05, map(mouseY, 0, height, 0.01, 2));
  osc.start();
  allOscs.push(osc);
}

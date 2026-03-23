let facemesh;
let video;
let predictions = [];
let origins = {}
let [lastX, lastY] = [0,0];
let frameCounts = 0;
let pointCount = 0;


let mode = "other";

function setup() {
  createCanvas(640, 480);
  video = createCapture(VIDEO);
  video.size(width, height);

  facemesh = ml5.facemesh(video, modelReady);

  // This sets up an event that fills the global variable "predictions"
  // with an array every time new predictions are made
  facemesh.on("predict", results => {
    predictions = results;
  });

  // Hide the video element, and just show the canvas
  video.hide();
}

function modelReady() {
  console.log("Model ready!");
}

function draw() {
  image(video, 0, 0, width, height);

  // We can call both functions to draw all keypoints
  drawKeypoints();
  
}


function keyPressed() {
  if (mode === "mask") {
    mode = "lines";
  } else if (mode === "other"){
    mode = "mask";
  }else {
    mode = "other";
  }
}

// A function to draw ellipses over the detected keypoints
function drawKeypoints() {
  
  for (let i = 0; i < predictions.length; i += 1) {
    const keypoints = predictions[i].scaledMesh;

    // Draw facial keypoints.
    for (let j = 0; j < keypoints.length; j += 1) {
      
      const [x, y] = keypoints[j];

      //line(x, y, lastX, lastY)
      fill(0, 255, 0);
      
      //[lastX, lastY] = [x, y]
      
      
      if (mode == "mask"){
        //stroke(map(x, 0, width, 0, 255), map(y, 0, height, 0, 255), 0);
        line(x, y, map(x, 0, width, mouseX -300, mouseX+300), map(y, 0, width,  mouseY -300, mouseY+300))
      fill(map(x, 0, width, 0, 255), map(y, 0, height, 0, 255), 0);
      ellipse(map(x, 0, width, mouseX -300, mouseX + 300), map(y, 0, width,  mouseY -300, mouseY+300), 7, 7);
        
      }else if (mode == "lines"){
        pointCount += 1;
        //stroke(map(x, 0, width, 0, 255), map(y, 0, height, 0, 255), 0);
        line(x, y, lastX, lastY);

        [lastX, lastY] = [x, y]
        
      }else{
        fill(220)
        quad(x, y, x+random(1,10), y, x+random(1,30), y+random(1,20), x, y+random(1,20))
        quad(x, y, x-random(1,10), y, x-random(1,30), y+random(1,20), x, y+random(1,20))
        //ellipse(x, y, 7, 7);
      }
      
    }
  }
  
}


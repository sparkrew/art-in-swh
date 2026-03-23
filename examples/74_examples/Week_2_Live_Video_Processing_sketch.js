let webCam;


function setup() {
  createCanvas(windowWidth, windowHeight);
  pixelDensity(1);
  webCam = createCapture(VIDEO);
  webCam.size(windowWidth, windowHeight);
  webCam.hide();
  noStroke();
  fill(0);
  
  

}

function draw() {
  background(255);
  webCam.loadPixels();
  stepSize = 4
  image(webCam, 0, 0, width, width * webCam.height / (webCam.width)/2);
  filter(INVERT);
  
//   webCam.loadPixels();
//   for(let y = 0; y < webCam.height; y+=10) {
//     // Visit every column of pixels
//     for(let x = 0; x < webCam.width; x+=10) {
//       // Get the color array [r,g,b,a] at x,y
//       let colorOfCamAtXY = webCam.get(x,y);
      
//       // Use that color as fill
//       //fill(colorOfCamAtXY);
      
//       // Extract the brightness level of the color
//       let b = brightness(colorOfCamAtXY);
//       // Test for a brightness threshold of 50
//       if(b > 50) fill('white');
//       else fill('black');
      
//       // Draw a 10x10 rectangle at x,y
//       rect(x, y, 10, 10);
//     }
//   }
  

  translate(width, 0);
  scale(-1, 1);
  image(webCam, 0, height/2, width, width * webCam.height / (webCam.width)/2);


  filter(INVERT);

  

  
}

let song;
let fft;
let degree = 10.0;
let dt = 0.1;


function preload() {
  song = loadSound("Sky.mp3");
}
function setup() {
  let cnv = createCanvas(400, 400);
  fft = new p5.FFT(0.9, 64);
  song.amp(0.4);
}
function mousePressed() {
  if (song.isPlaying()) {
    song.stop();
  } else {
    song.play();
  }
}

function analyze(r) {
  let spectrum = fft.analyze();
  fill(255);
  for (let i = 0; i < spectrum.length; i++) {
    
    let x = map(i, 0, spectrum.length, 0, height);
    
    let theta = map(i, 0, spectrum.length, 0, 2 * PI);
    
    let h = constrain(-height + map(spectrum[i], 0, 255, height, 0), -200, 200);
    
   
    if (h >= -20) h = -70;
   
    
    let xCoord = h * cos(theta);
    let yCoord = h * sin(theta);
    
    stroke(147, 112 , 219)
    fill(75, 0, 130)
    circle(xCoord, yCoord, 5); //tips
    strokeWeight(3);
    stroke(135, 206, 250); //lines
    line(0, 0, xCoord, yCoord);
    
    //shearX(2.0)
    //shearY(4.0)
    shearX(6.0)
    shearY(4.0)
  }

}

function waveform() {
  let r = 0;
  let lastR = 20; //changes circle size
  let waveform = fft.waveform();
  for (let i = 0; i < waveform.length; i++)
    if (r <= waveform[i]) r = waveform[i];
  let y = map(waveform[waveform.length - 1], -10, 10, 0, height);
  r = r * 500 + 100;
  analyze((r - lastR) * dt * 10);
  fill(147, 112, 219);
  circle(0, 0, (r - lastR) * dt * 5);//big circle
  lastR = r;
  
}


function waveform1() {
  let r = 0;
  let lastR = 20; //changes circle size
  let waveform = fft.waveform();
  for (let i = 0; i < waveform.length; i++)
    if (r <= waveform[i]) r = waveform[i];
  let y = map(waveform[waveform.length - 1], -10, 10, 0, height);
  r = r * 500 + 100;
  //analyze((r - lastR) * dt * 0);
  fill(147, 112, 219);
  circle(0, 0, (r - lastR) * dt * 3);//big circle
  lastR = r;
  
}


function waveform2() {
  let r = 0;
  let lastR = 20; //changes circle size
  let waveform = fft.waveform();
  for (let i = 0; i < waveform.length; i++)
    if (r <= waveform[i]) r = waveform[i];
  let y = map(waveform[waveform.length - 1], -100, 10, 0, width);
  r = r * 500 + 100;
  //analyze((r - lastR) * dt * 10);
  fill(147, 112, 219);
  circle(400, 400, (r - lastR) * dt * 3);//big circle
  lastR = r;
  
}


function waveform3() {
  let r = 0;
  let lastR = 20; //changes circle size
  let waveform = fft.waveform();
  for (let i = 0; i < waveform.length; i++)
    if (r <= waveform[i]) r = waveform[i];
  let y = map(waveform[waveform.length - 1], -100, 10, 0, width);
  r = r * 500 + 100;
  //analyze((r - lastR) * dt * 10);
  for (let i = 0; i < 10; i++) {
    var l = random(0, 400)
    var z = random(0, 400)
    fill(255);
    circle(l, z, (r - lastR) * dt * 0.5);//big circle
  }

  lastR = r;
  
}


function draw() {
  background(230, 230, 250);
  push();
  waveform1();
  waveform2();
  waveform3();
  translate(width / 2, height / 2);
  //translate(width, height)
  rotate(radians(degree));
  //rotate(radians(HALF_PI))
  waveform();
  waveform1();
  waveform2();
  degree++;
  pop();
  
  

}
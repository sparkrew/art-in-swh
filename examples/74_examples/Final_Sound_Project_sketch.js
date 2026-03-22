//songs
//Get It - Keshi
//The Search - NF
//Pure Sky - Genshin Impact

//Code inspired by therewasaguy and FilipaRita and a lot of p5.js references

let song;
let song2;
let song3;
let fft;
var button;
var button1;
var button2;

let w, a, d, r, g, b, x;

let dt = 0.1;
let degree = 0;
var smoothing = 0.8; // play with this, between 0 and .99
var binCount = 1024; // size of resulting FFT array. Must be a power of 2 between 16 an 1024
var particles =  new Array(binCount);

let slider;

function preload() {
  song1 = loadSound("NF.mp3");
  song2 = loadSound("keshi.mp3");
  song3 = loadSound("Sky.mp3");
  button = createButton('Song2');
  button.position(windowWidth/2 - 20, windowHeight - 100);
  button.mousePressed(toggleNext1);
  
  button1 = createButton("Song3");
  button1.position(windowWidth/2 + 80, windowHeight - 100);
  button1.mousePressed(toggleNext);
  
  button2 = createButton("Song1");
  button2.position(windowWidth/2 - 120, windowHeight - 100);
  button2.mousePressed(toggleNext2);
}

function setup() {
  createCanvas(windowWidth, windowHeight);


  fft = new p5.FFT(smoothing, binCount);
  fft = new p5.FFT();
  for (var i = 0; i < particles.length; i++) {
  var x = map(i, 0, binCount, 0, width * 2);
  var y = random(0, height);
  var position = createVector(x, y);
  particles[i] = new Particle(position);
  }
  
  slider = createSlider(0, 1, 0.1, 0.1);
  slider.position(windowWidth - 150, windowHeight - 100);
  slider.style('width', '80px');
  
}

function draw() {
  background(0);
  
  //noFill();
  noStroke();
  background(0, 0, 0, 100);

  var spectrum = fft.analyze(binCount);

  for (var i = 0; i < binCount; i++) {
    var thisLevel = map(spectrum[i], 0, 255, 0, 1);

    // update values based on amplitude at this part of the frequency spectrum
    particles[i].update( thisLevel );

    // draw the particle
    particles[i].draw();

    // update x position (in case we change the bin count while live coding)
    particles[i].position.x = map(i, 0, binCount, 0, width * 2);
    
    
  }
  
  
  
  
  //stroke(255, 230);
  //stroke(221, 160, 221);
  //stroke(255, 0, 0);
  stroke(a, w, d);
  //noFill();
  //lines
  //noStroke();
  strokeWeight(4);

  translate(width / 2, height / 2);
  angleMode(DEGREES);

  //fill(0, 191, 255);
  fill(r, g, b);
  let circle = fft.waveform();
  
  for (let t = -1; t <= 1; t += 2) {
    
    beginShape();

    for (let i = 0; i <= 180; i += 0.1) {
      let index = floor(map(i, 0, 180, 0, circle.length));

      let r = map(circle[index], -1, 1, -5, 150);
      let x = r * sin(i) * t;
      let y = r * cos(i);
      vertex(x, y);
    }
    endShape();
  }
  
  let val = slider.value();
  song1.setVolume(slider.value());
  song2.setVolume(slider.value());
  song3.setVolume(slider.value());
}



var Particle = function(position) {
  this.position = position;
  this.scale = random(0, 0.1);
  this.speed = createVector(0, random(0, 10) );
  //this.color = [random(0, 255), random(0,255), random(0,255)];
  this.color = [random(0, 80),random(0, 255), random(200, 255)];
  //this.color = [random(a, r), random(w, g), random(d, b)];
  //this.color = [255];
  // function toggleNext() {
  //   this.color = [255];
  // }

}

var theyExpand = 1;

// use FFT bin level to change speed and diameter
Particle.prototype.update = function(someLevel) {
  this.position.y += this.speed.y / (someLevel*2);
  if (this.position.y > height) {
    this.position.y = 0;
  }
  this.diameter = map(someLevel, 0, 1, 0, 100) * this.scale * theyExpand;

}


Particle.prototype.draw = function() {
  fill(this.color);
  ellipse(
    this.position.x, this.position.y,
    this.diameter, this.diameter
  );
}

//color
function mousePressed() {
  // Check if mouse is inside the circle
  let d = dist(mouseX, mouseY, windowWidth/2, windowHeight/2);
  if (d < 100) {
    // Pick new random color values
    r = random(255);
    g = random(255);
    b = random(255);
    x = 255;
  }
}


function toggleNext1() {
  //let d = dist(mouseX, mouseY, windowWidth/2 - 20, windowHeight - 100 )
  //if (d < 50) {
      a = 255;
      r = 128;
      w = 0;
      g = 0;
      d = 0;
      b = 128;
    if (song1.isPlaying()) {
      song1.pause();
      button.html("Song2")

      
    }
    else {
      song1.play();
      button.html("Pause")
    }
    //}
}

function toggleNext() {
  r = 0;
  g = 191;
  b = 255;
  
  a = 230;
  w = 230;
  d = 250;
  if(song3.isPlaying()) {
    song3.pause();
    button1.html("Song3");
  }
  else {
    song3.play();
    button1.html("Pause")
  }
}

function toggleNext2() {
  r = 255;
  g = 255;
  b = 224;
  
  a = 106;
  w = 90;
  d = 205;
  
  if (song2.isPlaying()) {
    song2.pause();
    button2.html("Song1");
  }
  else {
    song2.play();
    button2.html("Pause");
  }
    
}

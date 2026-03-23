//Leon Chen Week 4: Sound
//Play button to play the song and Volume and Speed sliders to change up the speed and amplitutde to see change on canvas
//Audio File is called Pure-Sky from Genshin Impact

let slider;
let slider1;
let song;
let amp;
let fft;

function preload() {
  song = loadSound('Sky.mp3')
  //amp = new p5.Amplitude();
}

function setup() {
  createCanvas(400, 400);
  slider = createSlider(0.0, 2.0, 0.2, 0.1);
  slider.position(0, 450);

  label = createDiv('Volume')
  label.position(0, 435);
  
  slider1 = createSlider(0.1, 4.0, 1.0, 0.1 );
  slider1.position(0, 495)
  
  label = createDiv('Speed')
  label.position(0, 480);
  
  
  
  button = createButton('Play')
  button.position(0, 405)
  button.mousePressed(Play)
  
 
  fft = new p5.FFT();
  fft.setInput(song)
  
  
}

function draw() {
  background(0);
  
  song.setVolume(slider.value());
  //song.setSpeed(slider1.value());
  
  speed = constrain(slider1.value(), 0.1, 4);
  song.rate(speed);
  
  
  let spectrum = fft.analyze()
  beginShape();
  for (i = 0; i < spectrum.length; i++) {
    vertex(i, map(spectrum[i], 0, 255, height, 0));
  }
  endShape();
  
  
}

function Play() {
    if (!song.isPlaying()) {
    song.play();
    button.html("Stop");

  } else {
    song.pause();
    button.html("Play");

  }
}
/*
Gurkirat Saini
gssaini
Rats (Remix by barbara_im)

Original: https://editor.p5js.org/gssaini117/sketches/rzAbNaPNd

Instructions: Simply move the mouse across the screen like a slider and enjoy. 

Music: https://www.youtube.com/watch?v=vdVnnMOTe3Q

The Remix!
by barbara_im -> Barbara Irarrazaval

Sounds from https://freesound.org/
Feel free to play with the patterns of the animal!
*/

let dogPattern = [1, 0, 0, 1, 0, 0]
let chickenPattern = [1, 0, 1, 0, 1, 0]
let catPattern = [1, 1, 0, 0, 1, 0]
let sheepPattern = [0, 1, 0, 1, 0, 1]
let part;
let isPlaying = false;

function preload() {
  rat = loadImage('assets/rat.png');
  mixtape = loadSound('assets/mixtape.mp3');
  
  dogsSound = loadSound('assets/24965__www-bonson-ca__bigdogbarking-02.wav');
  dog = loadImage('assets/dog-5276317_1280.webp');
  chickSound = loadSound('assets/316920__rudmer-rotteveel__chicken-single-alarm-call.wav');
  chicken = loadImage('assets/chik.png');
  sheepSound = loadSound('assets/34538__erdie__sheep.flac');
  sheep = loadImage('assets/sheep_PNG2718.png');
  catSound = loadSound('assets/4914__noisecollector__cat2.wav');
  cat = loadImage('assets/cat.png');
  
  cricketSound = loadSound('assets/337435__ev-dawg__cricket.wav');
  cricket = loadImage('assets/cricket_insect_PNG16.png');
  vinilSound = loadSound('assets/162493__tasmanianpower__vinyl-rewind.wav');
  oldSchoolSound = loadSound('assets/74522__laurencehr__pose1.mp3');
  peopleSound = loadSound('assets/23153__freqman__party-sounds2.wav');
}

function setup() {
  createCanvas(600, 400);
  mixtape.loop();
  ratAmp = new p5.Amplitude();
  ratAmp.setInput(mixtape);

  let dogPhrase = new p5.Phrase(dogsSound, playDog, dogPattern);
  let chickenPhrase = new p5.Phrase(chickSound, playChicken, chickenPattern);
  let catPhrase = new p5.Phrase(catSound, playCat, catPattern);
  let sheepPhrase = new p5.Phrase(sheepSound, playSheep, sheepPattern);
  part = new p5.Part();
  part.addPhrase(dogPhrase);
  part.addPhrase(chickenPhrase)
  part.addPhrase(catPhrase);
  part.addPhrase(sheepPhrase);
  part.setBPM(10);
  part.start(); 
  part.loop();

  //dogsSound.loop()
  //dogsSound.amp(1)
  dogAmp = new p5.Amplitude();
  dogAmp.setInput(dogsSound)
  //chickSound.loop()
  //chickSound.amp(0.5)
  chickAmp = new p5.Amplitude();
  chickAmp.setInput(chickSound)
  //sheepSound.loop()
  //sheepSound.amp(1.2)
  sheepAmp = new p5.Amplitude();
  sheepAmp.setInput(sheepSound)
  //catSound.loop()
  //catSound.amp(0.5)
  catAmp = new p5.Amplitude();
  catAmp.setInput(catSound)
  
  cricketAmp  = new p5.Amplitude();
  cricketAmp.setInput(cricketSound);
  cricketSound.amp(30)
    

  
}

function draw() {
  background(220);
  //mouseX controls volume
  let volume = map(mouseX, 0, width, 0, 1);
  volume = constrain(volume, 0, 1);
  mixtape.amp(volume);
  // controls the rat in relation to the mouse
  let ratWidth = mouseX+50;
  let ratHeight = ratAmp.getLevel() * height + ratWidth*2/3;
  
  
  
  image(dog, 0, 0, width/4, animalHeight(dogAmp))
  image(chicken, width/4, 0, width/4, animalHeight(chickAmp))
  image(cat, 2*width/4, 0, width/4, animalHeight(catAmp))
  image(sheep, 3*width/4, 0, width/4, animalHeight(sheepAmp))
  
  image(rat, mouseX-ratWidth/2, height/2-ratHeight/2, ratWidth, ratHeight);
  
  text("Some commands:", width/8, 6.5*height/8);
  text("p: people, c: crickets, v: vinil in reverse, o: some old school music ;)", width/8, 7*height/8);
}


function keyPressed(e) {
  if (e.key == 'c') {
    cricketSound.play();
  } else if(e.key == 'o'){
    oldSchoolSound.play();
  }else if(e.key=="v"){
    vinilSound.play();
  }else if(e.key == "p"){
    peopleSound.play()
  }else {
    value = 0;
  }
}

function animalHeight(amp){
  return amp.getLevel() * height + width/4*2/3;
}

function playDog(time, rate) {
  dogsSound.rate(rate);
  dogsSound.play(time);
}

function playCat(time, rate) {
  catSound.rate(rate);
  catSound.play(time);
}


function playSheep(time, rate) {
  sheepSound.rate(rate);
  sheepSound.play(time);
}


function playChicken(time, rate) {
  chickSound.rate(rate);
  chickSound.play(time);
}

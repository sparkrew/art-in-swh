let sourceText = "Sleep";
let source1 = "Time"
let source2 = "Money"
let source3 = "Happiness"

const word = "stress"

function setup() {
  createCanvas(700, 700);
  frameRate(100);
  font = textFont('ZCOOL QingKe HuangYou');
}

function draw() {
  background(0);
  
  //font = textFont('ZCOOL QingKe HuangYou');
  textSize(100);
  fill(255)
  textLeading( (mouseX / height) * 100);
  textSize(50)
  fill(187, 161, 79)
  text("Things That I Want More In My Life", width/2 - 100, height/32, 100)
  fill(225, 0, 0)
  
  textAlign(CENTER, CENTER);
  let middle = sourceText.length / 2;
  let left = middle - ((mouseX / width) * middle);
  let right = middle + ((mouseX / width) * middle);
  text(
    sourceText.substring(left, right+1),
    100, 100);
  text(
    source1.substring(left, right+1),
    175, 500);
  text(
    source2.substring(left, right+1),
    575, 300);
  text(
    source3.substring(left, right+5),
    600, 600);
  
  for(let i = 0; i<20; i++){
  const rand = int(random(0, word.length-1));
  fill(255);
  textSize(random(5, 50));
  text(word, random(width), random(height));
  
  }
}

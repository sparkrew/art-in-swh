let lines
let spacewidth = 6
let wordHeight = 20

function preload() {
  poem1 = loadStrings('cronos.txt') 
  poem2 = loadStrings('poesiaMorira.txt')
  poem3 = loadStrings('test.txt')
  
  lines = random([poem1, poem2, poem3])
  
}

function setup() {
  createCanvas(600, 800)
  //noLoop()
  fontsToChoose = random(['Anton', 'Shizuru', 'Cinzel'])
  textFont(fontsToChoose);
}

function draw() {
  
  background(50)
  textSize(wordHeight)
  fill(255)
  //textAlign(LEFT, TOP)
  
  for (let i = 0; i < lines.length; i ++ ) {
    let prevMod = 0
    var doc = window.nlp(lines[i])
    let textToPrint = doc

    
    let words = lines[i].split(" ")
    /* if (lines[0] == "Qué es un antipoeta:"){
      //text(words[j], 25 + offset, 25 + i * 20)
      
      //createCheckbox(lines[i], false);
    } */
    // Word by word rendering
    let offset = 0
    for (let j = 0; j < words.length; j++) {
       //prevMod += cos(random()) * 4
       let wordwidth = textWidth(words[j])

       //fill(128 + 10 * i)
    
      
      
       
      if (mouseIsPressed && lines[0] == "En Santiago de Chile"){
      rect(25 + offset, 10 + i * 20, wordwidth, 18)
        
      heart(width/2, height/2, height/4)
    }else if (mouseIsPressed && lines[0] == "LA"){

      
      text("✝".repeat(words[j].length), 25 + offset, 25 + i * 20)
      heart(width/2, height/2, height/4)
    }else if (lines[0] == "Qué es un antipoeta:"){
      text(words[j], 25 + offset, 25 + i * 20)
      //createCheckbox(words.join(' '), false);
       
    }
      else{
      text(words[j], 25 + offset, 25 + i * 20)
    }
       
      offset += wordwidth + spacewidth
     }
    
    if (lines[0] == "Qué es un antipoeta:" && mouseY <25 + (i) * 20 && mouseY >25 + (i-1) * 20){
      text( "⇦", 25 + offset, 25 + i * 20)
    }
    
  }
}


// original heart from https://editor.p5js.org/Mithru/sketches/Hk1N1mMQg
function heart(x, y, size) {
  noFill()
  stroke(255)
  strokeWeight(3)
  beginShape();
  vertex(x, y);
  bezierVertex(x - size / 2, y - size / 2, x - size, y + size / 3, x, y + size);
  bezierVertex(x + size, y + size / 3, x + size / 2, y - size / 2, x, y);
  endShape(CLOSE);
  
  
  ellipse(x -height/15, y + height/15, 30, 55);
  
  ellipse(x +height/15, y + height/15, 30, 55);
  
  fill(255)
  ellipse(x +height/16, y + height/13, 15, 25);
  
  /*
  line(x+height/12, y+height/6+10, x+height/12+ 10, y+height/4+30)
  line(x+height/12+ 10, y+height/4+30, x+height/12+ 30, y+height/4+30)
  
  line(x+height/12, y+height/6+10, x+height/12+ 10, y+height/4+30)
  line(x+height/12+ 10, y+height/4+30, x+height/12+ 30, y+height/4+30)
  */
  
  noStroke()
  fill(255)
}

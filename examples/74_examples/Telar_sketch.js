let type = "cloth";
let stepSize = 16;

function setup() {
  createCanvas(windowWidth, windowHeight);
  video = createCapture(VIDEO);
  video.size(windowWidth, windowHeight);
  video.hide();
  background(0);
}

function draw() {
  video.loadPixels();
  if (type == "cloth") {
    tela();
  } else if (type == "beads") {
    beads();
  }
}

function keyPressed() {
  if (keyCode == 67) {
    type = "cloth";
  } else if (keyCode == 66) {
    type = "beads";
  }
}

function tela() {
  let W = video.width;
  let h = video.height;
  //image(video,0,0)
  let randomW = int(random(W));
  let randomW2 = int(random(W));
  let randomH = int(random(h));

  let randomH2 = int(random(h));
  let stitchSize = int(random(50));

  if (mouseIsPressed) {
    copy(video, randomW, 0, stitchSize, h, randomW2, 0, stitchSize, h);
    copy(video, 0, randomH, W, stitchSize, 0, randomH2, W, stitchSize);

    if (keyIsDown(49)) {
      filter(GRAY);
    } else if (keyIsDown(50)) {
      filter(INVERT);
    }

    video.updatePixels();
  }
}

function beads() {
  for (let y = 0; y < height; y += stepSize) {
    for (let x = 0; x < width; x += stepSize) {
      const i = (y * width + x) * 4;
      fill(
        video.pixels[i],
        video.pixels[i + 1],
        video.pixels[i + 2],
        video.pixels[i + 3]
      );
      circle(x, y, video.pixels[i] / 5);
    }
  }

  if (keyIsDown(38)) {
    stepSize += 1;
  } else if (keyIsDown(40) && stepSize > 1) {
    stepSize -= 1;
  }
}

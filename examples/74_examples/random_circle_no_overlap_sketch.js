let circles = [];
// const COL = createCols("https://coolors.co/ffcdb2-ffb4a2-e5989b-b5838d-6d6875");

const COL = createCols("https://coolors.co/1c2c4a-36558f-f9dc5c-ff6b6b-2a91db-5aa9e6-7fc8f8");


function setup() {
  createCanvas(windowWidth, windowHeight);
  background(255);

  // Lets make sure we don't get stuck in infinite loop
  let protection = 0;
  // Try to get to 500
  while (circles.length < 1500) {
    // js object, pick a random circle
    circle = {
      x: random(width),
      y: random(height),
      r: random(6, 36)
    };

    // Does it overlap any previous circles?
    let overlapping = false;
    for (j = 0; j < circles.length; j++) {
      let other = circles[j];
      let d = dist(circle.x, circle.y, other.x, other.y);
      if (d < circle.r + other.r) {
        overlapping = true;
      }
    }

    // if it's not overlapping then add to array
    if (!overlapping) {
      circles.push(circle);
    }

    // do not stuck
    protection++;
    if (protection > 8000) {
      break;
    }
  }

}

function draw(){
    // Draw all the circles
  for (i = 0; i < circles.length; i++) {
    noStroke();
  fill(COL[int(random(COL.length))]);
    ellipse(circles[i].x, circles[i].y, circles[i].r * 2, circles[i].r * 2);
  }
  noLoop();
}

function createCols(_url){
  let slash_index = _url.lastIndexOf('/');
  let pallate_str = _url.slice(slash_index + 1);
  let arr = pallate_str.split('-');
  for (let i = 0; i < arr.length; i++) {
    arr[i] = '#' + arr[i];
  }
  return arr;
}
let topLayer; // Top striped layer (starting with black)
let bottomLayer; // Bottom striped layer (starting with white)
let maskGraphics; // Graphics to create the circular mask
let stripeWidth = 20; // Width of each stripe

function setup() {
  createCanvas(1200, 600);
  // noLoop();

  // Create the top layer with black and white stripes (starting with black)
  topLayer = createGraphics(width, height);
  for (let x = 0; x < width; x += stripeWidth) {
    if ((x / stripeWidth) % 2 === 0) {
      topLayer.fill(0); // Black stripe
    } else {
      topLayer.fill(255); // White stripe
    }
    topLayer.noStroke();
    topLayer.rect(x, 0, stripeWidth, height);
  }

  // Create the bottom layer with black and white stripes (starting with white)
  bottomLayer = createGraphics(width, height);
  for (let x = 0; x < width; x += stripeWidth) {
    if ((x / stripeWidth) % 2 === 0) {
      bottomLayer.fill(255); // White stripe
    } else {
      bottomLayer.fill(0); // Black stripe
    }
    bottomLayer.noStroke();
    bottomLayer.rect(x, 0, stripeWidth, height);
  }

  // Create the circular mask
  maskGraphics = createGraphics(width, height);
  maskGraphics.noFill();
  maskGraphics.ellipseMode(CENTER);
}

function draw() {
  background(0);

  // Draw the bottom layer
  image(bottomLayer, 0, 0);

//   // Update the mask with a moving circle
  maskGraphics.clear(); // Clear previous frames
  maskGraphics.fill(255); // White area defines the visible part
  let circleX = mouseX;
  let circleY = mouseY;
  let circleDiameter = 150;
  maskGraphics.ellipse(circleX, circleY, circleDiameter);

  // Apply the mask to the top layer
  let maskedLayer = topLayer.get(); // Get a copy of the top layer
  maskedLayer.mask(maskGraphics);

  // Draw the masked top layer
  image(maskedLayer, 0, 0);
}

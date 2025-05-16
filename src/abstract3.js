let wd;
let ht;
function setup() {
    wd = 580;
    ht = 750;
    createCanvas(wd, ht);
}

// eye of a cat: cardioid
function draw() {
    // Dark background
    background(0);

    // Configuring the line
    strokeWeight(1);
    stroke(255, 204, 0);

    for (let posX = 0; posX < 100; posX++) {
        // x1 y1 x2 y2
        line(1, 1 + posX * 10, 1 + posX * 10, ht);
        line(1 + posX * 10, 1, ht, 1 + posX * 10,
        );
    }
}

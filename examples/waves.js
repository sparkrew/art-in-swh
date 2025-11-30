const RESOLUTION = 25;

function f(x, y) {
    const value = (sin(x) + cos(y));
    // const value = (x) + (y);
    return map(value, -1, 1, -TWO_PI, TWO_PI);
}

function setup() {
    createCanvas(700, 900);
    background(0);
    noLoop();
}

function draw() {
    for (let x = RESOLUTION / 2; x < width; x += RESOLUTION) {
        beginShape()
        for (let y = RESOLUTION / 2; y < height; y += RESOLUTION) {
            newX = x
            newY = y
            var angle = f(x, y)
            fill(10 * sin(angle))
            strokeWeight(10 * sin(angle) + 1)
            vertex(x + 10 * sin(angle), y + 10 * sin(angle))
            stroke(55, 123, 223)
        }
        endShape()
    }
}
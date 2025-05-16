var a, b, c, d;

function setup() {
    createCanvas(700, 900);
    background(0);
    // noLoop();
    a = 100;
    b = 200;
    c = 300;
    d = 0;
}

function draw() {
    background(0);
    rects(10, 10, 680, 880, 200);
}

function rects(x, y, w, h, stroke_col) {
    noFill()
    stroke(stroke_col)
    if (w < 10 || h < 10) {
        return;
    } else {
        rect(x, y, w, h);
        rects(x + 10, y + 15, w - 20, h - 20, stroke_col - 10);
    }

}
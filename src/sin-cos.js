let stroke_col = 200;

function setup() {
    wd = 580;
    ht = 750;
    createCanvas(wd, ht);
    background(20);
}

function draw() {
    let min = 2; // 2
    let max = 3; // 3
    let a = 0.1; // 1 | 0.5
    let b = 2; // 2 | 3
    let i_max = random(min, max);
    let j = random(min, max);
    for (let i = 1; i < i_max; i++) {
        graphFunction(x => a * x ** b + sin(i * x ** b), 0, 3 * PI);
    }
    noLoop();
}


// Not my code from here:
// Credits to https://www.youtube.com/watch?v=Q9Gje2vh22Q
function graphFunction(fn, x1, x2) {
    let o = getFunctionValues(fn, x1, x2, 5000); // genuary jan 16

    let values = o.values;
    let y1 = o.min;
    let y2 = o.max;

    drawGraph(values, x1, x2, y1, y2);
}

function drawGraph(values, x1, x2, y1, y2) {
    stroke(stroke_col);
    strokeWeight(1);

    for (let i = 0; i < values.length - 1; i++) {
        let x = values[i].x;
        let y = values[i].y;

        let screenX = map(x, x1, x2, 0, width - 1);
        let screenY = map(y, y1, y2, height - 1, 0);

        let xNext = values[i + 1].x;
        let yNext = values[i + 1].y;

        let screenXNext = map(xNext, x1, x2, 0, width - 1);
        let screenYNext = map(yNext, y1, y2, height - 1, 0);

        line(screenX, screenY, screenXNext, screenYNext);
    }
}

function getFunctionValues(fn, x1, x2, n) {
    let ar = [];
    let min = Infinity;
    let max = -Infinity;

    let step = (x2 - x1) / n;

    for (let x = x1; x <= x2; x += step) {
        let y = fn(x);
        ar.push({ x, y });

        if (y < min) {
            min = y;
        }

        if (y > max) {
            max = y;
        }
    }

    return { values: ar, min, max };
}
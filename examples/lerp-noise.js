/* BezierCurves

References:
https://www.youtube.com/watch?v=uctX1P3H3xM
https://editor.p5js.org/PeterQwertz/sketches/Mh7aSsyMl
*/

let pause = false
let x1, y1, x2, y2, x3, y3, x4, y4
let i = 30
let offset = 100
let speed = 0.005
let j1 = -110
let j2 = -110
let j3 = 100
let j4 = 100


function setup() {
    createCanvas(700, 900)
    background(0)
}

function draw() {
    // background(0)

    bezier_func(1)

    // Tests:
    // call_bezier(2)
}


function bezier_func(l) {
    // background(10, 10, 10, 100)
    noFill()
    strokeWeight(1)

    stroke(
        // 200, 0, 0, // red
        // 200, 200, 0, // yellow
        noise(offset + i) * 300,
        noise(offset + i * 2) * 300, // adds color
        noise(offset + i * 3) * 300, // adds color
        200)

    x1 = (noise(offset + i) * width + j1) * l
    y1 = (noise(offset + i * 2) * height + j1) * l
    x2 = (noise(offset + i * 3) * width + j2) * l
    y2 = (noise(offset + i * 4) * height + j2) * l
    x3 = (noise(offset + i * 5) * width + j3) * l
    y3 = (noise(offset + i * 6) * height + j3) * l
    x4 = (noise(offset + i * 7) * width + j4) * l
    y4 = (noise(offset + i * 8) * height + j4) * l

    // y1 = randomGaussian() * 900
    // x1 = randomGaussian() * 700
    // x2 = randomGaussian() * 700
    // y2 = randomGaussian() * 900
    // x3 = randomGaussian() * 700
    // y3 = randomGaussian() * 900
    // x4 = randomGaussian() * 700
    // y4 = randomGaussian() * 900

    bezier(
        x1, y1,
        x2, y2,
        x3, y3,
        x4, y4)

    offset += speed

}

function mousePressed() {
    if (pause == false) {
        noLoop()
        pause = true
    } else {
        loop()
        pause = false
    }
}

function call_bezier(l) {
    if (l < 0.1) {
        return
    }
    else {
        bezier_func(l)
        call_bezier(l / 2)
    }
}
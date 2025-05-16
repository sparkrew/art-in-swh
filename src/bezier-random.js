/* BezierCurves

References:
https://www.youtube.com/watch?v=uctX1P3H3xM
https://editor.p5js.org/PeterQwertz/sketches/Mh7aSsyMl
// https://github.com/rethread-studio/algorithmic-art-course/blob/main/examples/template-p5-to-svg.html


vec_of_bezier_lines = [...,...,...]
new_point = point
vec_of_bezier_lines[i % len(vec)] = new_point
*/

var w
var h
var rightmargin
var leftmargin
var topmargin
var bottommargin
var actualwidth
var actualheight

// playground
let x1, y1, x2, y2, x3, y3, x4, y4
let i = 100
let offset = 2
let speed
let j1 = -100
let j2 = -100
let j3 = 100
let j4 = 100

let steps

function setup() {

    w = windowWidth
    h = windowHeight
    rightmargin = 0.9 * w
    leftmargin = 0.1 * w
    topmargin = 0.1 * h
    bottommargin = 0.9 * h
    actualwidth = rightmargin - leftmargin
    actualheight = bottommargin - topmargin
    createCanvas(w, h)
    clear()
    noLoop()
    // frameRate(0.5)
}

function draw() {
    bezier_func()
    draw_text()
}

function bezier_func() {
    noFill()
    let random_weight = random([1, 1.5, 2])
    strokeWeight(random_weight)
    background(0)

    let choice = random([0, 1, 2])
    let r1 = random(0, 255)
    let r2 = random(0, 255)
    let g1 = random(0, 255)
    let g2 = random(0, 255)
    let b1 = random(0, 255)
    let b2 = random(0, 255)
    speed = random(0.003, 0.007)
    steps = random(50, 250)

    if (choice != 2) {
        for (let j = 0; j < steps; j++) {

            x1 = (noise(offset + i) * width + j1)
            y1 = (noise(offset + i + 2) * height + j1)
            x2 = (noise(offset + i + 3) * width + j2)
            y2 = (noise(offset + i + 4) * height + j2)
            x3 = (noise(offset + i + 5) * width + j3)
            y3 = (noise(offset + i + 6) * height + j3)
            x4 = (noise(offset + i + 7) * width + j4)
            y4 = (noise(offset + i + 8) * height + j4)

            if (choice == 0) {
                stroke(r1, b1, g1)
                bezier(x1, y1, x2, y2, x3, y3, x4, y4)
                line(leftmargin, x1, x1, y1)
                let max_right
                if (y4 > rightmargin) {
                    max_right = rightmargin
                } else {
                    max_right = y4
                }
                line(x4, y4, max_right, bottommargin)
            }
            else if (choice == 1) {
                stroke(r1, g1, b1)
                bezier(x1, y1, x2, y2, x3, y3, x4, y4)
                stroke(r2, g2, b2)
                line(x3, y3, rightmargin, y3)
                line(x2, bottommargin, x2, y2)
            }

            offset += speed
        }
    } else {
        for (let j = 0; j < steps; j++) {
            stroke(r1, g1, b1)
            x1 = (noise(offset + i) * width + j1)
            y1 = (noise(offset + i * 52) * height + j1)
            x2 = (noise(offset + i * 53) * width + j2) - 100
            y2 = (noise(offset + i * 54) * height + j2) - 100
            x3 = (noise(offset + i * 55) * width + j3) + 100
            y3 = (noise(offset + i * 56) * height + j3) + 100
            x4 = (noise(offset + i * 57) * width + j4)
            y4 = (noise(offset + i * 58) * height + j4)

            bezier(x1, y1, x2, y2, x3, y3, x4, y4)

            offset += speed
        }
        for (let j = 0; j < steps; j++) {
            stroke(r2, g2, b2)
            // stroke(0)
            x1 = (noise(offset + i) * width + j1) - 150
            y1 = (noise(offset + i * 2) * height + j1) + 150
            x2 = (noise(offset + i * 3) * width + j2)
            y2 = (noise(offset + i * 4) * height + j2)
            x3 = (noise(offset + i * 5) * width + j3)
            y3 = (noise(offset + i * 6) * height + j3)
            x4 = (noise(offset + i * 7) * width + j4) + 150
            y4 = (noise(offset + i * 8) * height + j4) + 150

            bezier(x1, y1, x2, y2, x3, y3, x4, y4)
            offset += speed
        }
    }
}

function draw_text() {
    stroke(random(0, 50))
    textSize(12)
    textFont("Courier New")
    text(`
    for (let j = 0; j < steps; j++) {

        stroke(r1, g1, b1)
        x1 = (noise(offset + i) * width + j1)
        y1 = (noise(offset + i + 2) * height + j1)
        x2 = (noise(offset + i + 3) * width + j2)
        y2 = (noise(offset + i + 4) * height + j2)
        x3 = (noise(offset + i + 5) * width + j3)
        y3 = (noise(offset + i + 6) * height + j3)
        x4 = (noise(offset + i + 7) * width + j4)
        y4 = (noise(offset + i + 8) * height + j4)

        bezier(x1, y1, x2, y2, x3, y3, x4, y4)

        offset += speed
    }
    `, random(100, windowWidth - 100), random(100, windowHeight - 150), 500)
}
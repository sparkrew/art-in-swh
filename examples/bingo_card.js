
let letter_4 = [
    45,  // tripled the width for 3 cards
    30   // doubled the height for 2 cards
]

let paper = letter_4

var echelle = 1
var w = paper[0] * 96 * echelle
var h = paper[1] * 96 * echelle
var single_card_width = w / 3  // width of one card
var single_card_height = h / 2 // height of one card
//I suggest to keep a bit of white space on the sides of page when plotting.
//so plot within the area leftmargin - rightmargin on the x-axis and topmargin - bottommargin on the y axis
var topmargin = 0.2 * h
var bottommargin = 0.8 * h
var leftmargin = 0.2 * w
var rightmargin = 0.8 * w

var actualwidth = rightmargin - leftmargin
var actualheight = bottommargin - topmargin

let divs = 5
let y_step = actualheight / divs
let x_step = actualwidth / divs
let y_mid = y_step / 2
let x_mid = x_step / 2

let max_elements = 100
let shift = 200
let element
let x_elem
let y_elem
let display_shift = 1

let line_shift = 40
let max_lines = 21

let random_lines = 10

let r
let g
let b

const randomItem = arr => arr.splice((Math.random() * arr.length) | 0, 1);
let saveCount = 0;
const totalSaves = 100;

let myFont;
function preload() {
  // Load a custom font before the sketch starts
  myFont = loadFont('Kode_Mono/KodeMono-VariableFont_wght.ttf');
//   myFont = loadFont('Lexend_Giga/LexendGiga-VariableFont_wght.ttf');
//   myFont = loadFont('Geostar_Fill/GeostarFill-Regular.ttf');
//   myFont = loadFont('Silkscreen/Silkscreen-Regular.ttf');
}

function setup() {
    createCanvas(w, h)
    noLoop()
    frameRate(1); // Slow down the frame rate to handle saves
}


function draw() {
    textSize(100);  // Reduced text size to fit the smaller cards
    textFont(myFont);
    background(255)
    
    // Draw 6 cards in a 3x2 grid
    for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 3; col++) {
            push() // Save the current transformation state
            translate(col * single_card_width, row * single_card_height)
            draw_card()
            pop() // Restore the transformation state
        }
    }
}



function draw_card(){
    // Scale down the margins for each individual card
    let cardTopMargin = topmargin / 2
    let cardBottomMargin = single_card_height - (topmargin / 2)
    let cardLeftMargin = leftmargin / 3
    let cardRightMargin = single_card_width - (leftmargin / 3)
    let cardActualWidth = cardRightMargin - cardLeftMargin
    let cardActualHeight = cardBottomMargin - cardTopMargin
    
    let y_coords = []
    let x_coords = []
    let numbers = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
        50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
        60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
        70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
        80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
        90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
    ]

    
    // fill(random(10, 150))
    r = random(20,255)
    g = random(20,255)
    b = random(20,255)
    stroke(r, g, b)
    for (let y = cardTopMargin; y <= cardBottomMargin; y = y + (cardActualHeight / divs)) {
        for (let x = cardLeftMargin; x <= cardRightMargin; x = x + (cardActualWidth / divs)) {
            x_elem = x
            y_elem = y
            // Check if this is the center position of the current card
            let isCenterPosition = (
                y >= cardTopMargin + (2 * cardActualHeight/divs) - 1 && 
                y <= cardTopMargin + (2 * cardActualHeight/divs) + 1 &&
                x >= cardLeftMargin + (2 * cardActualWidth/divs) - 1 && 
                x <= cardLeftMargin + (2 * cardActualWidth/divs) + 1
            );
            
            if (!isCenterPosition) {
                element = randomItem(numbers)
                if (x < cardRightMargin && y < cardBottomMargin) {
                    // Adjust text positioning for the scaled card size
                    let textOffsetX = cardActualWidth / divs / 4
                    let textOffsetY = cardActualHeight / divs / 4
                    fill(r, g, b)
                    console.log(element)
                    text(element, x_elem + textOffsetX - 10, y_elem + textOffsetY + 90)
                }
            }

            y_coords.push(y_elem + random(-shift,shift))
            x_coords.push(x_elem + random(-shift,shift))
        }
    }
    
    for (let i = 0; i <= x_coords.length; i = i + 1){
        strokeWeight(1)
        // horizontal lines
        if ((i + 1) % (divs + 1) != 0){
            // 
            line(
                x_coords[i], 
                y_coords[i], 
                x_coords[i + 1], 
                y_coords[i + 1]
            )
            for (let incr = 1; incr < 7; incr = incr + 5){
                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let q = 0; q < (max_lines); q++){
                        line(
                            x_coords[i] + random(-line_shift, line_shift), 
                            y_coords[i],
                            x_coords[i + incr],
                            y_coords[i + incr]
                        )
                    }
                }

                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let q = 0; q < (max_lines); q++){
                        line(
                            x_coords[i], 
                            y_coords[i] + random(-line_shift, line_shift),
                            x_coords[i + incr],
                            y_coords[i + incr]
                        )
                    }
                }
            
                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let q = 0; q < (max_lines); q++){
                        line(
                            x_coords[i], 
                            y_coords[i],
                            x_coords[i + incr] + random(-line_shift, line_shift),
                            y_coords[i + incr]
                        )
                    }
                }
                
                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let j = 0; j < (max_lines); j++){
                        line(
                            x_coords[i], 
                            y_coords[i],
                            x_coords[i + incr], 
                            y_coords[i + incr] + random(-line_shift, line_shift)
                        )
                    }
                }
            }
        } else {
            for (let incr = 6; incr < 7; incr = incr + 5){
                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let q = 0; q < (max_lines); q++){
                        line(
                            x_coords[i] + random(-line_shift, line_shift), 
                            y_coords[i],
                            x_coords[i + incr],
                            y_coords[i + incr]
                        )
                    }
                }

                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let q = 0; q < (max_lines); q++){
                        line(
                            x_coords[i], 
                            y_coords[i] + random(-line_shift, line_shift),
                            x_coords[i + incr],
                            y_coords[i + incr]
                        )
                    }
                }
            
                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let q = 0; q < (max_lines); q++){
                        line(
                            x_coords[i], 
                            y_coords[i],
                            x_coords[i + incr] + random(-line_shift, line_shift),
                            y_coords[i + incr]
                        )
                    }
                }
                
                if (Math.floor(random(0,random_lines)) == 0) {
                    for (let j = 0; j < (max_lines); j++){
                        line(
                            x_coords[i], 
                            y_coords[i],
                            x_coords[i + incr], 
                            y_coords[i + incr] + random(-line_shift, line_shift)
                        )
                    }
                }
            }
        }
        // vertical lines
        // line(x_coords[i], y_coords[i], x_coords[i + 6], y_coords[i + 6])
    }
        // Save the canvas
    if (saveCount < totalSaves) {
        saveCanvas('bingo_' + nf(saveCount, 3) + '.png');
        saveCount++;
    } else {
        noLoop(); // Stop when we've saved enough files
        console.log('Finished saving ' + totalSaves + ' images');
    }
}
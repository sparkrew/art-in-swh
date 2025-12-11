function setup() {
    createCanvas(700, 900)
    background(0)
}

function draw() {
    background(0)

    let ancx1 = 200
    let ancy1 = 200
    let ancx2 = 100
    let ancy2 = 500
    let ctrlx1 = mouseX
    let ctrly1 = mouseY
    let ctrlx2 = 500
    let ctrly2 = 500

    noFill()
    strokeWeight(5)
    stroke(255, 102, 0)

    // line(ancx1, ancy1, ctrlx1, ctrly1);
    // line(ctrlx2, ctrly2, ancx2, ancy2);

    strokeWeight(10)
    point(ancx1, ancy1)
    point(ancx2, ancy2)
    stroke(200, 0, 200)
    point(ctrlx1, ctrly1)
    point(ctrlx2, ctrly2)

    strokeWeight(5)
    stroke(200, 0, 0)
    bezier(
        ancx1, ancy1,
        ctrlx1, ctrly1,
        ctrlx2, ctrly2,
        ancx2, ancy2
    );

    
}


let colors;

function setup() {
  createCanvas(windowWidth, windowHeight);
  colors = [
    color(255, 0, 0),
    color(0, 255, 0),
    color(0, 0, 255)
  ];
}

function draw() {
  // This is the default blending mode.
  blendMode(BLEND);
  noFill();

  background(255);
  blendMode(EXCLUSION);



  for (let i = 0; i < 3; i++) {
    stroke(colors[i]);
    strokeWeight(20);

    //要注意beginshape和endshape的位置
    beginShape();
    for (let x = -20; x < width+20; x += 20) {
      let y = height / 2;
      //y=sin(x), x越大，周期越短，相同长度内频率更大
      //y=sin(x+a),a为正数时，曲线向左平移
      //i * TWO_PI / 3 控制每个正弦函数根据i的变化，在不同的位置
      //y=Asin(x) 振幅（纵坐标）变为原来的A倍
      y += 200 * sin(x * 0.03 + frameCount * 0.06 + i * TWO_PI / 3) * pow(abs(sin(x*0.0015+frameCount * 0.01)),5);
      curveVertex(x, y);

    }
    endShape();

  }

}
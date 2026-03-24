let audioContext, analyser, dataArray, sound;
let num = 80;
let noiseScale = 0.01;
let particles = [];
let currentColor;
let currentIteration = 0;
let isPlaying = false;

// Load and play an audio file
function preload() {
    soundFormats('wav');
    sound = loadSound("Cornfield_Chase.mp3", soundLoaded);
}

// Ensure user interaction before playing audio
function soundLoaded() {
    console.log("Audio loaded. Click to start.");
}

function setup() {
    createCanvas(1550, 900);
    colorMode(HSB);
    currentColor = color(0, 0, 100);
    background(0, 0, 0);

    for (let i = 0; i < num; i++) {
        particles.push(createVector(random(width), random(height)));
    }
}

function draw() {
    if (!isPlaying) return; // Wait until audio starts

    if (currentIteration % 15 === 0 && particles.length < 2000) {
        for (let i = 0; i < num; i++) {
            particles.push(createVector(random(width), random(height)));
        }
    }

    background(0, 0, 0, 0.01);

    if (analyser) {
        analyser.getByteFrequencyData(dataArray);

        let avgFrequency = getAverageFrequency(dataArray);
        let hueValue = map(avgFrequency, 0, 255, 0, 360);
        let noiseStrength = map(avgFrequency, 0, 255, 0.005, 0.3);
        noiseScale = noiseStrength;

        currentColor = color(hueValue, 100, 100);
    }

    for (let i = 0; i < particles.length; i++) {
        stroke(currentColor);
        let p = particles[i];
        point(p.x, p.y);
        let n = noise(p.x * noiseScale, p.y * noiseScale);
        let a = TAU * n;
        p.x += cos(a);
        p.y += sin(a);

        if (!onScreen(p)) {
            p.x = random(width);
            p.y = random(height);
        }
    }

    currentIteration++;
}

// Start music on user interaction
function mousePressed() {
    if (!isPlaying) {
        setupAudio();
        sound.loop();
        isPlaying = true;
        console.log("Audio started.");
    }
    noiseSeed(millis());
}

function onScreen(v) {
    return v.x >= 0 && v.x <= width && v.y >= 0 && v.y <= height;
}

function setupAudio() {
    audioContext = getAudioContext();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 512;

    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    sound.connect(analyser);
    analyser.connect(audioContext.destination);
}

function getAverageFrequency(array) {
    let sum = 0;
    for (let i = 0; i < array.length; i++) {
        sum += array[i];
    }
    return sum / array.length;
}

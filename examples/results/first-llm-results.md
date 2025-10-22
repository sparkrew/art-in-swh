# Source File

```js
var xoff = 0.0
var xinc = 42

function hal() {
    let resx, resy, stepx, stepy, x, y, x1, y1, coords, p1, p2, p3, p4
    resx = 2 * Math.floor(random(2, 5)); resy = 2 * Math.floor(random(2, 5)); coords = []
    stepx = Math.floor(actualwidth / resx); stepy = Math.floor(actualheight / resy)
    x = leftmargin
    for (let i = 0; i < resx; i++) {
        y = topmargin
        for (let j = 0; j < resy; j++) {
            x1 = x + stepx * noise(xoff); xoff += xinc; y1 = y + stepy * noise(xoff)
            coords.push({ x: x1, y: y1 })
            y += stepy}
        x += stepx}
    for (let i = 0; i < resx - 1; i++) {
        for (let j = 0; j < resy - 1; j++) {
            p1 = coords[i * resy + j]; p2 = coords[i * resy + j + resy]; p3 = coords[i * resy + j + resy + 1]; p4 = coords[i * resy + j + 1]
            trianglewlines(p1.x, p1.y, p2.x, p2.y, p4.x, p4.y);
            trianglewlines(p2.x, p2.y, p3.x, p3.y, p4.x, p4.y);
}}}

function trianglewlines(x1, y1, x2, y2, x3, y3) {
    // https://mathopenref.com/coordincenter.html
    len1 = dist(x2, y2, x3, y3); len2 = dist(x1, y1, x3, y3); len3 = dist(x1, y1, x2, y2)
    cx = (len1 * x1 + len2 * x2 + len3 * x3) / (len1 + len2 + len3); cy = (len1 * y1 + len2 * y2 + len3 * y3) / (len1 + len2 + len3)
    for (let i = 0; i < 1; i += 0.03) {
        triangle(lerp(cx, x1, i), lerp(cy, y1, i), lerp(cx, x2, i), lerp(cy, y2, i), lerp(cx, x3, i), lerp(cy, y3, i),
)}}
```

## True classification:

```json
{
    "entities": ["synthesized image","randomness"],
    "interaction": ["none"],
    "outcome": ["visual","static"]
}
```

# Using CodeLlama to get classification

## Material and Processes

- 1) Does it use external audio file? [True/False]
    - A: False
- 2) Does it use external image file? [True/False]
    - A: False
- 3) Does it generate sound? [True/False]
    - A: False
- 4) Does it generate images? [True/False]
    - A: True
- 5) Does it contain randomness? [True/False]
    - A: True
- 6) Does it contain interactions? [True/False]
    - A: False

## Environmental interaction

- 1) Does it depend on human interaction (through mouse, midi controller, microphone, keyboard, camera, motion sensor, or lidar) to run? [True/False]
    - A: False
- 2) Does it depend on computer interaction through data files to run? [True/False]
    - A: False
- 3) Does it depend on computer interaction through data stream to run? [True/False]
    - A: False
- 4) Does it depend on computer interaction through remote data to run? [True/False]
    - A: False
- 5) Does it depend on computer interaction through web API to run? [True/False]
    - A: False

## Sensory outcomes

- 1) Does it produce visual sensory outcomes? [True/False]
    - A: True
- 2) Does it produce auditory sensory outcomes? [True/False]
    - A: False
- 3) Does it produce physical sensory outcomes? [True/False]
    - A: False
- 4) Does it produce static or time-based (one of these values is mandatory for this characteristic) sensory outcomes? [True/False]
    - A: True

if we compile the answers into a json:

```json
{
    "entities": ["synthesized image","randomness"],
    "interaction": ["none"],
    "outcome": ["visual","static"]
}
```

we get the same true classification :)  It means that the model could understand the code and the questions to provide us the correct answer.


# Some observations so far: 

- Sending all questions at once makes the output unstable (probably too much information to extract). The model behaves differently in multiple repetitions. Tends to be more accurate then wrong.
- Sending one question at a time makes the output stable (always the same answer), but sometimes incorrect. From a very short experiment, it seems that it was more prone to false positives.
- Sending the group of questions by category is the perfect balance for stability and accuracy.
- Open questions are more prone to false positives too.
  - Instead of giving examples (eg *computer interaction (for example through data file, data stream, remote data, web API, etc.)*), we should ask one interaction type at a time for better accuracy.
  - Perhaps we should do it for the human interaction too. I wonder if we will have accuracy problems if we keep the question as-is.

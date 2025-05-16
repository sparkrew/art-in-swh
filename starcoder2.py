
"""
StarCoder2 

This model was trained with SWH code.

Used NVIDIA L4 Tensor Core GPU with 24 GB of VRAM to run this, and was taking around 1 minute to 
print answer. Crazy amount of time for our project. I also have to check how to better write 
prompts for this model. It was fine-tuned for instructions, but I had some weird results.
"""

import transformers
import torch
import time

pipeline = transformers.pipeline(
    model="bigcode/starcoder2-15b-instruct-v0.1",
    task="text-generation",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

def respond(instruction: str, response_prefix: str) -> str:
    messages = [{"role": "user", "content": instruction}]
    prompt = pipeline.tokenizer.apply_chat_template(messages, tokenize=False)
    prompt += response_prefix

    teminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("###"),
    ]

    result = pipeline(
        prompt,
        max_length=256,
        num_return_sequences=1,
        do_sample=False,
        eos_token_id=teminators,
        pad_token_id=pipeline.tokenizer.eos_token_id,
        truncation=True,
        max_new_tokens=256,
    )
    response = response_prefix + result[0]["generated_text"][len(prompt) :].split("###")[0].rstrip()
    return response


instruction = """
Given this code:
```
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.js"></script>
    <script src="abstract3.js"></script>
</head>
<body>
    <main>
    let wd;
    let ht;
    function setup() {
        wd = 580;
        ht = 750;
        createCanvas(wd, ht);
    }

    function draw() {
        // Dark background
        background(0);

        // Configuring the line
        strokeWeight(1);
        stroke(255, 204, 0);

        for (let posX = 0; posX < 100; posX++) {
            // x1 y1 x2 y2
            line(1, 1 + posX * 10, 1 + posX * 10, ht);
            line(1 + posX * 10, 1, ht, 1 + posX * 10,
            );
        }
    }
    </main>
</body>
</html>
```
What are the dependencies from this code?
"""
response_prefix = ""

start = time.time()
answer = respond(instruction, response_prefix)
end = time.time()

print(answer)

## OUTPUT 1
# The code is plotting a diagonal pattern using the `line()` function in the `draw()` function. The `setup()` function is used to set the dimensions of the canvas

## OUTPUT 2
# Here are the dependencies from the code:
# - `p5.js`: This is a JavaScript library for creative coding, providing a set of simple and powerful tools for creating interactive web-based art, design, and animation.
# - `abstract3.js`: This is a custom JavaScript file that contains the code for the `setup()` and `draw()` functions.

## OUTPUT 3
# To identify the dependencies, you can look for the `script` tags in the `head` section of the HTML code. The `src` attribute of each `script` tag indicates the source of the dependency, which is either a remote URL (in the case of `p5.js`) or a local file (in the case of `abstract3.js`).

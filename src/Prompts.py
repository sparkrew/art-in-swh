from dataclasses import dataclass
from typing import Optional

@dataclass
class PromptTemplate:
    name: str
    template: str
    version: Optional[str] = None
    description: Optional[str] = None

# Then define your prompts
PROMPT_1 = PromptTemplate(
    name="basic_classification",
    template="""You are given the source code of a generative artwork (sound, visual, or textual).  
    Using the framework below, tag the artwork along 3 dimensions.

    1) Entities  
    Select all that apply:
    - processed audio        // uses existing audio (e.g., mp3, wav, midi)
    - processed image        // uses existing visual media (e.g., images, video)
    - processed text         // uses existing text/code files
    - synthesized sound      // generates new sounds or notes
    - synthesized image      // generates new visual elements
    - synthesized text       // generates new textual or typographic elements
    - randomness             // uses randomness in synthesis or processing
    - interactions           // defines interactions between audio/visual/text elements
    - other                  // material/process present but not covered above

    2) Environmental interaction  
    How the artwork interacts with its environment. Select all that apply:
    - human_interaction      // input devices: mouse, keyboard, midi, mic, camera, motion sensor, lidar, etc.
    - computer_interaction   // data file, data stream, remote data, web API, etc.
    - none                   // no environmental interaction

    3) Sensory outcomes  
    What the audience perceives, and whether it is static or temporal:
    - modalities: any of [visual, auditory, physical]
    - time: exactly one of [static, time-based] (this is mandatory)

    OUTPUT FORMAT (very important!!):
    Return ONLY a valid JSON object, no extra text, in this exact schema:

    {
    "entities": [
        "processed audio" | "processed image" | "processed text" |
        "synthesized sound" | "synthesized image" | "synthesized text" |
        "randomness" | "interactions" | "other"
    ],
    "interaction": [
        "human interaction" | "computer interaction" | "none"
    ],
    "outcome": [
        "visual" | "auditory" | "physical",
        "static" | "time-based"
    ]
    }

    Follow these rules:
    - Use only the tag strings listed above.
    - The response must be valid JSON and nothing else.

    Now analyze the following source code:
    """,
    version="1.0"
)


PROMPT_2 = PromptTemplate(
    name="detailed_analysis",
    template="""You analyze source code of a generative artwork and output tags in JSON.

    Dimensions and allowed tags:

    entities (0+ tags):
    - "processed audio"      // uses preexisting audio files
    - "processed image"      // uses preexisting images or video
    - "processed text"       // uses preexisting text or code
    - "synthesized sound"    // generates new sounds or notes
    - "synthesized image"    // generates new visual elements
    - "synthesized text"     // generates new textual/typographic elements
    - "randomness"           // uses randomness in processing or synthesis
    - "interactions"         // defines interactions between audio/visual/text elements
    - "other"

    interaction (exactly 1 if any interaction, otherwise "none"):
    - "human interaction"    // e.g., mouse, keyboard, MIDI, mic, camera, motion sensor, lidar
    - "computer interaction" // e.g., data files, streams, remote data, web APIs
    - "none"

    outcome (≥1 modality + exactly 1 time tag):
    - modalities: "visual", "auditory", "physical"
    - time: "static" or "time-based"

    Rules:
    - Use only the tags listed above.
    - If there is no interaction, use ["none"] for interaction.
    - In "outcome", always include exactly one of "static" or "time-based".

    Output format (JSON only, no explanation, no extra text):

    {
    "entities": [...],
    "interaction": [...],
    "outcome": [...]
    }

    Now analyze this source code:
    """,
    description="Detailed classification with interaction detection",
    version="2.0"
)


In their [A framework for understanding generative art](https://www.tandfonline.com/doi/pdf/10.1080/14626268.2012.709940), Dorin and colleagues distinguish 4 main dimensions to characterize a piece of generative art: entities; processes; environmental interaction; and sensory outcomes. We use these four dimensions to analyze generative artworks, and refine them with concrete options for each dimnesion. We aim at using an ML based approach to precisely charactarize existing programs for generative art, based on this framework.

- Material and Processes
  - audio_file // the code uses preexisting audio material, such as a mp3 or midi audio sample, as part of the artwork  
  - image_file // the code uses preexisting visual material, such as an image or video files, as part of the artwork
  - text_file // the code uses preexisting textual material, such as text or code files, as part of the artwork
  - synthesized_sound // the code synthesizes, generates new sounds or notes, as part of the artwork
  - synthesized_image // the code synthesizes, generates new visual elements, as part of the artwork
  - synthesized_text  // the code synthesizes, generates new textual or typographical elements, as part of the artwork
  - randomness // the code uses randomness in the syntehsis or processing of audio or visual or textual elements, as part of the artwork
  - interactions // the code defines interactions between audio or visual or textual elements, as part of the artwork
  - other 
- Environmental interaction
  - human_interaction (for example through mouse, midi controller, microphone, keyboard, camera, motion sensor, lidar, etc.)
  - computer_interaction (for example through data file, data stream, remote data, web API, etc.)
  - none
- Sensory outcomes
  - visual 
  - auditory
  - physical
  - static or time-based [one of these values is mandatory for this characteristic]

We also ask the LLM: Is this piece reusing existing algorithm ?
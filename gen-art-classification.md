In their [A framework for understanding generative art](https://www.tandfonline.com/doi/pdf/10.1080/14626268.2012.709940), Dorin and colleagues distinguish 4 main dimensions to characterize a piece of generative art: entities; processes; environmental interaction; and sensory outcomes. In our work, we adapt this framework to automatically analyze the different types of code for generative art that we have found in Software Heritage. The adaptation consists in renaming entities into 'material', which is a term commonly used in the arts that has a more continuous nature than entities, which is better suited to analyze generative sound artworks. Also, we merge material and processes as both can be difficult to distinguish in the code of a generative artwork. We refine the three dimensions of generative artworks with concrete options for each dimension.

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
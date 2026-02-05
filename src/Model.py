import json
# import logging
from openai import OpenAI

# logger = logging.getLogger(__name__)


class LLM_Model():
    
    def __init__(self, model_name, base_url="http://localhost:8000/v1", system_prompt=""):
        self.model_name = model_name
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=""  # no api key because we're running our own model :)
        )
        # logger.info(f"Initialized LLM_Model: {model_name} at {base_url}")

    def _validate_response(self, text):
        """
        returns boolean value if string contains a valid json file.
        """
        try:
            json.loads(text)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    def _extract_json_string(self, text):
        """
        extracts only the json string from the text.
        """
        # Try to find JSON in markdown code blocks
        if "```" in text:
            # Handle ```json or ``` with optional language tag
            start_markers = ["```json", "```JSON", "```"]
            for marker in start_markers:
                if marker in text:
                    start = text.find(marker) + len(marker)
                    # Skip to next line if there's content after marker
                    if text[start:start+1] in ['\n', '\r']:
                        start += 1
                    end = text.find("```", start)
                    if end != -1:
                        return text[start:end].strip()
        
        # Try to find JSON object or array with proper nesting
        for start_char, end_char in [('{', '}'), ('[', ']')]:
            start = text.find(start_char)
            if start != -1:
                # Count nested braces/brackets to find matching closing
                count = 0
                for i in range(start, len(text)):
                    if text[i] == start_char:
                        count += 1
                    elif text[i] == end_char:
                        count -= 1
                        if count == 0:
                            return text[start:i+1]
        
        return text.strip()

    def get_labels(self, prompt_template, art_src_code, system_prompt, max_tokens=124, temperature=0.1, max_retries=3):
        """
        prompt the model.
        if the model response doesn't contain a valid json, prompt again.
        """
        user_prompt = f"{prompt_template}\n ```\n{art_src_code}\n```"
        # logger.debug(f"Prompting model with code length: {len(art_src_code)} chars")

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                ).choices[0].message.content
                
                # logger.debug(f"Attempt {attempt + 1}: Received response length: {len(response)} chars")
                
                # Extract JSON from response
                extracted_json = self._extract_json_string(response)
                
                # Validate the extracted JSON
                if self._validate_response(extracted_json):
                    # Parse and return valid JSON
                    predicted_labels = json.loads(extracted_json)
                    # logger.info(f"Successfully extracted labels on attempt {attempt + 1}")
                    return predicted_labels
                else:
                    # logger.warning(f"Attempt {attempt + 1}/{max_retries}: Invalid JSON received, retrying...")
                    # logger.debug(f"Invalid response: {response[:200]}...")
                    pass
            except Exception as e:
                # logger.error(f"Attempt {attempt + 1}/{max_retries}: Error during API call: {e}")
                if attempt == max_retries - 1:
                    raise
        
        # If all retries failed, raise an error
        error_msg = f"Failed to get valid JSON response after {max_retries} attempts. Last response: {response}"
        # logger.error(error_msg)
        raise ValueError(error_msg)
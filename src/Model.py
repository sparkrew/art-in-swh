import json
from openai import OpenAI

class LLM_Model():
    
    def __init__(self, model_name, base_url="http://localhost:8000/v1", system_prompt=""):
        self.model_name = model_name
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=""  # no api key because we're running our own model :)
        )

    def _validate_response(self):
        """
        we have to make sure that the model response contains a json.
        we may need to apply something like a regex to extract json from response string.
        """
        pass

    def get_labels(self, prompt_template, art_src_code, system_prompt, max_tokens=124, temperature=0.1):
        """
        prompt the model.
        if the model response doesn't contain a valid json, prompt again.
        """
        user_prompt = f"{prompt_template}\n ```\n{art_src_code}\n```"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        ).choices[0].message.content
        
        # Parse JSON response
        predicted_labels = json.loads(response)
        
        return predicted_labels
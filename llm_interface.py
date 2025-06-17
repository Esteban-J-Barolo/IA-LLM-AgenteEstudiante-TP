# Clase para conectarse al LLM
# from openai import OpenAI
import requests

class Llm:
    def __init__(self):
        self.modelo = 'nvidia/llama-3.3-nemotron-super-49b-v1:free'
        self.temperature = 0.7
        self.API_KEY = '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'
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        # self.client = OpenAI(
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key=self.API_KEY,
        #     )

    def enviar_mensaje(self, prompt):
            # response = self.client.chat.completions.create(
            #     model=self.modelo,
            #     messages=[{"role": "user", "content": prompt}],
            #     temperature=self.temperature
            # )
            # return response.choices[0].message.content
        
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.modelo,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[ERROR] Código {response.status_code}: {response.text}"
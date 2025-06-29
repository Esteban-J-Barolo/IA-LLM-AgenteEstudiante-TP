# Clase para conectarse al LLM
# from openai import OpenAI
import requests

class Llm:
    def __init__(self):
        self.modelo = 'nvidia/llama-3.3-nemotron-super-49b-v1:free'
        self.temperature = 0.7
<<<<<<< HEAD
        self.API_KEY = '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' # https://openrouter.ai/settings/keys
=======
        self.API_KEY = '' # https://openrouter.ai/settings/keys
>>>>>>> 95974e349d44416d651f5d739f0699563c6aed86
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
                {"role": "system", "content": "Eres un profesor universitario experto que explica de forma clara y resumida el contenido de textos académicos. Tu tarea es leer un texto en español y generar un resumen claro, conciso y en español para estudiantes."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[ERROR] Código {response.status_code}: {response.text}"

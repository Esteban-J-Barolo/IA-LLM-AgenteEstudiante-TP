# Clase para conectarse al LLM
# from openai import OpenAI
import requests
from huggingface_hub import InferenceClient

class Llm:
    def __init__(self):
        self.modelo = 'nvidia/llama-3.3-nemotron-super-49b-v1:free'
        self.temperature = 0.7
        self.API_KEY = '' # https://openrouter.ai/settings/keys
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def enviar_mensaje(self, prompt):
        
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

        print(response)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[ERROR] Código {response.status_code}: {response.text}"

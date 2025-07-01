# Clase para conectarse al LLM
import requests
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables
api_key = os.getenv('API_KEY')

class Llm:
    def __init__(self):
        self.modelo = 'nvidia/llama-3.3-nemotron-super-49b-v1:free'
        self.temperature = 0.5
        self.API_KEY = api_key # https://openrouter.ai/settings/keys
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

        if response.status_code == 200:

            data = response.json()

            if 'choices' in data:
                content = data['choices'][0]['message']['content']
            elif 'content' in data:
                content = data['content'][0]['text']
            elif 'text' in data:
                content = data['text']
            else:
                print(f"Estructura inesperada: {data}")
                content = str(data)
            return content
            # return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Error HTTP: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return f"Error HTTP: {response.status_code}"


import requests

modelo = 'nvidia/llama-3.3-nemotron-super-49b-v1:free'
temperature = 0.7
API_KEY = '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' # https://openrouter.ai/settings/keys
url = "https://openrouter.ai/api/v1/chat/completions"


def enviar_mensaje(prompt):

        # headers = {
        #     "Authorization": f"Bearer {API_KEY}",
        #     "Content-Type": "application/json"
        # }
        
        # data = {
        #     "model": model,
        #     "messages": [
        #         {"role": "user", "content": prompt}
        #     ],
        #     "temperature": temperature,
        #     "max_tokens": 1000
        # }
        
        # try:
        #     response = requests.post(url, headers=headers, json=data)
            
        #     if response.status_code == 200:
        #         return response.json()['choices'][0]['message']['content']
        #     else:
        #         return f"Error {response.status_code}: {response.text}"
                
        # except Exception as e:
        #     return f"Error de conexión: {str(e)}"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": "Eres un profesor universitario experto que explica de forma clara y resumida el contenido de textos académicos. Tu tarea es leer un texto en español y generar un resumen claro, conciso y en español para estudiantes."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }

        response = requests.post(url, headers=headers, json=data)

        print(response)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[ERROR] Código {response.status_code}: {response.text}"

resp = enviar_mensaje("Que es la física?")

print(resp)
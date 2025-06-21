import json
from pathlib import Path

def guardar_chat(chat: list, vault_path: str, materia: str):
    if materia:
        path = Path(vault_path) / "Materias" / materia / "chat.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chat, f, indent=2, ensure_ascii=False)
    else:
        path = Path(vault_path) / "Materias" / "chat.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chat, f, indent=2, ensure_ascii=False)

def cargar_chat(vault_path: str, materia: str) -> list:
    if materia:
        path = Path(vault_path) / "Materias" / materia / "chat.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    else:
        path = Path(vault_path) / "Materias" / "chat.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    return []

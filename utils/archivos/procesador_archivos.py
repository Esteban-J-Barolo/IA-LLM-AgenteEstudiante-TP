# Lee archivos markdown o texto plano
from pathlib import Path

def guardar_en_vault(uploaded_file, vault_path: str, materia: str):
    
    ruta_destino = Path(vault_path) / "Materias" / materia / "Archivos" / uploaded_file.name
    
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_destino, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return ruta_destino


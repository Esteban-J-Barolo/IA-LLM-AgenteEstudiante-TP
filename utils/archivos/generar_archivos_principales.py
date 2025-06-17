from pathlib import Path
from typing import List
from config.configuraciones import cargar_config

def inicializar_archivos():

    conf = cargar_config()

    ruta_vault = conf["vault_path"]
    
    base = Path(ruta_vault).expanduser().resolve()

    archivos = ["materias", "perfil", "progreso", "sistema"]
    carpetas = ["Materias", "Perfil", "Progreso", "Sistema"]

    index_path_index = base / "index.md"
    if not index_path_index.exists():
        with open(index_path_index, "w", encoding="utf-8") as f:
            f.write(estruc_index())
    
    for carpeta, materia in zip(carpetas, archivos):
        index_path_index = base / f"{carpeta}" / f"{materia}.md"
        if not index_path_index.exists():
            with open(index_path_index, "w", encoding="utf-8") as f:
                f.write(estruc(materia, archivos))

def estruc_index() -> str:
    return """
# 📘 Bienvenido a tu Vault académico\n\nDesde aquí podés navegar todas tus materias y secciones.\n\n
## [[Materias]] \n
## [[Perfil]] \n
## [[Progreso]] \n
## [[Sistema]] \n
"""
def estruc(materia: str, archivos: List[str]) -> str:
    estructuras = {
        archivos[0]: estruc_materias,
        archivos[1]: estruc_perfil,
        archivos[2]: estruc_progreso,
        archivos[3]: estruc_sistema
    }

    if materia in estructuras:
        return estructuras[materia]()
    else:
        return ""
    
def estruc_materias() -> str:
    return "# **Materias**\n\n[[index|Volver]]"

def estruc_perfil() -> str:
    return "[[index|Volver]]"

def estruc_progreso() -> str:
    return "[[index|Volver]]"

def estruc_sistema() -> str:
    return "[[index|Volver]]"
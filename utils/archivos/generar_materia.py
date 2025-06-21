from pathlib import Path

def crear_archivos_materia(ruta_vault: str, nombre_materia: str):

    base = Path(ruta_vault).expanduser().resolve()
    carpeta_materias = base / "Materias"
    carpeta_materia = carpeta_materias / nombre_materia

    carpetas = ["Teoria", "Practica", "TPs", "Examenes", "Notas", "Archivos"]

    # Crear carpeta principal de la materia
    carpeta_materia.mkdir(parents=True, exist_ok=True)

    editar_materias(carpeta_materias / "materias.md", nombre_materia)

    index_path_index = carpeta_materia / f"index_{nombre_materia}.md"
    if not index_path_index.exists():
        with open(index_path_index, "w", encoding="utf-8") as f:
            f.write(estruc_index(nombre_materia))

    for carpeta in carpetas:
        (carpeta_materia / carpeta).mkdir(parents=True, exist_ok=True)

def estruc_index(nombre_materia: str) -> str:
    md_materia = f"""# 📘 {nombre_materia}\n
---## Agente\n\n### Teoría\n\n### Práctica\n\n### TPs\n\n### Exámenes\n
---
## Estudiante\n\n### Notas\n
- 
\n### Resúmenes\n
- \n
```button
name ✍️ Crear nuevas nota del estudiante
type command
action Templater: Open insert template modal 
```
\n## *[[Materias|⬅️ Volver a materias]]*\n
"""
    return md_materia

def editar_materias(index_path: Path, nombre_materia: str):

    index_path.touch(exist_ok=True)

    linea_materia = f"- [[index_{nombre_materia}|{nombre_materia}]]\n"

    with open(index_path, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Evitar duplicados
    if linea_materia in lineas:
        return

    # Insertar después de título "# Materias"
    for i, linea in enumerate(lineas):
        if "# **Materias**" in linea:
            lineas.insert(i + 1, linea_materia)
            break
    else:
        # Si no hay título, agregar al final
        lineas.append("# Materias\n")
        lineas.append(linea_materia)

    with open(index_path, "w", encoding="utf-8") as f:
        f.writelines(lineas)
from pathlib import Path
from utils.archivos.generar_archivos_principales import inicializar_archivos

def crear_vault(path_str: str):

    base = Path(path_str).expanduser().resolve()

    # Carpetas que se van a crear
    carpetas = ["Materias", "Perfil", "Progreso", "Sistema", "Plantillas"]

    for carpeta in carpetas:
        (base / carpeta).mkdir(parents=True, exist_ok=True)

    # Crear los archivos principales
    inicializar_archivos(path_str)

    crear_las_plantillas(path_str)


def crear_plantilla(vault_path: str, nombre_archivo: str, contenido: str, carpeta_plantillas: str = "Plantillas", terminacion_archivo: str = "md"):
    plantilla_path = Path(vault_path) / carpeta_plantillas
    plantilla_path.mkdir(parents=True, exist_ok=True)

    archivo = plantilla_path / f"{nombre_archivo}.{terminacion_archivo}"
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)


def crear_las_plantillas(vault_path: str):
    contenido_notas = """---
tags: [nota, estudiante, <% tp.system.prompt("¿Materia?") %>]
tipo: libre
fecha: <% tp.date.now("YYYY-MM-DD") %>
tema: <% tp.system.prompt("¿Qué tema estás por ver?") %>
---

# ✍️ Notas del estudiante – <% tp.file.title %>

## 🗣️ Clase / fuente


---

## ✏️ Notas tomadas


---

## 🧠 Lo que entendí


---

## ❗ Lo que no entendí


---

## 🗂️ Posibles temas para repasar / desarrollar más

- 
"""
    crear_plantilla(vault_path, "nota_estudiante", contenido_notas)
    contenido_resumen = """---
tags: [nota, estudiante, <% tp.file.title %>]
tipo: libre
fecha: <% tp.date.now("YYYY-MM-DD") %>
tema: <% tp.system.prompt("¿Qué tema estás resumiendo?") %>
---

# 📝 Resumen del estudiante – <% tp.file.title %>

## 🧠 ¿Qué entendí del tema?


---

## 🔍 Conceptos clave


---

## ✏️ Ejemplos (propios o de clase)


---

## ❗ Dudas o puntos confusos


---

## 📎 Fuente

- 
"""
    crear_plantilla(vault_path, "resumen_estudiante", contenido_resumen)

    contenido_crear_resumen = "<% tp.user.script_crear_notas(tp, \"Resumen\") %>"
    crear_plantilla(vault_path, "crear_resumen_estudiante", contenido_crear_resumen, "Plantillas/Crear")

    contenido_crear_nota = "<% tp.user.script_crear_notas(tp, \"Nota\") %> "
    crear_plantilla(vault_path, "crear_nota_estudiante", contenido_crear_nota, "Plantillas/Crear")

    contenido_script_crear = """async function my_function (tp, tipo) {
    const currentFile = tp.file.path(true); // ruta completa con carpeta y nombre del archivo actual
    const currentFolder = currentFile.split('/').slice(0, -1).join('/'); // carpeta donde está la nota actual

    const nombreMateria = currentFolder.split('/').pop(); // saca solo el último nombre

    const newFileName = tipo + "_" + nombreMateria + "_" + tp.date.now("DD-MM-YYYY");
    const newFilePath = currentFolder + "/Notas/" + newFileName;

    const tipo_lower = tipo.toLowerCase()

    const plantilla = tp.file.find_tfile(tipo_lower + "_estudiante");
    const contenidoPlantilla = await tp.file.include(plantilla);

    const textoExtra = `\n# *[[index_${nombreMateria}|Volver]]*`;
    const contenidoNuevo = contenidoPlantilla + textoExtra;

    // Creá la nota nueva usando plantilla base vacía o con contenido
    await tp.file.create_new(contenidoNuevo, newFilePath);

    // Insertar en la nota actual un enlace a la nota creada, justo arriba del cursor
    const linkText = `[[${newFileName}]]\n- `;
    // Abrir el archivo actual y agregar el enlace arriba del cursor (o arriba del botón)
    await tp.file.cursor_append(linkText); // inserta al inicio del archivo actual

    return ""; // evitar que esciba undefined
}
module.exports = my_function;
"""
    crear_plantilla(vault_path, "script_crear_notas", contenido_script_crear, "Scripts", "js")
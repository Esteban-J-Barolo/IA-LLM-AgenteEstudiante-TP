import os
import re
from datetime import datetime
from typing import List, Dict

def generar_nota_resumen(path_vault:str, tema: str, informacion: str, conceptos: List[Dict[str, str]], materia: str):
    """
    Genera una nota de resumen en formato markdown con la estructura especificada
    y crea archivos individuales para cada concepto.
    
    Args:
        tema (str): Título del tema principal
        informacion (str): Contenido de la información a resumir
        conceptos (List[Dict[str, str]]): Lista de diccionarios con conceptos y sus desarrollos
        materia (str): Nombre de la materia (por defecto "General")
    
    Returns:
        tuple: (contenido_nota_principal, rutas_archivos_creados)
    """
    # Obtener fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Limpiar nombre de materia para usar como tag y carpeta
    materia_tag = materia.lower().replace(" ", "_")

    directorio_base = path_vault+f"/Materias/{materia}/Teoria"

    # Extraer conceptos principales para la sección
    puntos_clave = []
    for concepto in conceptos:
        nombre_concepto = concepto["concepto"]
        # Limpiar nombre del concepto de corchetes si los tiene
        nombre_limpio = re.sub(r'\[\[|\]\]', '', nombre_concepto)
        puntos_clave.append(f"- **{nombre_limpio}**")

    # Generar contenido de la nota principal
    nota_principal = f"""---
tags: [teoria, {materia_tag}]
tema: "{tema}"
fecha: {fecha_actual}
---

# 🧠 {tema}

## Conceptos principales
{chr(10).join(puntos_clave)}

## Desarrollo

{informacion}

## Referencias
- [[{tema}_referencias]]

## Ejemplos
- [[{tema}_ejemplos]]
"""
    # Crear archivo de la nota principal
    nombre_archivo_principal = f"{tema}.md"
    ruta_principal = os.path.join(directorio_base, nombre_archivo_principal)

    with open(ruta_principal, 'w', encoding='utf-8') as f:
        f.write(nota_principal)

    # Crear archivos para cada concepto
    rutas_conceptos = []
    for concepto in conceptos:
        nombre_concepto = concepto["concepto"]
        desarrollo = concepto["desarrollo"]
        
        nombre_archivo = concepto["concepto"]
        nombre_archivo = re.sub(r'\[\[|\]\]', '', nombre_archivo)
        nombre_archivo += ".md"
        
        # Limpiar nombre para el título
        titulo_concepto = re.sub(r'\[\[|\]\]', '', nombre_concepto)

        # Contenido del concepto
        contenido_concepto = f"""---
tags: [concepto, {materia_tag}]
tema: "{titulo_concepto}"
fecha: {fecha_actual}
---

# 📝 {titulo_concepto}

## Definición

{desarrollo}

## Relación con otros conceptos
- [[{tema}]]

## Referencias
- [[{titulo_concepto}_referencias]]

## Ejemplos
- [[{titulo_concepto}_ejemplos]]
"""
        # Crear archivo del concepto
        ruta_concepto = os.path.join(directorio_base, nombre_archivo)
        with open(ruta_concepto, 'w', encoding='utf-8') as f:
            f.write(contenido_concepto)
        
        rutas_conceptos.append(ruta_concepto)
        
    rutas_creadas = [ruta_principal] + rutas_conceptos

    print(f"✅ Nota principal creada: {ruta_principal}")
    print(f"✅ {len(rutas_conceptos)} archivos de conceptos creados")
    for ruta in rutas_conceptos:
        print(f"   - {os.path.basename(ruta)}")
    
    # return nota_principal, rutas_creadas
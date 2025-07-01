import os
import re
from datetime import datetime
from typing import Dict

def generar_nota_resumen(path_vault:str, informacion: Dict, materia: str):
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
    for concepto in informacion.get('conceptos'):
        nombre_concepto = concepto["concepto"]
        # Limpiar nombre del concepto de corchetes si los tiene
        nombre_limpio = re.sub(r'\[\[|\]\]', '', nombre_concepto)
        puntos_clave.append(f"- [[{nombre_limpio}]]")

    # Generar contenido de la nota principal
    nota_principal = f"""---
tags: [teoria, {materia_tag}]
tema: "{informacion.get('tema')}"
fecha: {fecha_actual}
---

# 🧠 {informacion.get('tema')}

## Conceptos principales
{chr(10).join(puntos_clave)}

## Desarrollo

{informacion.get('resumen')}

## Referencias
{format_referencias(informacion.get('referencias', []))}

## Ejemplos
- {informacion.get('ejemplos')}
"""
    # Crear archivo de la nota principal
    nombre_archivo_principal = f"{informacion.get('tema')}.md"
    ruta_principal = os.path.join(directorio_base, nombre_archivo_principal)

    agregar_enlace_simple(path_vault+f"/Materias/{materia}/index_{materia}.md", nombre_archivo_principal)

    with open(ruta_principal, 'w', encoding='utf-8') as f:
        f.write(nota_principal)

    # Crear archivos para cada concepto
    rutas_conceptos = []
    for concepto in informacion.get('conceptos'):
        nombre_concepto = concepto["concepto"]
        desarrollo = concepto["desarrollo"]
        
        nombre_archivo = concepto["concepto"]
        # Eliminar [[ y ]]
        nombre_archivo = re.sub(r'\[\[|\]\]', '', nombre_archivo)
        # Eliminar caracteres no válidos en Windows: < > : " | ? * /
        nombre_archivo = re.sub(r'[<>:"|?*\\/]', '', nombre_archivo)
         # Reemplazar espacios múltiples por uno solo
        nombre_archivo = re.sub(r'\s+', ' ', nombre_archivo)
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
- [[{informacion.get('tema')}]]
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

def format_referencias(referencias_list):
    if not referencias_list:
        return "- No hay referencias disponibles"
    
    referencias_formatted = []
    for ref in referencias_list:
        ref_name = ref.get('referencia', 'Sin referencia')
        referencias_formatted.append(f"- [[{ref_name}]]")
    
    return "\n".join(referencias_formatted)

def agregar_enlace_simple(archivo_path, nombre_archivo):
    with open(archivo_path, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    for i, linea in enumerate(lineas):
        if linea.strip() == '### Teoría':
            # Verificar si el enlace ya existe en las próximas líneas
            enlace = f'- [[{nombre_archivo}]]\n'
            
            # Buscar en las siguientes 5 líneas si ya existe
            ya_existe = False
            for j in range(i+1, min(i+6, len(lineas))):
                if enlace.strip() in lineas[j]:
                    ya_existe = True
                    break
            
            if not ya_existe:
                # Insertar después de "### Teoría"
                lineas.insert(i+1, enlace)
                break
    
    with open(archivo_path, 'w', encoding='utf-8') as f:
        f.writelines(lineas)
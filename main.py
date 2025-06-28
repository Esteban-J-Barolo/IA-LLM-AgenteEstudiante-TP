# Punto de entrada de la app (controlador general)
import json
import re
from typing import Dict, Optional
from percepcion.clasificador_intencion import clasificar
from razonamiento.generar_salidas import respuesta
from utils.rag.iniciar_rag import iniciar_rag
from utils.archivos.generar_nota_resumen import generar_nota_resumen
from generacion_contenido.generar_salidas_deseadas import generar_salida_deseada

class AgenteEstudio():
    def __init__(self):
        self.rag = iniciar_rag()

    def procesar_interaccion(self, mensaje_usuario: str, materia: str, path_vault: str) -> Dict:

        intencion = clasificar(mensaje_usuario)
        print(intencion, end="\n")

        # buscamos informacion relevante en el RAG
        informacion = self.rag.search_and_format(intencion.get("tema"))

        # obtenemos el resumen a trvez de la LLM
        resumen_raw = respuesta(intencion, informacion)
        print(resumen_raw, end="\n")
        
        # Validación segura
        if isinstance(resumen_raw, dict):
            resumen = resumen_raw
        elif isinstance(resumen_raw, str):
            try:
                resumen = json.loads(resumen_raw.strip())
            except json.JSONDecodeError:
                resumen = _extraer_json_de_respuesta(resumen_raw)
        else:
            resumen = None

        # creamos los archivos para guardar el resumen
        generar_nota_resumen(path_vault, resumen.get("tema"), resumen.get("resumen"), resumen.get("conceptos"), materia)

        # Generamos un mensaje para el ususario
        respuesta_agente = generar_salida_deseada(resumen.get("resumen"))

        return respuesta_agente

# ---------------------------------------
import json
import re
import ast
from typing import Dict, Optional, Any, Union

def validar_y_procesar_resumen(respuesta_raw: Any) -> Optional[Dict]:
    """
    Valida y procesa la respuesta para asegurar que sea un diccionario válido
    con los campos requeridos.
    """
    
    # Si ya es un diccionario, validarlo directamente
    if isinstance(respuesta_raw, dict):
        return _validar_estructura_resumen(respuesta_raw)
    
    # Si es string, intentar convertir a diccionario
    if isinstance(respuesta_raw, str):
        resumen_dict = _extraer_json_de_respuesta(respuesta_raw)
        if resumen_dict:
            return _validar_estructura_resumen(resumen_dict)
    
    print(f"⚠️  Error: No se pudo procesar la respuesta como diccionario válido")
    print(f"Tipo recibido: {type(respuesta_raw)}")
    print(f"Contenido: {respuesta_raw}")
    return None

def _validar_estructura_resumen(resumen: Dict) -> Optional[Dict]:
    """
    Valida que el diccionario tenga la estructura correcta y campos requeridos.
    """
    campos_requeridos = ["tema", "resumen", "conceptos"]
    campos_faltantes = []
    
    for campo in campos_requeridos:
        if campo not in resumen:
            campos_faltantes.append(campo)
    
    if campos_faltantes:
        print(f"⚠️  Campos faltantes en el resumen: {campos_faltantes}")
        # Intentar recuperar con valores por defecto
        resumen = _completar_campos_faltantes(resumen, campos_faltantes)
    
    # Validar tipos de datos
    if not isinstance(resumen.get("tema", ""), str):
        print("⚠️  El campo 'tema' debe ser string")
        resumen["tema"] = str(resumen.get("tema", "Tema sin definir"))
    
    if not isinstance(resumen.get("resumen", ""), str):
        print("⚠️  El campo 'resumen' debe ser string")
        resumen["resumen"] = str(resumen.get("resumen", "Resumen no disponible"))
    
    if not isinstance(resumen.get("conceptos", []), list):
        print("⚠️  El campo 'conceptos' debe ser una lista")
        resumen["conceptos"] = []
    
    # Validar estructura de conceptos
    conceptos_validados = []
    for i, concepto in enumerate(resumen.get("conceptos", [])):
        if isinstance(concepto, dict):
            if "concepto" in concepto and "desarrollo" in concepto:
                conceptos_validados.append(concepto)
            else:
                print(f"⚠️  Concepto {i+1} no tiene la estructura correcta, se omite")
        else:
            print(f"⚠️  Concepto {i+1} no es un diccionario, se omite")
    
    resumen["conceptos"] = conceptos_validados
    
    print(f"✅ Resumen validado correctamente:")
    print(f"   - Tema: {resumen['tema']}")
    print(f"   - Resumen: {len(resumen['resumen'])} caracteres")
    print(f"   - Conceptos: {len(resumen['conceptos'])} elementos")
    
    return resumen

def _completar_campos_faltantes(resumen: Dict, campos_faltantes: list) -> Dict:
    """
    Completa campos faltantes con valores por defecto.
    """
    valores_defecto = {
        "tema": "Tema sin definir",
        "resumen": "Resumen no disponible",
        "conceptos": [],
        "ejemplos": "Ejemplos no disponibles"
    }
    
    for campo in campos_faltantes:
        if campo in valores_defecto:
            resumen[campo] = valores_defecto[campo]
            print(f"📝 Campo '{campo}' completado con valor por defecto")
    
    return resumen

def _extraer_json_de_respuesta(respuesta: str) -> Optional[Dict]:
    """
    Extrae JSON de la respuesta del LLM, incluso si viene con texto adicional.
    Versión mejorada con más patrones de búsqueda.
    """
    
    try:
        # Limpiar respuesta
        respuesta_limpia = respuesta.strip()
        
        # Intentar parsear directamente
        return json.loads(respuesta_limpia)
    except json.JSONDecodeError:
        pass
    
    # Buscar JSON con diferentes patrones
    patrones_json = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # JSON simple
        r'\{.*?\}',  # JSON básico
        r'\{[\s\S]*\}',  # JSON con saltos de línea
    ]
    
    for patron in patrones_json:
        matches = re.findall(patron, respuesta, re.DOTALL)
        for match in matches:
            try:
                # Intentar con json.loads
                resultado = json.loads(match)
                if isinstance(resultado, dict):
                    return resultado
            except json.JSONDecodeError:
                try:
                    # Intentar con ast.literal_eval como respaldo
                    resultado = ast.literal_eval(match)
                    if isinstance(resultado, dict):
                        return resultado
                except (ValueError, SyntaxError):
                    continue
    
    print(f"❌ No se pudo extraer JSON válido de la respuesta")
    return None

# Función principal mejorada para tu caso de uso
def procesar_respuesta_y_generar_nota(intencion, informacion, materia, path_vault, generar_nota_resumen):
    """
    Procesa la respuesta y genera la nota de forma segura.
    """
    try:
        # Obtener respuesta (asumiendo que tienes una función respuesta)
        resumen_raw = respuesta(intencion, informacion)  # Tu función existente
        print("Respuesta recibida:", resumen_raw, end="\n")
        
        # Validar y procesar el resumen
        resumen = validar_y_procesar_resumen(resumen_raw)
        
        if resumen is None:
            print("❌ Error: No se pudo procesar el resumen")
            return {
                "error": "No se pudo procesar la respuesta",
                "respuesta_original": str(resumen_raw)
            }
        
        # Generar nota con los datos validados
        try:
            resultado_nota = generar_nota_resumen(
                path_vault, 
                resumen.get("tema", "Tema por defecto"), 
                resumen.get("resumen", ""), 
                resumen.get("conceptos", []), 
                materia
            )
            print("✅ Nota generada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al generar la nota: {str(e)}")
            return {
                "error": f"Error generando nota: {str(e)}",
                "resumen_procesado": resumen
            }
        
        return resumen
        
    except Exception as e:
        print(f"❌ Error general en el procesamiento: {str(e)}")
        return {
            "error": f"Error general: {str(e)}"
        }

# Función auxiliar para debug
def debug_respuesta(respuesta_raw):
    """
    Función para debuggear qué está devolviendo tu función respuesta()
    """
    print(f"🔍 DEBUG - Tipo de respuesta: {type(respuesta_raw)}")
    print(f"🔍 DEBUG - Es dict: {isinstance(respuesta_raw, dict)}")
    print(f"🔍 DEBUG - Es string: {isinstance(respuesta_raw, str)}")
    print(f"🔍 DEBUG - Contenido (primeros 200 chars): {str(respuesta_raw)[:200]}...")
    
    if isinstance(respuesta_raw, dict):
        print(f"🔍 DEBUG - Keys disponibles: {list(respuesta_raw.keys())}")
        for key in ["tema", "resumen", "conceptos"]:
            if key in respuesta_raw:
                print(f"🔍 DEBUG - {key}: Tipo {type(respuesta_raw[key])}")
    
    return respuesta_raw
import json
import re
import ast
from typing import Dict

class ValidadorRespuesta:
    """
    Encapsula toda la lógica de validación y procesamiento de respuestas del LLM.
    """
    
    def __init__(self):
        self.campos_requeridos = ["tema", "resumen", "conceptos"]
        self.valores_defecto = {
            "tema": "Tema sin definir",
            "resumen": "Resumen no disponible",
            "conceptos": [],
            "ejemplos": "Ejemplos no disponibles"
        }
    
    def validar_y_procesar(self, respuesta_raw) -> str:
        """Método principal para validar y procesar respuestas."""
        if isinstance(respuesta_raw, dict):
            return self._validar_estructura(respuesta_raw)
        elif isinstance(respuesta_raw, str):
            resumen_dict = self._extraer_json(respuesta_raw)
            if resumen_dict:
                return self._validar_estructura(resumen_dict)
        return None
    
    def _validar_estructura(self, resumen):
        """Valida la estructura del diccionario de resumen."""
        campos_requeridos = ["tema", "resumen", "conceptos"]
        campos_faltantes = []
        
        for campo in campos_requeridos:
            if campo not in resumen:
                campos_faltantes.append(campo)
        
        if campos_faltantes:
            print(f"⚠️  Campos faltantes en el resumen: {campos_faltantes}")
            # Intentar recuperar con valores por defecto
            resumen = self._completar_campos_faltantes(resumen, campos_faltantes)
        
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
    
    def _completar_campos_faltantes(self, resumen: Dict, campos_faltantes: list) -> Dict:
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
    def _extraer_json(self, respuesta):
        """Extrae JSON de respuesta de texto."""
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
    
    def debug_respuesta(self, respuesta_raw):
        """Método para debugging de respuestas."""
        pass
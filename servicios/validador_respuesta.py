import json
import re
from typing import Dict, Optional

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
    
    
    def validar_y_procesar(self, respuesta_raw) -> Dict:
        """Método principal para validar y procesar respuestas."""
        print(f"🔍 Procesando respuesta de tipo: {type(respuesta_raw)}")
        
        if isinstance(respuesta_raw, dict):
            return self._validar_estructura(respuesta_raw)
        elif isinstance(respuesta_raw, str):
            resumen_dict = self._extraer_json_robusto(respuesta_raw)
            if resumen_dict:
                return self._validar_estructura(resumen_dict)
            else:
                print("❌ No se pudo extraer JSON válido, intentando recuperación")
                return self._crear_respuesta_fallback(respuesta_raw)
        else:
            print(f"⚠️  Tipo de respuesta no soportado: {type(respuesta_raw)}")
            return self._crear_respuesta_vacia()
    
    def _extraer_json_robusto(self, respuesta: str) -> Optional[Dict]:
        """Extrae JSON con múltiples estrategias de recuperación."""
        
        # Estrategia 1: JSON directo
        json_directo = self._intentar_json_directo(respuesta)
        if json_directo:
            return json_directo
        
        # Estrategia 2: Reparar JSON común (agregar comas faltantes)
        json_reparado = self._reparar_json_comun(respuesta)
        if json_reparado:
            return json_reparado
        
        # Estrategia 3: Extraer con regex
        json_regex = self._extraer_con_regex(respuesta)
        if json_regex:
            return json_regex
        
        # Estrategia 4: Parseo manual para casos específicos
        json_manual = self._parseo_manual_llm(respuesta)
        if json_manual:
            return json_manual
        
        return None
    
    def _intentar_json_directo(self, respuesta: str) -> Optional[Dict]:
        """Intenta parsear JSON directamente."""
        try:
            respuesta_limpia = respuesta.strip()
            resultado = json.loads(respuesta_limpia)
            if isinstance(resultado, dict):
                print("✅ JSON parseado directamente")
                return resultado
        except json.JSONDecodeError as e:
            print(f"❌ Error JSON directo: {str(e)[:100]}")
        return None
    
    def _reparar_json_comun(self, respuesta: str) -> Optional[Dict]:
        """Repara errores comunes en JSON de LLM."""
        try:
            # 1. Agregar comas faltantes entre campos
            # Patrón: "campo": "valor"\n"otro_campo"
            respuesta_reparada = re.sub(r'("\s*)\n(\s*")', r'\1,\n\2', respuesta)
            
            # 2. Agregar comas después de } y antes de "
            respuesta_reparada = re.sub(r'(\})\s*\n\s*(")', r'\1,\n  \2', respuesta_reparada)
            
            # 3. Agregar comas después de ] y antes de "
            respuesta_reparada = re.sub(r'(\])\s*\n\s*(")', r'\1,\n\2', respuesta_reparada)
            
            # 4. Arreglar comillas en markdown dentro de strings
            # respuesta_reparada = re.sub(r'\*\*\[\[(.*?)\]\]\*\*', r'**\1**', respuesta_reparada)
            
            resultado = json.loads(respuesta_reparada)
            if isinstance(resultado, dict):
                print("✅ JSON reparado exitosamente (comas agregadas)")
                return resultado
                
        except json.JSONDecodeError as e:
            print(f"❌ Error en reparación JSON: {str(e)[:100]}")
        return None
    
    def _extraer_con_regex(self, respuesta: str) -> Optional[Dict]:
        """Extrae JSON usando patrones regex más específicos."""
        patrones_json = [
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # JSON simple
            r'\{[\s\S]*?\}(?=\s*$)',  # JSON hasta el final
            r'\{[\s\S]*\}',  # JSON con todo el contenido
        ]
        
        for i, patron in enumerate(patrones_json):
            matches = re.findall(patron, respuesta, re.DOTALL)
            for match in matches:
                # Intentar reparar antes de parsear
                match_reparado = self._reparar_json_comun(match)
                if match_reparado:
                    return match_reparado
                
                # Intentar parsear directo
                try:
                    resultado = json.loads(match)
                    if isinstance(resultado, dict):
                        print(f"✅ JSON extraído con regex patrón {i+1}")
                        return resultado
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def _parseo_manual_llm(self, respuesta: str) -> Optional[Dict]:
        """Parseo manual para respuestas específicas de LLM."""
        try:
            # Buscar campos específicos con regex
            resultado = {}
            
            # Extraer tema
            tema_match = re.search(r'"tema":\s*"([^"]*)"', respuesta)
            if tema_match:
                resultado["tema"] = tema_match.group(1)
            
            # Extraer resumen
            resumen_match = re.search(r'"resumen":\s*"([^"]*(?:"[^"]*"[^"]*)*)"', respuesta, re.DOTALL)
            if resumen_match:
                resultado["resumen"] = resumen_match.group(1)
            
            # Extraer conceptos (más complejo)
            conceptos_match = re.search(r'"conceptos":\s*\[([\s\S]*?)\]', respuesta)
            if conceptos_match:
                conceptos_str = conceptos_match.group(1)
                resultado["conceptos"] = self._extraer_conceptos_manual(conceptos_str)
            
            # Extraer ejemplos
            ejemplos_match = re.search(r'"ejemplos":\s*"([^"]*)"', respuesta)
            if ejemplos_match:
                resultado["ejemplos"] = ejemplos_match.group(1)
            
            if len(resultado) >= 2:  # Al menos 2 campos extraídos
                print("✅ JSON construido manualmente")
                return resultado
                
        except Exception as e:
            print(f"❌ Error en parseo manual: {e}")
        
        return None
    
    def _extraer_conceptos_manual(self, conceptos_str: str) -> list:
        """Extrae conceptos manualmente del string."""
        conceptos = []
        
        # Buscar patrones de conceptos
        patron_concepto = r'\{\s*"concepto":\s*"([^"]*)",\s*"desarrollo":\s*"([^"]*(?:"[^"]*"[^"]*)*)"\s*\}'
        matches = re.findall(patron_concepto, conceptos_str, re.DOTALL)
        
        for concepto, desarrollo in matches:
            conceptos.append({
                "concepto": concepto,
                "desarrollo": desarrollo
            })
        
        return conceptos
    
    def _crear_respuesta_fallback(self, respuesta_raw: str) -> Dict:
        """Crea una respuesta básica cuando no se puede parsear JSON."""
        return {
            "tema": "Error en procesamiento",
            "resumen": f"No se pudo procesar la respuesta. Contenido original: {respuesta_raw[:200]}...",
            "conceptos": [],
            "ejemplos": "No disponible",
            "error": "JSON malformado o no válido"
        }
    
    def _crear_respuesta_vacia(self) -> Dict:
        """Crea una respuesta vacía por defecto."""
        return {
            "tema": "Respuesta vacía",
            "resumen": "No se recibió respuesta válida",
            "conceptos": [],
            "ejemplos": "No disponible"
        }
    
    def _validar_estructura(self, resumen: Dict) -> Dict:
        """Valida la estructura del diccionario de resumen."""
        campos_requeridos = ["tema", "resumen", "conceptos"]
        campos_faltantes = []
        
        for campo in campos_requeridos:
            if campo not in resumen:
                campos_faltantes.append(campo)
        
        if campos_faltantes:
            print(f"⚠️  Campos faltantes en el resumen: {campos_faltantes}")
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
        """Completa campos faltantes con valores por defecto."""
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

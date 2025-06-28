import os
import json
import hashlib
from utils.rag.rag_local import LocalRetrievalSystem
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class RAGIncrementalSystem:
    """Sistema RAG que maneja actualizaciones incrementales de archivos."""
    
    def __init__(self, vectorstore_path: str = "./vectorstore_materias"):
        self.vectorstore_path = vectorstore_path
        self.metadata_path = f"{vectorstore_path}_metadata.json"
        self.retrieval_system = None
        
    def obtener_hash_archivo(self, file_path: str) -> str:
        """Obtiene el hash MD5 de un archivo para detectar cambios."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"⚠️ Error calculando hash de {file_path}: {e}")
            return ""
    
    def cargar_metadata_archivos(self) -> Dict:
        """Carga metadatos de archivos procesados previamente."""
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando metadata: {e}")
        
        return {
            "archivos_procesados": {},  # {file_path: {"hash": "", "timestamp": ""}}
            "ultima_actualizacion": "",
            "total_archivos": 0
        }
    
    def guardar_metadata_archivos(self, metadata: Dict):
        """Guarda metadatos de archivos procesados."""
        metadata["ultima_actualizacion"] = datetime.now().isoformat()
        try:
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando metadata: {e}")
    
    def detectar_cambios_archivos(self, carpetas_materias: List[str]) -> Dict:
        """
        Detecta archivos nuevos, modificados y eliminados.
        
        Returns:
            Dict con listas de archivos nuevos, modificados y eliminados
        """
        metadata = self.cargar_metadata_archivos()
        archivos_previos = set(metadata["archivos_procesados"].keys())
        
        # Obtener archivos actuales
        archivos_actuales = set()
        archivos_info_actual = {}
        
        for carpeta in carpetas_materias:
            if os.path.exists(carpeta):
                for archivo in Path(carpeta).rglob('*'):
                    if archivo.is_file() and self.es_archivo_soportado(archivo):
                        archivo_str = str(archivo)
                        archivos_actuales.add(archivo_str)
                        archivos_info_actual[archivo_str] = {
                            "hash": self.obtener_hash_archivo(archivo_str),
                            "timestamp": datetime.fromtimestamp(archivo.stat().st_mtime).isoformat()
                        }
        
        # Detectar cambios
        archivos_nuevos = archivos_actuales - archivos_previos
        archivos_eliminados = archivos_previos - archivos_actuales
        archivos_modificados = set()
        
        # Verificar archivos que existían antes
        for archivo in archivos_actuales & archivos_previos:
            hash_anterior = metadata["archivos_procesados"].get(archivo, {}).get("hash", "")
            hash_actual = archivos_info_actual[archivo]["hash"]
            
            if hash_anterior != hash_actual:
                archivos_modificados.add(archivo)
        
        return {
            "nuevos": list(archivos_nuevos),
            "modificados": list(archivos_modificados),
            "eliminados": list(archivos_eliminados),
            "info_archivos": archivos_info_actual,
            "metadata_previa": metadata
        }
    
    def es_archivo_soportado(self, archivo_path: Path) -> bool:
        """Verifica si el archivo tiene una extensión soportada."""
        extensiones_soportadas = {'.txt', '.pdf', '.docx', '.doc', '.md', '.rtf', '.csv'}
        return archivo_path.suffix.lower() in extensiones_soportadas
    
    def procesar_archivos_incrementalmente(self, carpetas_materias: List[str]) -> bool:
        """
        Procesa solo archivos nuevos o modificados.
        
        Returns:
            True si hubo cambios, False si no
        """
        print("🔍 Detectando cambios en archivos...")
        
        cambios = self.detectar_cambios_archivos(carpetas_materias)
        
        total_cambios = len(cambios["nuevos"]) + len(cambios["modificados"]) + len(cambios["eliminados"])
        
        if total_cambios == 0:
            print("✅ No hay cambios detectados. Vector store actual está actualizado.")
            return False
        
        print(f"📊 Cambios detectados:")
        print(f"   📄 Archivos nuevos: {len(cambios['nuevos'])}")
        print(f"   ✏️ Archivos modificados: {len(cambios['modificados'])}")
        print(f"   🗑️ Archivos eliminados: {len(cambios['eliminados'])}")
        
        # Mostrar archivos específicos si no son demasiados
        if len(cambios["nuevos"]) <= 10:
            for archivo in cambios["nuevos"]:
                print(f"      + {Path(archivo).name}")
        
        if len(cambios["modificados"]) <= 10:
            for archivo in cambios["modificados"]:
                print(f"      ✏️ {Path(archivo).name}")
        
        # Procesar archivos nuevos y modificados
        archivos_a_procesar = cambios["nuevos"] + cambios["modificados"]
        
        if archivos_a_procesar:
            print(f"\n🔄 Procesando {len(archivos_a_procesar)} archivos...")
            
            # Cargar y procesar solo archivos nuevos/modificados
            documentos_nuevos = []
            
            for archivo in archivos_a_procesar:
                try:
                    # Aquí deberías usar tu método específico para cargar un solo archivo
                    docs = self.retrieval_system.load_single_document(archivo)
                    if docs:
                        documentos_nuevos.extend(docs)
                        print(f"   ✅ {Path(archivo).name}")
                    else:
                        print(f"   ⚠️ No se pudo procesar: {Path(archivo).name}")
                except Exception as e:
                    print(f"   ❌ Error procesando {Path(archivo).name}: {e}")
            
            if documentos_nuevos:
                # Dividir en chunks
                texts = self.retrieval_system.split_documents(documentos_nuevos)
                print(f"📝 {len(texts)} chunks generados de archivos nuevos/modificados")
                
                # Agregar al vector store existente
                self.retrieval_system.add_documents_to_vectorstore(texts)
                print("✅ Documentos agregados al vector store existente")
        
        # Actualizar metadata
        metadata_nueva = cambios["metadata_previa"]
        
        # Agregar/actualizar archivos procesados
        for archivo, info in cambios["info_archivos"].items():
            if archivo not in cambios["eliminados"]:
                metadata_nueva["archivos_procesados"][archivo] = info
        
        # Remover archivos eliminados
        for archivo in cambios["eliminados"]:
            if archivo in metadata_nueva["archivos_procesados"]:
                del metadata_nueva["archivos_procesados"][archivo]
        
        metadata_nueva["total_archivos"] = len(metadata_nueva["archivos_procesados"])
        self.guardar_metadata_archivos(metadata_nueva)
        
        return True


def iniciar_rag_con_actualizacion_incremental(
    vault_path: str,
    materias_incluir: Optional[List[str]] = None,
    materias_excluir: Optional[List[str]] = None,
    vectorstore_path: str = "./vectorstore_materias",
    forzar_recrear: bool = False
):
    """
    Inicializa RAG con detección automática de cambios y actualización incremental.
    
    Args:
        vault_path: Ruta base del vault
        materias_incluir: Lista de materias específicas a incluir
        materias_excluir: Lista de materias a excluir
        vectorstore_path: Ruta del vector store
        forzar_recrear: Si True, recrea todo el vector store desde cero
    """
    
    print("🎓 SISTEMA RAG INCREMENTAL PARA MATERIAS")
    print("=" * 50)
    
    # Obtener carpetas de materias
    info_materias = obtener_info_materias(vault_path)
    
    if not info_materias:
        print("❌ No se encontraron materias")
        return None
    
    # Filtrar materias
    carpetas_filtradas = filtrar_materias(info_materias, materias_incluir, materias_excluir)
    carpetas_materias = list(carpetas_filtradas.values())
    
    if not carpetas_materias:
        print("❌ No hay carpetas válidas después del filtrado")
        return None
    
    # Inicializar sistema incremental
    rag_incremental = RAGIncrementalSystem(vectorstore_path)
    
    # Inicializar sistema de recuperación
    rag_incremental.retrieval_system = LocalRetrievalSystem(
        embedding_model="all-MiniLM-L6-v2"
    )
    
    try:
        vector_store_existe = os.path.exists(vectorstore_path)
        
        if forzar_recrear or not vector_store_existe:
            print(f"\n🔄 {'Recreando' if forzar_recrear else 'Creando'} vector store desde cero...")
            
            # Crear desde cero (código original)
            all_documents = []
            for carpeta in carpetas_materias:
                if os.path.exists(carpeta):
                    documentos = rag_incremental.retrieval_system.load_documents(carpeta)
                    if documentos:
                        all_documents.extend(documentos)
            
            if all_documents:
                texts = rag_incremental.retrieval_system.split_documents(all_documents)
                rag_incremental.retrieval_system.create_vectorstore(texts, vectorstore_path)
                
                # Crear metadata inicial
                metadata = {"archivos_procesados": {}, "total_archivos": 0}
                for carpeta in carpetas_materias:
                    if os.path.exists(carpeta):
                        for archivo in Path(carpeta).rglob('*'):
                            if archivo.is_file() and rag_incremental.es_archivo_soportado(archivo):
                                archivo_str = str(archivo)
                                metadata["archivos_procesados"][archivo_str] = {
                                    "hash": rag_incremental.obtener_hash_archivo(archivo_str),
                                    "timestamp": datetime.fromtimestamp(archivo.stat().st_mtime).isoformat()
                                }
                
                metadata["total_archivos"] = len(metadata["archivos_procesados"])
                rag_incremental.guardar_metadata_archivos(metadata)
                
                print("✅ Vector store creado desde cero")
            else:
                print("❌ No se cargaron documentos")
                return None
                
        else:
            print("\n📂 Cargando vector store existente...")
            rag_incremental.retrieval_system.load_vectorstore(vectorstore_path)
            
            # Verificar y procesar cambios incrementales
            hubo_cambios = rag_incremental.procesar_archivos_incrementalmente(carpetas_materias)
            
            if not hubo_cambios:
                print("📊 Vector store está actualizado")
            else:
                print("🔄 Vector store actualizado incrementalmente")
        
        return rag_incremental.retrieval_system
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# Funciones auxiliares (reutilizadas del código anterior)
def obtener_info_materias(vault_path: str) -> Dict[str, Dict]:
    """Obtiene información de materias del vault."""
    materias_path = Path(vault_path) / "Materias"
    info_materias = {}
    
    if not materias_path.exists():
        return {}
    
    for materia_dir in materias_path.iterdir():
        if materia_dir.is_dir():
            archivos_dir = materia_dir / "Archivos"
            archivo_count = 0
            
            if archivos_dir.exists():
                for archivo in archivos_dir.rglob('*'):
                    if archivo.is_file():
                        archivo_count += 1
            
            info_materias[materia_dir.name] = {
                'path': str(archivos_dir),
                'existe_carpeta_archivos': archivos_dir.exists(),
                'total_archivos': archivo_count
            }
    
    return info_materias


def filtrar_materias(info_materias: Dict, 
                    incluir: Optional[List[str]] = None,
                    excluir: Optional[List[str]] = None) -> Dict[str, str]:
    """Filtra materias según criterios."""
    carpetas_filtradas = {}
    
    for materia, info in info_materias.items():
        if not info['existe_carpeta_archivos'] or info['total_archivos'] == 0:
            continue
            
        if incluir and materia not in incluir:
            continue
            
        if excluir and materia in excluir:
            continue
            
        carpetas_filtradas[materia] = info['path']
    
    return carpetas_filtradas
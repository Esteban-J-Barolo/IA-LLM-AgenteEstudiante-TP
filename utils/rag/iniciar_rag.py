import os
from utils.rag.rag_local import LocalRetrievalSystem

import shutil


def iniciar_rag():
    # Eliminar caché de sentence-transformers
    # cache_dir = os.path.expanduser("~/.cache/torch/sentence_transformers")
    # if os.path.exists(cache_dir):
    #     shutil.rmtree(cache_dir)

    # Configuración
    data_folder = "./data"
    vectorstore_path = "./my_local_vectorstore"
    
    # Crear carpeta de datos si no existe
    os.makedirs(data_folder, exist_ok=True)
    
    # Inicializar sistema de recuperación
    retrieval_system = LocalRetrievalSystem(
        embedding_model="all-MiniLM-L6-v2"
        # embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Crear o cargar vector store
    try:
        if not os.path.exists(vectorstore_path):
            print("\n📁 Cargando documentos...")
            documents = retrieval_system.load_documents(data_folder)
            
            if documents:
                texts = retrieval_system.split_documents(documents)
                retrieval_system.create_vectorstore(texts, vectorstore_path)
            else:
                print("❌ No se pudieron cargar documentos")
                return
        else:
            print("\n📂 Cargando vector store existente...")
            retrieval_system.load_vectorstore(vectorstore_path)
        
        # Mostrar información del vector store
        # info = retrieval_system.get_vectorstore_info()
        # print(f"\n📊 Información del vector store: {info}")
        
        # Realizar búsquedas de ejemplo
        # print("\n" + "=" * 60)
        # print("🔍 BÚSQUEDAS DE EJEMPLO")
        # print("=" * 60)
        
        # queries = [
        #     "¿Qué es la inteligencia artificial?",
        #     "tipos de machine learning",
        #     "modelos de lenguaje",
        #     "IA generativa y aplicaciones"
        # ]
        
        # for query in queries:
        #     print(f"\n❓ Consulta: {query}")
        #     print("-" * 50)
            
        #     results = retrieval_system.search_and_format(query, k=3)
            
        #     if results:
        #         for result in results:
        #             print(f"\n📄 Resultado {result['rank']}:")
        #             print(f"   Fuente: {result['source']}")
        #             print(f"   Contenido: {result['content']}")
        #     else:
        #         print("   No se encontraron resultados relevantes")
        
        # print("\n" + "=" * 60)
        # print("✅ Sistema de recuperación funcionando correctamente!")
        # print("💡 Ahora puedes usar este sistema para recuperar documentos relevantes")
        # print("   y procesarlos con tu propio sistema de generación de respuestas.")

        return retrieval_system
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        print("Verifica las dependencias y la instalación de los modelos.")

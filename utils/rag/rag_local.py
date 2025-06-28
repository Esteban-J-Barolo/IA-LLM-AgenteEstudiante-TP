# Instalación simplificada para uso local
# pip install langchain langchain-huggingface sentence-transformers faiss-cpu pypdf2 python-docx
# pip install langchain-community unstructured

import os
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    DirectoryLoader,
    UnstructuredWordDocumentLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path

class LocalRetrievalSystem:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        """
        Sistema de recuperación de documentos completamente local
        
        Args:
            embedding_model: Modelo para embeddings (soporta español)
        """
        print(f"Inicializando sistema de recuperación...")
        
        # Configurar embeddings locales
        self.embeddings = self._setup_embeddings(embedding_model)
        
        self.vectorstore = None
        self.retriever = None
        
    def _setup_embeddings(self, model_name):
        """Configura embeddings locales"""
        print(f"Cargando modelo de embeddings: {model_name}")
        
        model_kwargs = {
            'device': 'cpu',  # Usar CPU por defecto para mayor compatibilidad
            'trust_remote_code': True
        }
        
        encode_kwargs = {
            'normalize_embeddings': True
        }
        
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        
        print("✅ Embeddings cargados exitosamente")
        return embeddings
    
    def load_documents(self, data_path, file_types=["txt", "pdf", "docx"]):
        """
        Carga documentos de múltiples formatos
        """
        # Crear documentos de ejemplo si el directorio está vacío
        if not any(os.listdir(data_path)) if os.path.exists(data_path) else True:
            print("📁 Directorio vacío, creando documentos de ejemplo...")
            self.create_sample_documents(data_path)
        
        all_documents = []
        
        for file_type in file_types:
            try:
                if file_type == "txt":
                    loader = DirectoryLoader(
                        data_path, 
                        glob="*.txt", 
                        loader_cls=TextLoader,
                        loader_kwargs={'encoding': 'utf-8'}
                    )
                elif file_type == "pdf":
                    loader = DirectoryLoader(
                        data_path, 
                        glob="*.pdf", 
                        loader_cls=PyPDFLoader
                    )
                elif file_type == "docx":
                    loader = DirectoryLoader(
                        data_path, 
                        glob="*.docx", 
                        loader_cls=UnstructuredWordDocumentLoader
                    )
                else:
                    continue
                
                docs = loader.load()
                all_documents.extend(docs)
                print(f"✅ Cargados {len(docs)} archivos {file_type.upper()}")
            except Exception as e:
                print(f"⚠️  Error cargando archivos {file_type}: {e}")
        
        print(f"📚 Total de documentos cargados: {len(all_documents)}")
        return all_documents

    def load_single_document(self, file_path: str):
        """Carga un solo documento desde un archivo específico."""
        try:
            
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"❌ Archivo no encontrado: {file_path}")
                return []
            
            file_extension = file_path.suffix.lower()
            
            if file_extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif file_extension in ['.docx', '.doc']:
                loader = Docx2txtLoader(str(file_path))
            elif file_extension in ['.txt', '.md']:
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif file_extension == '.csv':
                loader = TextLoader(str(file_path), encoding='utf-8')
            else:
                print(f"⚠️ Tipo de archivo no soportado: {file_extension}")
                return []
                
            return loader.load()
            
        except Exception as e:
            print(f"❌ Error cargando {file_path}: {e}")
            return []
        
    def add_documents_to_vectorstore(self, texts):
        """Agrega nuevos documentos al vector store existente."""
        try:
            if self.vectorstore is None:
                print("❌ Vector store no está inicializado")
                return False
            
            # Agregar documentos al vector store existente
            self.vectorstore.add_documents(texts)
            print(f"✅ {len(texts)} documentos agregados al vector store")
            return True
            
        except Exception as e:
            print(f"❌ Error agregando documentos al vector store: {e}")
            return False
    
    def split_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        """
        Divide documentos en chunks optimizados
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        texts = text_splitter.split_documents(documents)
        print(f"📄 Documentos divididos en {len(texts)} chunks")
        return texts
    
    def create_vectorstore(self, texts, save_path=None):
        """
        Crea vector store local con FAISS
        """
        print("🔄 Creando embeddings y vector store...")
        
        # Crear vector store
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        
        # Configurar retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Guardar automáticamente si se especifica path
        if save_path:
            self.save_vectorstore(save_path)
        
        print("✅ Vector store creado exitosamente")
    
    def save_vectorstore(self, path="local_vectorstore"):
        """
        Guarda vector store en disco
        """
        if self.vectorstore is None:
            raise ValueError("No hay vector store para guardar")
        
        os.makedirs(path, exist_ok=True)
        
        # Usar allow_dangerous_deserialization para evitar warnings
        self.vectorstore.save_local(path)
        
        print(f"💾 Vector store guardado en: {path}")
    
    def load_vectorstore(self, path="local_vectorstore"):
        """
        Carga vector store desde disco
        """
        try:
            # Usar allow_dangerous_deserialization para cargar
            self.vectorstore = FAISS.load_local(
                path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            print(f"✅ Vector store cargado desde: {path}")
        except Exception as e:
            print(f"❌ Error cargando vector store: {e}")
            raise
    
    def similarity_search(self, query, k=5, score_threshold=None):
        """
        Búsqueda por similaridad con puntuación opcional
        """
        if self.vectorstore is None:
            raise ValueError("No hay vector store disponible")
        
        if score_threshold is not None:
            # Búsqueda con puntuación de similaridad
            docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=k)
            filtered_docs = [(doc, score) for doc, score in docs_with_scores if score <= score_threshold]
            return filtered_docs
        else:
            # Búsqueda normal
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
    
    def retrieve_relevant_docs(self, query, k=4):
        """
        Recupera documentos relevantes usando el retriever
        """
        if self.retriever is None:
            raise ValueError("No hay retriever disponible")
        
        # Actualizar el número de documentos a recuperar
        self.retriever.search_kwargs["k"] = k
        
        docs = self.retriever.get_relevant_documents(query)
        return docs
    
    def search_and_format(self, query, min_score=0.7, max_docs=10, max_content_length=300):
        """
        
        Busca documentos por relevancia mínima con límite máximo
        
        Args:
            query: Consulta del usuario
            min_score: Puntuación mínima de similitud (0.7 recomendado)
            max_docs: Máximo número de documentos a devolver (10 recomendado)
            max_content_length: Máximo caracteres por documento
        """
        print(f"🔍 Buscando: {query}")
        
        try:
            # docs = self.retrieve_relevant_docs(query, k)
            
            # Buscar más documentos inicialmente para filtrar por score
            docs_with_scores = self.vectorstore.similarity_search_with_score(
                query, k=max_docs * 2  # Buscar el doble para filtrar
            )
            
            # Filtrar por score mínimo
            filtered_docs = [
                (doc, score) for doc, score in docs_with_scores 
                if score >= min_score
            ]

            # Limitar al máximo
            filtered_docs = filtered_docs[:max_docs]

            results = []
            for i, (doc, score) in enumerate(filtered_docs):
                content = doc.page_content
                if len(content) > max_content_length:
                    content = content[:max_content_length] + "..."
                
                result = {
                    "rank": i + 1,
                    "content": content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "Desconocido"),
                    "similarity_score": round(score, 3)  # Útil para debugging
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    def get_vectorstore_info(self):
        """
        Obtiene información del vector store
        """
        if self.vectorstore is None:
            return "No hay vector store cargado"
        
        try:
            # Información básica del vector store
            info = {
                "total_documents": self.vectorstore.index.ntotal,
                "embedding_dimension": self.vectorstore.index.d,
                "index_type": type(self.vectorstore.index).__name__
            }
            return info
        except Exception as e:
            return f"Error obteniendo información: {e}"
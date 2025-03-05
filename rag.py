import os
from settings import settings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_core.documents import Document

# Path to the PDF file in the container
PDF_PATH = "/app/data/knowledge_base.pdf"

class RAGManager:
    def __init__(self):
        self.vector_store = None
        self.qa_chain = None
        self.initialize_rag()

    def initialize_rag(self):
        """Initialize the RAG system by loading and processing the PDF"""
        try:
            # Load PDF
            if not os.path.exists(PDF_PATH):
                print(f"Warning: PDF file not found at {PDF_PATH}")
                return
                
            loader = PyPDFLoader(PDF_PATH)
            documents = loader.load()

            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.RAG_CHUNK_SIZE,
                chunk_overlap=200,
                length_function=len
            )
            texts = text_splitter.split_documents(documents)

            # Create embeddings using Ollama
            embeddings = OllamaEmbeddings(
                model=settings.OLLAMA_MODEL,
                base_url=os.getenv("OLLAMA_HOST", settings.OLLAMA_HOST)
            )

            # Create vector store
            if texts:
                self.vector_store = FAISS.from_documents(texts, embeddings)

                # Initialize Ollama LLM
                llm = Ollama(
                    model=settings.OLLAMA_MODEL,
                    base_url=os.getenv("OLLAMA_HOST", settings.OLLAMA_HOST)
                )

                # Create QA chain
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=self.vector_store.as_retriever(
                        search_kwargs={"k": settings.RAG_NUM_CHUNKS}
                    )
                )
            else:
                print("Warning: No text chunks were created from the PDF")

        except Exception as e:
            print(f"Error initializing RAG: {e}")
            raise

    def query_knowledge_base(self, query: str) -> str:
        """
        Query the knowledge base using the provided question
        
        Args:
            query: The question to ask
            
        Returns:
            Answer from the RAG system
        """
        try:
            if not self.qa_chain:
                return "RAG system not initialized. Please make sure the PDF file exists and is accessible."

            result = self.qa_chain.run(query)
            return result
        except Exception as e:
            print(f"Error querying knowledge base: {e}")
            return f"Error processing query: {str(e)}"

# Create a global instance
rag_manager = RAGManager() 